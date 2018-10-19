# -*- coding: utf-8 -*-
# (c) AbAKUS IT Solutions
from odoo import models, fields


class HrEmployeeTimesheetReminder(models.Model):
    _inherit = ['hr.employee']

    remind_to_make_timesheets = fields.Boolean(default=False,
                                               help="Sends an timesheet remind email every 4th of the month when "
                                                    "an employee forgot to complete his timesheet.")
