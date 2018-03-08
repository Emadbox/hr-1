from odoo import api, models, fields

class hr_holiday_archived(models.Model):
    _inherit = 'hr.holidays'
    
    active = fields.Boolean('Active', default=True)
