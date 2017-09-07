# -*- coding: utf-8 -*-
{
    'name': "HR Holidays Summary Report Improved",

    'summary': """
    """,

    'description': """
        HR Holidays Summary Report Improved
        
        This module modifies the leaves summary report :
            - Displays only 1 month
            - Shows leaves sum by category
            - Hides the unused categories
        
        This module has been developed by Jason PINDAT, intern @ AbAKUS it-solutions.
    """,

    'author': "Jason PINDAT, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",

    'category': 'Human Resources',
    'version': '9.0.1.0',

    'depends': ['hr'],

    'data': [
        'views/hr_holidays.xml',
        'views/hr_holidays_summary_dept.xml',
        'templates/report_hr_holidays_summary.xml'
    ],
}