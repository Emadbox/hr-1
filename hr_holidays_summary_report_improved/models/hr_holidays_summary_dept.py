# -*- coding: utf-8 -*-
# (c) AbAKUS IT Solutions
import time
from odoo import models, fields, api, exceptions, _


class HrHolidaysSummaryDept(models.TransientModel):
    _inherit = 'hr.holidays.summary.dept'

    month = fields.Selection([
        ('01', 'January'),
        ('02', 'February'),
        ('03', 'March'),
        ('04', 'April'),
        ('05', 'May'),
        ('06', 'June'),
        ('07', 'July'),
        ('08', 'August'),
        ('09', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December')
    ], required=True, default=lambda *a: time.strftime('%m'))
    year = fields.Integer(required=True, default=lambda *a: int(time.strftime('%Y')))
    company_id = fields.Many2one(
        'res.company',
        'Company',
        default=lambda self: self.env['res.company']._company_default_get('hr.holidays.summary.dept'))

    hide_empty_categories = fields.Boolean(string="Hide Empty Departments", default=True)
    hide_empty_status = fields.Boolean(string="Hide Empty Leave Types", default=True)
    hide_no_leaves_emp = fields.Boolean(string="Hide Employees Without Leaves", default=True)

    depts = fields.Many2many('hr.department', 'summary_dept_rel', 'sum_id', 'dept_id', string='Department(s)')

    @api.one
    @api.onchange('month', 'year')
    def onchange_date(self):
        if not self.month or not self.year or self.year < 0 or self.year > 9999:
            self.date_from = False
        else:
            self.date_from = str(self.year).zfill(4) + '-' + self.month + '-01'
