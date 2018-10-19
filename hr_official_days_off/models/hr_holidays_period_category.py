# -*- coding: utf-8 -*-
# (c) AbAKUS IT Solutions
from odoo import models, fields, api, exceptions, _


class HrHolidaysPeriodCategory(models.Model):
    _name = 'hr.holidays.period.category'
    
    name = fields.Char(required=True)
