from openerp import api, models, fields

class hr_holiday_archived(models.Model):
    _inherit = 'hr.holidays'
    
    active = fields.Boolean('Active', default=True)

    @api.multi
    def archive_holiday(self):
        for holiday in self:
            holiday.active = False

    @api.multi
    def unarchive_holiday(self):
        for holiday in self:
            holiday.active = True