{
    'name': "Attachments on timesheets",
    'version': '9.0.1.0',
    'depends': ['hr_timesheet_sheet'],
    'author': "Bernard DELHEZ, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Humain Resource',
    'description': """
    Adds a field for saving attachments inside Odoo timesheets.

	It creates a new tab in the My Current Timesheet form and allow in edit mode to add all kind of files to the timesheets.
    This module has been developed by Bernard Delhez, intern @ AbAKUS it-solutions, under the control of Valentin Thirion.
    """,
    'data': ['view/hr_timesheet_sheet_view.xml',],
}
