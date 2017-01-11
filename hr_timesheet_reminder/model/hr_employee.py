from openerp import models, fields

class hr_employee_timesheet_reminder(models.Model):
    _inherit = ['hr.employee']
    
    remind_to_make_timesheets = fields.Boolean(string='Remind to make timesheets', default=False, help="Sends an timesheet remind email every 4th of the month when an employee forgot to complete his timesheet.")