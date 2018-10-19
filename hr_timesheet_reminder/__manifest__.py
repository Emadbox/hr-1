# -*- coding: utf-8 -*-
# (c) AbAKUS IT Solutions
{
    'name': "Timesheet Reminder",
    'license': 'AGPL-3',
    'version': '10.0.1.0.0',
    'depends': [
        'hr_timesheet_sheet',
    ],
    'author': "Bernard DELHEZ, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Human Resource',
    'summary': "Timesheet Reminder",
    'data': [
        'views/hr_employee_view.xml',
        'data/hr_timesheet_reminder_email_template.xml',
        'data/hr_timesheet_sheet_sheet_reminder_cron.xml',
    ],
}
