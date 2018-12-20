{
    'name': "Timesheet submit date",
    'version': '9.0.1.0',
    'depends': [
        'hr_timesheet_sheet'
    ],
    'author': "Valentin THIRION, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'HR',
    'description': 
    """
Timesheet submit date

This modules adds a field called 'submit_date' that is set when the Sheet is first submitted.

    """,
    'data': [
            'views/hr_timesheet_sheet_view.xml',
             ],
}
