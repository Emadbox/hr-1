# -*- coding: utf-8 -*-

{
    'name': "Advantages on Employee Contract",
    'version': '9.0.1.0.0',
    'depends': [
        'hr',
        'hr_contract',
        'hr_equipment',
        'fleet',
    ],
    'author': "Valentin Thirion, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Human Resources',
    'description': """
This module has been developed by Valentin Thirion @ AbAKUS it-solutions""",
    'data': [
        'views/hr_contract_view.xml',
        'views/hr_advantage_card_type_view.xml',
        'views/hr_advantage_card_view.xml',
        'views/hr_advantage_view.xml',
        'views/hr_employee_view.xml',
        'reports/hr_employee_contract_advantage_reports.xml',
        'security/ir.model.access.csv',
    ],
}