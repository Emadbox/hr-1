# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions, _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil import rrule

import logging
_logger = logging.getLogger(__name__)

class HrHolidaysPeriod(models.Model):
    _name = 'hr.holidays.period'
    
    name = fields.Char('Name', required=True)
    year_id = fields.Many2one('hr.holiday.year', string="Year", required=True, ondelete='cascade')
    date_start = fields.Date('Start Date', required=True, lambda *a: time.strftime(DEFAULT_SERVER_DATE_FORMAT))
    date_stop = fields.Date('Stop Date', required=True, lambda *a: time.strftime(DEFAULT_SERVER_DATE_FORMAT))
    category_id = fields.Many2one('hr.holidays.period.category', string="Category")
    company_ids = field.Many2many('res.company', string="Specific Companies", , help="Apply this period only for specific companies (otherwise it is a common period)")
    active = fields.Boolean(default=True)

    @api.model
    def _check_fields(self, values):
        if values.get('date_start', self.date_start) > values.get('date_stop', self.date_stop):
            raise exceptions.ValidationError(_('Stop date must be greater or equal to start date.'))
            return False

        return True

    @api.model
    def create(self, values):
        if self._check_fields(values):
            return super(HrHolidaysPeriod, self).create(values)
        return False

    @api.one
    def write(self, values):
        if self._check_fields(values):
            return super(HrHolidaysPeriod, self).write(values)
        return False