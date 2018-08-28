# -*- coding: utf-8 -*-
# (c) AbAKUS IT Solutions
from odoo import models, fields


class HrEmployee(models.Model):
    _inherit = ['hr.employee']

    # Add a new columns
    entry_date = fields.Date('Start date')

    key_number = fields.Char()
    has_badge = fields.Boolean('Has a building badge')

    computer_model = fields.Char()
    computer_serial = fields.Char('Computer serial number')
    computer_acquisition_date = fields.Date('Date of acquisition')

    partner_id = fields.Many2one('res.partner',
                                 string='Fuel company',
                                 help='Select a partner for this fuel card if it exists.',
                                 ondelete='restrict')
    fuel_card_number = fields.Char()
    fuel_card_pin = fields.Char()
    notes = fields.Char()
