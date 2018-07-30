from odoo import api, fields, models, _, tools

import logging
_logger = logging.getLogger(__name__)

class HrHolidays(models.Model):
    _inherit = ['hr.holidays']

    @api.multi
    def _prepare_holidays_meeting_values(self):
        self.ensure_one()
        res = super(HrHolidays, self)._prepare_holidays_meeting_values()

        res['categ_ids'] = self.holiday_status_id.categ_id.id

        return res
        

    