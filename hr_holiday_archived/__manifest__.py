{
    'name': "Archive Holidays",
    'version': '10.0.1.0.1',
    'depends': ['hr_holidays'],
    'author': "AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Human Resources',
    'description': 
    """Archive Holidays
    This modules adds a field on HR holidays to be able to archive them.
    They still are in the system but they are only visible when the users looks for 'active=False' holidays.
This module has been developed by AbAKUS it-solution.
    """,
    'data': [
        'views/holiday_view.xml',
    ],
}