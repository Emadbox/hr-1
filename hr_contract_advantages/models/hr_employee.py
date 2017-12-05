from openerp import models, fields, api

import logging
_logger = logging.getLogger(__name__)


class hr_employee_with_advantages(models.Model):
    _inherit = 'hr.employee'

    advantages_count = fields.Integer(compute='_compute_advantages_count', string='Advantages')

    def _compute_advantages_count(self):
        count = 0
        for employee in self:
            for contract in employee.contract_ids:
                count += len(contract.advantage_ids)
            employee.advantages_count = count

    