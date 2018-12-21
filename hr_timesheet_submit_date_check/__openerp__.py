{
    'name': "Timesheet settings for departments and submit date check",
    'version': '9.0.1.0',
    'depends': [
        'hr_timesheet_sheet'
    ],
    'author': "Valentin THIRION, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'HR',
    'description': 
    """
Timesheet submit date check

This module adds seetings on the HR departments to specify on which interval timesheets should be made.
It also adds settings on the HR department to check the submission date.

In the Timehseets, it will auto use the interval defined on the departement related to the employee.
And it will check on the submission of the TS if it matches the settings and set a boolean accordingly.

This modules adds a field called 'submit_date' that is set when the Sheet is first submitted.

    """,
    'data': [
        'views/hr_timesheet_sheet_view.xml',
        'views/hr_department_view.xml',
    ],
}
