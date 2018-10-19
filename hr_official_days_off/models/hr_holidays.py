# -*- coding: utf-8 -*-
# (c) AbAKUS IT Solutions
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import math
import pytz
import logging
from odoo import models, fields, api, exceptions, _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

_logger = logging.getLogger(__name__)


class HrHolidays(models.Model):
    _inherit = "hr.holidays"
    _order = 'id desc'

    date_day_from = fields.Date(string="Date From")
    date_day_to = fields.Date(string="Date To")

    day_time_from = fields.Selection([
        ('morning', 'Morning'),
        ('midday', 'Midday')
    ], string="Day Time From", default='morning')
    day_time_to = fields.Selection([
        ('midday', 'Midday'),
        ('evening', 'Evening')
    ], string="Day Time From", default='evening')

    def _check_fields(self, values):
        # Do these computation when 'removing' holidays
        if values.get('type', self.type) == 'remove':
            date_from = values.get('date_from', self.date_from)
            date_to = values.get('date_to', self.date_to)

            if date_from >= date_to:
                raise exceptions.ValidationError(_('End date must be greater to start date.'))
        return True

    def _add_needed_fields(self, values):
        type = values.get('type', self.type)
        if type == 'remove':
            if values.get('date_day_from') or values.get('day_time_from') or values.get('date_day_to') or values.get(
                    'day_time_to'):
                date_day_from = values.get('date_day_from', self.date_day_from)
                day_time_from = values.get('day_time_from', self.day_time_from)
                date_day_to = values.get('date_day_to', self.date_day_to)
                day_time_to = values.get('day_time_to', self.day_time_to)

                if date_day_from and day_time_from:
                    worktime = self.get_worktime(date_day_from, values)
                    if day_time_from == 'midday':
                        time = worktime['midday']
                    else:
                        time = worktime['morning']
                    # time = worktime['midday'] if day_time_from=='midday' else worktime['morning']
                    values['date_from'] = self.to_datetime(date_day_from + ' ' + self.float_time_convert(time) + ':00',
                                                           self._context.get('tz')).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
                else:
                    values['date_from'] = False
                if date_day_to and day_time_to:
                    worktime = self.get_worktime(date_day_to, values)
                    if day_time_to == 'midday':
                        time = worktime['midday']
                    else:
                        time = worktime['evening']
                    # time = worktime['midday'] if day_time_to=='midday' else worktime['evening']
                    values['date_to'] = self.to_datetime(date_day_to + ' ' + self.float_time_convert(time) + ':00',
                                                         self._context.get('tz')).strftime(
                        DEFAULT_SERVER_DATETIME_FORMAT)
                else:
                    values['date_to'] = False

                values['number_of_days_temp'] = self._compute_holidays_duration(values)

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
        values = self._add_needed_fields(values)
        if self._check_fields(values):
            return super(HrHolidays, self).create(values)

    @api.one
    def write(self, values):
        values = self._removeDatesForAllocation(values)
        values = self._add_needed_fields(values)
        if self._check_fields(values):
            return super(HrHolidays, self).write(values)

    @api.model
    def to_datetime(self, date_local_str, timezone_str='UTC'):
        date = datetime.strptime(date_local_str, DEFAULT_SERVER_DATETIME_FORMAT)
        timezone = pytz.timezone(timezone_str)
        return timezone.localize(date).astimezone(pytz.UTC)

    @api.model
    def _compute_holidays_duration(self, values={}):
        year_now = time.strftime('%Y')
        if not self.env['hr.holidays.year'].search([('year', '=', year_now)]):
            raise exceptions.ValidationError(_('The days off are not configured for this year(') + year_now + ')')

        user_company = self.env.user.company_id

        date_from = values.get('date_from', self.date_from)
        date_to = values.get('date_to', self.date_to)
        date_day_from = values.get('date_day_from', self.date_day_from)
        date_day_to = values.get('date_day_to', self.date_day_to)
        day_time_from = values.get('day_time_from', self.day_time_from)
        day_time_to = values.get('day_time_to', self.day_time_to)

        date_from = self.to_datetime(date_from, self._context.get('tz'))
        date_to = self.to_datetime(date_to, self._context.get('tz'))

        date_iterator = date_from
        days_holidays_count = 0
        while date_iterator <= date_to:
            if not self.env['hr.holidays.period'].search([
                '&',
                '|',
                ('company_ids', '=', False),
                ('company_ids', '=', user_company.id),
                ('date_start', '<=', date_iterator),
                ('date_stop', '>=', date_iterator)
            ]):
                days_holidays_count += 1
                if str(date_iterator.date()) == date_day_from and day_time_from == 'midday':
                    days_holidays_count -= 0.5
                if str(date_iterator.date()) == date_day_to and day_time_to == 'midday':
                    days_holidays_count -= 0.5

            date_iterator += relativedelta(days=1)
        return days_holidays_count

    @api.model
    def float_time_convert(self, float_val):
        factor = float_val < 0 and -1 or 1
        val = abs(float_val)
        hour = factor * int(math.floor(val))
        minute = int(round((val % 1) * 60))

        return format(hour, '02') + ':' + format(minute, '02')

    @api.model
    def get_worktime(self, date, values={}):

        employee_id = self.env['hr.employee'].search([('id', '=', values['employee_id'])]) if values.get(
            'employee_id') else self.employee_id
        calendar_ids = self.env['resource.calendar'].search([('company_id', '=', employee_id.company_id.id)])

        worktime = {
            'morning': 8.5,
            'midday': 13.5,
            'evening': 17.5
        }

        if len(calendar_ids) > 0:
            for attendance in calendar_ids.attendance_ids:
                if int(attendance.dayofweek) == datetime.strptime(date, DEFAULT_SERVER_DATE_FORMAT).weekday():
                    worktime['morning'] = attendance.hour_from
                    worktime['midday'] = (attendance.hour_to + attendance.hour_from) / 2
                    worktime['evening'] = attendance.hour_to
                    break

        return worktime

    def _get_number_of_days(self, date_from, date_to, employee_id):
        return self._compute_holidays_duration()

    @api.onchange('date_day_from', 'day_time_from', 'date_day_to', 'day_time_to')
    def _onchange_dates(self):
        if self.date_day_from and self.date_day_to:
            worktime = self.get_worktime(self.date_day_from)
            time_from = worktime['midday'] if self.day_time_from == 'midday' else worktime['morning']
            time_to = worktime['midday'] if self.day_time_to == 'midday' else worktime['evening']

            self.date_from = self.to_datetime(self.date_day_from + ' ' + self.float_time_convert(time_from) + ':00',
                                              self._context.get('tz'))
            self.date_to = self.to_datetime(self.date_day_to + ' ' + self.float_time_convert(time_to) + ':00',
                                            self._context.get('tz'))

            count = self._compute_holidays_duration()
            self.number_of_days_temp = count
