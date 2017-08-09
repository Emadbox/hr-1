# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions, _

import logging
_logger = logging.getLogger(__name__)

class Bonus(models.Model):
    _name = 'hr.bonus'
    _order = 'date desc'

    name = fields.Char(string='Name', copy=False, index=True, required=True, readonly=True, states={'draft': [('readonly', False)]})
    description = fields.Text(string='Description', readonly=True, states={'draft': [('readonly', False)]})
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('refused', 'Refused')
    ], string='State', default='draft', required=True)
    date = fields.Datetime(string='Date', required=True, readonly=True, states={'draft': [('readonly', False)]})
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, readonly=True, states={'draft': [('readonly', False)]}, default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.user.id)]))

    @api.one
    def action_draft(self):
        self.write({'state': 'draft'})

    @api.one
    def action_submit(self):
        self.write({'state': 'submitted'})

    @api.one
    def action_approve(self):
        self.write({'state': 'approved'})

    @api.one
    def action_refuse(self):
        self.write({'state': 'refused'})

    @api.one
    def action_unlink(self):
        self.sudo().unlink()