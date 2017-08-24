# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions, _

import time

import logging
_logger = logging.getLogger(__name__)
    
    
class HrHolidaysSummaryDept(models.Model):
    _inherit = 'hr.holidays.summary.dept'

    month = fields.Selection([
        ('01', 'January'),
        ('02', 'February'),
        ('03', 'March'),
        ('04', 'April'),
        ('05', 'May'),
        ('06', 'June'),
        ('07', 'July'),
        ('08', 'August'),
        ('09', 'September'),
        ('10', 'October'),
        ('11', 'November'),
        ('12', 'December')
    ], string="Month", required=True, default=lambda *a: time.strftime('%m'))
    year = fields.Integer(string="Year", required=True, default=lambda *a: int(time.strftime('%Y')))

    @api.one
    @api.onchange('month', 'year')
    def onchange_date(self):
        if not self.month or not self.year or self.year < 0 or self.year > 9999:
            self.date_from = False
        else:
            self.date_from = str(self.year).zfill(4) + '-' + self.month + '-01'