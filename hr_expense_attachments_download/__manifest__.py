# -*- coding: utf-8 -*-
{
    'name': "Hr Expense Attachment Download",

    'summary': """
        Download all expense report attachments.
    """,

    'description': """
        This module adds an action button to an Expense Report view allowing to export all attachments referenced into
        a single zip archive.
    """,

    'author': "AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",

    'category': 'HR',
    'version': '0.1',

    'depends': [
        'base',
        'hr_expense'
    ],
    'data': [
        'views/views.xml',
    ],
}