from openerp import models, fields, api

import logging
_logger = logging.getLogger(__name__)


class hr_contract_advantage(models.Model):
    _name = 'hr.contract.advantage'
    _description = 'Employee contract advantage'

    name = fields.Char('Name', required=True)
    contract_id = fields.Many2one('hr.contract', 'Contract', required=True)
    date_start = fields.Date('Start Date')
    date_end = fields.Date('End Date')
    state = fields.Selection([('draft', 'Draft'), ('active', 'Active'), ('end', 'Ended')], 'State', default='draft', required=True)
    type = fields.Selection([('vehicle', 'Vehicle'), ('card', 'Card'), ('equipment', 'Equipment'), ('other', 'Other')], 'Type', default='other', required=True)
    vehicle_id = fields.Many2one('fleet.vehicle', 'Vehicle')
    card_id = fields.Many2one('hr.contract.advantage.card', 'Card')
    equipment_id = fields.Many2one('hr.equipment', 'Equipment')
    description = fields.Text('Description')

    