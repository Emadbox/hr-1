# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions, _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import dateutil.parser
import math
import pytz

import logging
_logger = logging.getLogger(__name__)

class HrHolidays(models.Model):
    _inherit = "hr.holidays"
    _order = 'id desc'

    date_day_from = fields.Date(string="Date From", readonly=True,
        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]}, track_visibility='onchange')
    date_day_to = fields.Date(string="Date To", readonly=True,
        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]}, track_visibility='onchange')

    day_time_from = fields.Selection([
        ('morning', 'Morning'),
        ('midday', 'Midday')
    ], string="Day Time From", default='morning', readonly=True,
        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]}, track_visibility='onchange')
    day_time_to = fields.Selection([
        ('midday', 'Midday'),
        ('evening', 'Evening')
    ], string="Day Time From", default='evening', readonly=True,
        states={'draft': [('readonly', False)], 'confirm': [('readonly', False)]}, track_visibility='onchange')

    def _check_fields(self, values):
        # Do these computation when 'removing' holidays
        if values.get('type', self.type) == 'remove' and (values.get('date_from', self.date_from) != False and values.get('date_to', self.date_from) != False):
            date_from = values.get('date_from', self.date_from)
            date_to = values.get('date_to', self.date_to)

            if date_from >= date_to:
                raise exceptions.ValidationError(_('End date must be greater to start date.'))
        return True

    def _add_needed_fields(self, values):
        type = values.get('type', self.type)
        if type == 'remove':
            if values.get('date_day_from') or values.get('day_time_from') or values.get('date_day_to') or values.get('day_time_to'):
                date_day_from = values.get('date_day_from', self.date_day_from)
                day_time_from = values.get('day_time_from', self.day_time_from)
                date_day_to = values.get('date_day_to', self.date_day_to)
                day_time_to = values.get('day_time_to', self.day_time_to)

                if date_day_from and day_time_from:
                    worktime = self.get_worktime(date_day_from, values)
                    if day_time_from == 'midday':
                        time = worktime['afternoon_start']
                    else:
                        time = worktime['morning_start']
                    #time = worktime['midday'] if day_time_from=='midday' else worktime['morning']
                    values['date_from'] = self.to_datetime(date_day_from + ' ' + self.float_time_convert(time) + ':00', self._context.get('tz')).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                else:
                    values['date_from'] = False
                if date_day_to and day_time_to:
                    worktime = self.get_worktime(date_day_to, values)
                    if day_time_to == 'midday':
                        time = worktime['morning_end']
                    else:
                        time = worktime['afternoon_end']
                    #time = worktime['midday'] if day_time_to=='midday' else worktime['evening']
                    values['date_to'] = self.to_datetime(date_day_to + ' ' + self.float_time_convert(time) + ':00', self._context.get('tz')).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                else:
                    values['date_to'] = False

            values['number_of_days_temp'] = self._get_number_of_days(values['date_from'], values['date_to'], self.employee_id.id)

        return values

    @api.model
    def _removeDatesForAllocation(self, values):
        if values.get('type') and values.get('type') == 'add':
            values['date_from'] = False
            values['date_to'] = False
            values['date_day_from'] = False
            values['date_day_to'] = False
            values['day_time_from'] = 'morning'
            values['day_time_to'] = 'evening'
        return values

    @api.model
    def create(self, values):
        values = self._removeDatesForAllocation(values)
        #values = self._add_needed_fields(values)
        if self._check_fields(values):
            _logger.debug("Create values: %s", values)
            return super(HrHolidays, self).create(values)

    @api.one
    def write(self, values):
        values = self._removeDatesForAllocation(values)
        #values = self._add_needed_fields(values)
        if self._check_fields(values):
            _logger.debug("Write values : %s", values)
            return super(HrHolidays, self).write(values)

    @api.model
    def to_datetime(self, date_local_str, timezone_str='UTC'):
        date = datetime.strptime(date_local_str, DEFAULT_SERVER_DATETIME_FORMAT)
        timezone = pytz.timezone(timezone_str)
        return timezone.localize(date).astimezone(pytz.UTC)

    @api.model
    def float_time_convert(self, float_val):
        factor = float_val < 0 and -1 or 1
        val = abs(float_val)
        hour = factor * int(math.floor(val))
        minute = int(round((val % 1) * 60))

        return format(hour, '02') + ':' + format(minute, '02')

    @api.model
    def get_worktime(self, date, values = {}):
        # Generic work time
        worktime = {
            'morning_start': 8.5,
            'morning_end': 12.5,
            'afternoon_start': 13.5,
            'afternoon_end': 17.5
        }

        attendance_ids = self.employee_id.resource_id.calendar_id.attendance_ids.filtered(lambda a: int(a.dayofweek == datetime.strptime(date, DEFAULT_SERVER_DATE_FORMAT).weekday()))
        _logger.debug("Attendances: %s", attendance_ids)
        if len(attendance_ids) == 2:
            worktime['morning_start'] = attendance_ids[0].hour_from if (attendance_ids[0].hour_from <= worktime['morning_start']) else worktime['morning_start']
            worktime['morning_end'] = attendance_ids[0].hour_to if (attendance_ids[0].hour_to >= worktime['morning_end']) else worktime['morning_end']
            worktime['afternoon_start'] = attendance_ids[1].hour_from if (attendance_ids[1].hour_from <= worktime['afternoon_start']) else worktime['afternoon_start']
            worktime['afternoon_end'] = attendance_ids[1].hour_to if (attendance_ids[1].hour_to >= worktime['afternoon_end']) else worktime['afternoon_end']
        elif len(attendance_ids) == 1:
            worktime['morning_start'] = attendance_ids[0].hour_from if (attendance_ids[0].hour_from <= worktime['morning_start']) else worktime['morning_start']
            worktime['afternoon_end'] = attendance_ids[0].hour_to if (attendance_ids[0].hour_to >= worktime['afternoon_end']) else worktime['afternoon_end']

        return worktime

    @api.onchange('date_day_from', 'day_time_from', 'date_day_to', 'day_time_to')
    def _onchange_dates(self):
        if self.date_day_from and self.date_day_to:
            worktime = self.get_worktime(self.date_day_from)
            time_from = worktime['afternoon_start'] if self.day_time_from == 'midday' else worktime['morning_start']
            time_to = worktime['morning_end'] if self.day_time_to == 'midday' else worktime['afternoon_end']

            self.date_from = self.to_datetime(self.date_day_from + ' ' + self.float_time_convert(time_from) + ':00', self._context.get('tz'))
            self.date_to = self.to_datetime(self.date_day_to + ' ' + self.float_time_convert(time_to) + ':00', self._context.get('tz'))
            self.number_of_days_temp = self._get_number_of_days(self.date_from, self.date_to, self.employee_id.id)
