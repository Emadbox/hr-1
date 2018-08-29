# -*- coding: utf-8 -*-
# (c) AbAKUS IT Solutions
{
    'name': "HR Bonus",
    'version': '10.0.1.0.0',
    'author': "AbAKUS it-solutions SARL",
    'license': 'AGPL-3',
    'depends': [
        'hr'
    ],
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Human Resources',
    'summary': "HR Bonus",
    'data': [
        'views/menu_buttons.xml',
        'views/bonus.xml',
        'views/employee.xml',
        'security/ir.models.access.csv',
    ],
    'application': True
}
