from openerp import models, fields, api

import datetime
import logging
_logger = logging.getLogger(__name__)


class hr_contract_with_advantages(models.Model):
    _inherit = 'hr.contract'

    advantage_ids = fields.One2many('hr.contract.advantage', 'contract_id', 'Advantages')

    