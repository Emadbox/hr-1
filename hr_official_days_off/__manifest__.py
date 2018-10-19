# -*- coding: utf-8 -*-
# (c) AbAKUS IT Solutions
{
    'name': 'Holidays Official Days Off',
    'summary': "Holidays Official Days Off",
    'images': [
        'images/leave.png',
        'images/periods.png'
    ],
    'license': 'AGPL-3',
    'author': 'AbAKUS it-solutions SARL',
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Leaves',
    'version': '10.0.1.0.0',
    'depends': [
        'base',
        'hr',
        'hr_holidays',
    ],
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
