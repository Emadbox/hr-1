{
    'name': "HR Recruitment Applicant Duplication",
    'version': '9.0.1.0',
    'depends': [
        'hr_recruitment',
    ],
    'author': "François Wyaime @ AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu/",
    'category': 'Recruitment',
    'description': """
This module warns hr users that they are encoding some duplicate in the system.

This module has been developed by AbAKUS it-solutions""",
    'data': [
        'views/hr_applicant_view.xml',
        'views/hr_duplicate_check_wizard.xml',
        'views/hr_duplicate_suspects_view.xml',
        'security/ir.model.access.csv',
    ]
}
