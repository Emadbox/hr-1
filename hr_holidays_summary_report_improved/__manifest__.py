# -*- coding: utf-8 -*-
# (c) AbAKUS IT Solutions
{
    'name': "HR Holidays Summary Report Improved",
    'summary': "HR Holidays Summary Report Improved",
    'author': "AbAKUS it-solutions SARL",
    'license': 'AGPL-3',
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Human Resources',
    'version': '10.0.1.0.0',
    'depends': [
        'hr',
        'hr_holidays',
        'hr_official_days_off'
    ],
    'data': [
        'views/hr_holidays_status.xml',
        'views/hr_holidays_summary_dept.xml',
        'templates/report_hr_holidays_summary.xml'
    ],
}
