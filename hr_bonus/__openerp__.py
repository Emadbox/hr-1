{
    'name': "HR Bonus",
    'version': '9.0.1.0.0',
    'depends': [
        'hr'
        # 'project_service_desk'
    ],
    'author': "Jason PINDAT @ AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Human Resources',
    'description': """
        HR Bonus

        Adds a system to manages bonuses

        This module has been developed by Jason PINDAT @ AbAKUS it-solutions.
    """,
    'data': [
        'views/menu_buttons.xml',
        'views/bonus.xml',
        'views/employee.xml',
        'security/ir.model.access.csv'
    ],
}
