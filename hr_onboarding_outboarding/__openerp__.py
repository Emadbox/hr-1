# -*- coding: utf-8 -*-

{
    'name': "Employee Onboarding and Outboarding",
    'version': '9.0.1.0.0',
    'depends': [
        'hr',
        'project',
    ],
    'author': "Valentin Thirion, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Human Resources',
    'description': """
This module has been developed by Valentin Thirion @ AbAKUS it-solutions""",
    'data': [
        'views/hr_employee_view.xml',
        'views/project_project_view.xml',
        'views/hr_on_out_boarding_project_view.xml',
        'security/ir.model.access.csv',
    ],
}