from openerp import models, fields, api

import logging
_logger = logging.getLogger(__name__)


class hr_employee_with_bonuses(models.Model):
    _inherit = 'hr.employee'

    bonus_ids = fields.One2many('hr.employee.bonus', 'employee_id', 'Bonuses')
    bonus_count = fields.Integer(compute='_compute_bonuses_count', string='Bonuses')

    def _compute_bonuses_count(self):
        for employee in self:
            employee.bonus_count = len(employee.bonus_ids)

    