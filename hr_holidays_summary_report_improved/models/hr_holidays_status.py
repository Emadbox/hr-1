# -*- coding: utf-8 -*-
# (c) AbAKUS IT Solutions
from odoo import models, fields, api, exceptions, _


class HrHolidaysStatus(models.Model):
    _inherit = 'hr.holidays.status'
    _order = 'sequence, id'

    sequence = fields.Integer(default=10)
