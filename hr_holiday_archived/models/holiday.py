from odoo import api, models, fields

class hr_holiday_archived(models.Model):
    _inherit = 'hr.holidays'
    
    active = fields.Boolean('Active', default=True)

    @api.model
    def _archive_holiday(self):
        for holiday in self:
            if holiday.active:
                holiday.active = False
            else:
                holiday.active = True
