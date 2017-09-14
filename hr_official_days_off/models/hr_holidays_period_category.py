# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions, _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil import rrule

import logging
_logger = logging.getLogger(__name__)

class HrHolidaysPeriodCategory(models.Model):
    _name = 'hr.holidays.period.category'
    
    name = fields.Char('Name', required=True)