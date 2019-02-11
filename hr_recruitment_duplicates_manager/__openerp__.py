{
    'name': "HR Recruitment Duplicates Manager",
    'version': '9.0.1.0',
    'depends': [
        'hr_recruitment',
    ],
    'author': "François Wyaime @ AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu/",
    'category': 'Recruitment',
    'description': """
HR Recruitment Duplicates Manager

This module allows you tu manage possible duplicates in your applications inside the Recuitment App.
It will generate a list of possible duplicates for each new application on creation.
A new wizard will also help you to find suspected duplicates in your DB in order to clean them.

This module has been developed by AbAKUS it-solutions""",
    'data': [
        'views/hr_applicant_view.xml',
        'views/hr_duplicate_check_wizard.xml',
        'views/hr_duplicate_suspects_view.xml',

        'security/ir.model.access.csv',
    ]
}
