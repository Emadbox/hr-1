from openerp import models, fields, api, _
from openerp.exceptions import ValidationError

from datetime import datetime
import time
from dateutil.relativedelta import relativedelta

import logging

_logger = logging.getLogger(__name__)

class HrTimesheetSheet(models.Model):
    _inherit = ['hr_timesheet_sheet.sheet']

    # Redefine default methods
    def _default_date_to(self):
        user = self.env.user
        employee_id = self.env['hr.employee'].search([('user_id', '=', user.id)])
        
        r = employee_id and employee_id.department_id.default_timesheet_duration or 'month'
        if r=='month':
            return (datetime.today() + relativedelta(months=+1,day=1,days=-1)).strftime('%Y-%m-%d')
        elif r=='week':
            return (datetime.today() + relativedelta(weekday=6)).strftime('%Y-%m-%d')
        elif r=='year':
            return time.strftime('%Y-12-31')
        return fields.date.context_today(self, cr, uid, context)

    def _default_date_from(self):
        user = self.env.user
        employee_id = self.env['hr.employee'].search([('user_id', '=', user.id)])

        r = employee_id and employee_id.department_id.default_timesheet_duration or 'month'
        if r=='month':
            return time.strftime('%Y-%m-01')
        elif r=='week':
            return (datetime.today() + relativedelta(weekday=0, days=-6)).strftime('%Y-%m-%d')
        elif r=='year':
            return time.strftime('%Y-01-01')
        return fields.date.context_today(self, cr, uid, context)

    # Redefine fields and their default value methods
    date_from = fields.Date(string='Date from', required=True, select=1, readonly=True, states={'new':[('readonly', False)]}, default=_default_date_from)
    date_to = fields.Date(string='Date to', required=True, select=1, readonly=True, states={'new':[('readonly', False)]}, default=_default_date_to)
    submit_date = fields.Datetime(string="First submit date", readonly=True)
    submit_date_check = fields.Boolean(string="Match submission settings", default=False, readonly=True)

    def button_confirm(self, cr, uid, ids, context=None):
        if super(HrTimesheetSheet, self).button_confirm(cr, uid, ids, context):
            for sheet in self.browse(cr, uid, ids, context=context):
                if sheet.submit_date == False:
                    # Set the current date as submission date
                    sheet.submit_date = datetime.now()
                    if sheet.department_id.timesheet_submission_date_check:
                        # Check, regarding settings on the department, if the sheet as been submitted respecting rules
                        # compute the limit of the submission
                        date_to = datetime.strptime(sheet.date_to, '%Y-%m-%d')
                        submission_limit = date_to + relativedelta(days=+sheet.department_id.timesheet_submission_date_delay_days, hour=+sheet.department_id.timesheet_submission_date_delay_hour)
                        if datetime.today() <= submission_limit:
                            sheet.submit_date_check = True
                        
                    
        return True