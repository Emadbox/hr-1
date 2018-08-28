# -*- coding: utf-8 -*-
# (c) AbAKUS IT Solutions
from odoo import api, fields, models, _
from odoo.exceptions import UserError
import odoo.addons.decimal_precision as dp


class Expense(models.Model):
    _inherit = 'hr.expense'

    state = fields.Selection([
        ('draft', 'To Submit'),
        ('submit', 'Submitted'),
        ('approve', 'Approved'),
        ('moves_generated', 'Moves generated'),
        ('post', 'Waiting Payment'),
        ('done', 'Paid'),
        ('cancel', 'Refused')], string='Status', index=True, readonly=True, track_visibility='onchange',
                             copy=False, default='draft', required=True,
                             help="""When the expense request is created the status is \'To Submit\'.\n
         It is submitted by the employee and request is sent to manager, the status is \'Submitted\'.\n
         If the manager approve it, the status is \'Approved\'.\n
         If the accountant generates the accounting entries for the expense request, the status is \'Waiting Payment\'.
         """)

    @api.multi
    def action_move_create(self):
        """
        main function that is called when trying to create the accounting entries related to an expense
        """
        if any(expense.state != 'approve' for expense in self):
            raise UserError(_("You can only generate accounting entry for approved expense(s)."))

        if any(expense.employee_id != self[0].employee_id for expense in self):
            raise UserError(_("Expenses must belong to the same Employee."))

        if any(not expense.journal_id for expense in self):
            raise UserError(_("Expenses must have an expense journal specified to generate accounting entries."))

        journal_dict = {}
        max_date = False
        for expense in self:
            if expense.date > max_date:
                max_date = expense.date
            jrn = expense.bank_journal_id if expense.payment_mode == 'company_account' else expense.journal_id
            journal_dict.setdefault(jrn, [])
            journal_dict[jrn].append(expense)

        for journal, expense_list in journal_dict.items():
            # create the move that will contain the accounting entries
            move = self.env['account.move'].create({
                'journal_id': journal.id,
                'company_id': self.env.user.company_id.id,
                'date': max_date,
            })
            for expense in expense_list:
                company_currency = expense.company_id.currency_id
                diff_currency_p = expense.currency_id != company_currency
                # one account.move.line per expense (+taxes..)
                move_lines = expense._move_line_get()

                # create one more move line, a counterline for the total on payable account
                total, total_currency, move_lines = expense._compute_expense_totals(company_currency, move_lines,
                                                                                    max_date)
                if expense.payment_mode == 'company_account':
                    if not expense.bank_journal_id.default_credit_account_id:
                        raise UserError(_("No credit account found for the %s journal, please configure one.") % (
                            expense.bank_journal_id.name))
                    emp_account = expense.bank_journal_id.default_credit_account_id.id
                else:
                    if not expense.employee_id.address_home_id:
                        raise UserError(_("No Home Address found for the employee %s, please configure one.") % (
                            expense.employee_id.name))
                    emp_account = expense.employee_id.address_home_id.property_account_payable_id.id

                move_lines.append({
                    'type': 'dest',
                    'name': expense.employee_id.name,
                    'price': total,
                    'account_id': emp_account,
                    'date_maturity': expense.date,
                    'amount_currency': diff_currency_p and total_currency or False,
                    'currency_id': diff_currency_p and expense.currency_id.id or False,
                    'ref': expense.employee_id.address_home_id.ref or False
                })

                # convert eml into an osv-valid format
                lines = map(lambda x: (0, 0, expense._prepare_move_line(x)), move_lines)
                move.write({'line_ids': lines})
                expense.write({'account_move_id': move.id, 'state': 'moves_generated'})
                if expense.payment_mode == 'company_account':
                    expense.paid_expenses()
        return True

    @api.multi
    def action_move_post(self):
        for expense in self:
            if expense.account_move_id:
                expense.account_move_id.post()
                expense.write({'state': 'post'})
