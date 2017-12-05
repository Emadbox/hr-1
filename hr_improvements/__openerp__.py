# -*- coding: utf-8 -*-

##############################################################################
#
#    Copyright 2014 AbAKUS it-solutions SARL
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'version': '9.0.1.0',
    'author': "Valentin THIRION, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",
    'category': 'Human resources',
    "name": "Human resources AbAKUS improvements",
    "description": """
This module adds a some improvements for the HR module.
It adds:
- a date field for the entry of the employee in the company
- info regarding the key of the buidling and badge access
- info regarding the computer of the employee
- info regarding the fuel card of the employee
- note

This module has been developed by Valentin THIRION @ AbAKUS it-solutions
 """,
    "depends": [
        "hr",
    ],
    "data": ["hr_view.xml",],
    'installable': True
}
