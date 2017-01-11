from openerp import models, fields, api
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class hr_timesheet_reminder(models.Model):
    _inherit = ['hr_timesheet_sheet.sheet']
    
    def _cron_timesheet_reminder(self, cr, uid, ids=None, context=None):
        email_template_obj = self.pool.get('mail.template')
        mail_mail_obj = self.pool.get('mail.mail')
        timesheet_obj = self.pool.get('hr_timesheet_sheet.sheet')
        employee_obj = self.pool.get('hr.employee')
        
        employee_ids = employee_obj.search(cr, uid, [('active','=',True),('remind_to_make_timesheets','=',True)])
        if employee_ids:
            for employee in employee_obj.browse(cr, uid, employee_ids):
                first_day_last_month_string= (datetime.now()-relativedelta(months=1)).strftime('%Y-%m-01 00:00:00')
                last_day_last_month_string = (datetime.strptime((datetime.now().strftime('%Y-%m-01 23:59:59')),'%Y-%m-%d %H:%M:%S')-timedelta(days=1)).strftime('%Y-%m-%d %H:%M:%S')
                timesheet_ids = timesheet_obj.search(cr, uid, [('date_from','>=',first_day_last_month_string),('date_to','<=',last_day_last_month_string),('state','in',['confirm','done']), ('employee_id', '=', employee.id)])
                if not timesheet_ids or (timesheet_ids and len(timesheet_ids)==0):
                    template_ids = email_template_obj.search(cr, uid, [('name', '=','HR Timesheet Reminder')]) 
                    if template_ids:
                        values = email_template_obj.generate_email(cr, uid, template_ids[0], employee.id)
                        msg_id = mail_mail_obj.create(cr, uid, values)
                        if msg_id:
                            mail_mail_obj.send(cr, uid, [msg_id]) 
