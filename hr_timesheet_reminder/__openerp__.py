{
    'name': "Timesheet Reminder",
    'version': '9.0.1.0',
    'depends': ['hr_timesheet_sheet',],
    'author': "Bernard DELHEZ, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Human Resource',
    'description': """
    Timesheet Reminder.
    
    Sends an timesheet remind email every 4th of the month when an employee forgot to complete his timesheet.
    
    It adds a boolean remind_to_make_timesheets in hr.employee. The cron check that the employee is active and that the boolean remind_to_make_timesheets is true before checking his timesheets.
    The timesheets are checked by the date of the last month and if the state are not 'confirm' or 'done' then an email is send.

    This module has been developed by Bernard Delhez, intern @ AbAKUS it-solutions.""",
    'data': ['view/hr_employee_view.xml',
             'hr_timesheet_reminder_email_template.xml',
             'hr_timesheet_sheet_sheet_reminder_cron.xml',
             ],
}
