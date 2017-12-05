from openerp import models, fields, api

import logging
_logger = logging.getLogger(__name__)


class hr_contract_advantage_card(models.Model):
    _name = 'hr.contract.advantage.card'
    _description = 'Contract card advantage'

    name = fields.Char('Name', required=True)
    number = fields.Char('Number')
    advantage_id = fields.Many2one('hr.contract.advantage', 'Advantage')
    #employee_id = fields.
    state = fields.Selection([('draft', 'Draft'), ('active', 'Active'), ('end', 'Ended')], 'State', default='draft')
    type = fields.Many2one('hr.contract.advantage.card.type', 'Type', required=True)