{
    'name': "Hr Expense Attachment Download",
    'version': '0.1',
    'depends': [
        'base',
        'hr_expense'
    ],
    'author': "AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'HR',
    'description':
"""
This module adds an action button to an Expense Report view allowing to export all attachments referenced into
a single zip archive.
This module has been developed by AbAKUS it-solutions
""",
    'data': [
        'views/hr_expense_attachments_download_views.xml',
    ],
}