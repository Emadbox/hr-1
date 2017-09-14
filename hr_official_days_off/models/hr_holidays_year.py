# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions, _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil import rrule

import logging
_logger = logging.getLogger(__name__)

class HrHolidaysYear(models.Model):
    _name = 'hr.holidays.year'
    _sql_constraints = [
        ('uniq_year', 'unique(year)', 'The year must be unique.'),
    ]

    year = fields.Char(string="Year", required=True, default=lambda *a: datetime.today().year)
    period_ids = fields.One2many('hr.holidays.period', 'year_id', 'Holiday Periods')