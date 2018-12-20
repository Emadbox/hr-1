from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

from datetime import datetime

import logging

_logger = logging.getLogger(__name__)

class HrTimesheetSheet(models.Model):
    _inherit = ['hr_timesheet_sheet.sheet']

    submit_date = fields.Datetime(string="First submit date")

    def button_confirm(self, cr, uid, ids, context=None):
        if super(HrTimesheetSheet, self).button_confirm(cr, uid, ids, context):
            for sheet in self.browse(cr, uid, ids, context=context):
                if sheet.submit_date == False:
                    sheet.submit_date = datetime.now()
        return True