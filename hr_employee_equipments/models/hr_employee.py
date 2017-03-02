from openerp import models, fields, api
import datetime
from datetime import date


class hr_employee_equiped(models.Model):
    _inherit = 'hr.employee'

    equipment_ids = fields.One2many('hr.equipment', 'employee_id', 'Equipments')
    equipment_count = fields.Integer(compute='_compute_equipment_cout', string='Number of equipments')

    @api.one
    @api.depends('equipment_ids')
    def _compute_equipment_cout(self):
        self.equipment_count = len(self.equipment_ids)
        return len(self.equipment_ids)