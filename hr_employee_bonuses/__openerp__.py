# -*- coding: utf-8 -*-

{
    'name': "Bonuses on Employee",
    'version': '9.0.1.0.0',
    'depends': [
        'hr',
    ],
    'author': "Valentin Thirion, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Human Resources',
    'description': """
HR Bonuses on Employee

This modules manages Bonuses on employees manually.
A new Menuitem is added and you can create Bonuses (date, desc, amount, type) for employees.

This module has been developed by Valentin Thirion @ AbAKUS it-solutions""",
    'data': [
        'views/hr_employee_view.xml',
        'views/hr_employee_bonuses_view.xml',
        'reports/hr_employee_bonuses_reports.xml',
        'security/ir.model.access.csv',
    ],
}