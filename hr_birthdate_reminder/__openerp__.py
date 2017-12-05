{
    'name': "Employee birthday and entry date reminder",
    'version': '9.0.1.0',
    'depends': ['hr','hr_improvements', 'hr_contract'],
    'author': "Bernard DELHEZ, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Human Resources',
    'description': 
    """
    This module creates a scheduler that will run every day a method that looks for birthdays or entry date anniversary (at AbAKUS) of employees.
    This method works if there are several employees who have their birthday on the same day. When a match is found, a message is generated and sent by email to employees specified as managers.

    This module has been developed by Bernard Delhez, intern @ AbAKUS it-solutions, under the control of Valentin Thirion.
    """,
    'data': ['hr_employee_date_reminder_cron.xml',],
}
