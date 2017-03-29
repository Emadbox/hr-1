from openerp import models, fields, api

import logging
_logger = logging.getLogger(__name__)


class hr_contract_advantage_card_type(models.Model):
    _name = 'hr.contract.advantage.card.type'
    _description = 'Contract card advantage type'

    name = fields.Char('Name', required=True)
    description = fields.Text('Description')
