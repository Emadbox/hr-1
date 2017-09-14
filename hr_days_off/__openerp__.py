# -*- encoding: utf-8 -*-
{
    'name': 'Holidays Days Off',
    
    'description': """
This module creates the non working days in OpenERP using a generator(for the week-end) or manually.
It's use to improve the holidays requests by taking into account the bank holidays.""",
    'images': ['images/leave.png','images/periods.png'],

    'author': 'Jason PINDAT, AbAKUS it-solutions SARL',
    'website': "http://www.abakusitsolutions.eu",

    'category': 'Leaves',
    'version': '9.0.1.0',

    'depends': ['base','hr','hr_holidays'],
    
    'data': [
        'views/hr_holidays.xml',
        'views/hr_holidays_period.xml',
        'views/hr_holidays_period_category.xml',
        'views/hr_holidays_year.xml',
        'views/hr_holidays_year_wizard.xml',
        'views/menuitems.xml',
        'security/ir.model.access.csv'
    ]
}