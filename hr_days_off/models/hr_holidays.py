# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions, _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import math
import pytz

import logging
_logger = logging.getLogger(__name__)

class HrHolidays(models.Model):
    _inherit = "hr.holidays"
    _order = 'id desc'

    name = fields.Char(readonly=True, states={'draft':[('readonly',False)]})
    user_id = fields.Many2one(readonly=True, states={'draft':[('readonly',False)]})
    holiday_status_id = fields.Many2one(states={'draft':[('readonly',False)]})
    notes = fields.Text(states={'draft':[('readonly',False)]})

    date_day_from = fields.Date(string="Date From", default=lambda *a: time.strftime(DEFAULT_SERVER_DATE_FORMAT))
    date_day_to = fields.Date(string="Date To", default=lambda *a: time.strftime(DEFAULT_SERVER_DATE_FORMAT))

    day_time_from = fields.Selection([
        ('morning', 'Morning'),
        ('midday', 'Midday')
    ], string="Day Time From", default='morning')
    day_time_to = fields.Selection([
        ('midday', 'Midday'),
        ('evening', 'Evening')
    ], string="Day Time From", default='evening')

    @api.model
    def _compute_holidays_duration(self, date_from, date_to):
        year_now = time.strftime('%Y')
        if not self.env['hr.holidays.year'].search([('year', '=', year_now)]):
            raise exceptions.ValidationError(_('The days off are not configured for this year(') + year_now + ')')
            return False

        user_company = self.env.user.company_id

        date_iterator = date_from
        days_off_count = 0
        while date_iterator < date_to:
            if self.env['hr.holidays.period'].search([
                '&',
                    '|',
                        ('company_ids', '=', False),
                        ('company_ids', '=', user_company.id),
                    ('date_start', '<=', date_iterator),
                    ('date_stop', '>=', date_iterator)
            ]):
                days_off_count += 1

            date_iterator += relativedelta(days=1)

        holidays_duration = date_to - date_from
        holidays_duration_in_days = holidays_duration.days + float(holidays_duration.seconds) / (24 * 60 * 60)
        return math.ceil(holidays_duration_in_days - days_off_count)

    @api.model
    def float_time_convert(self, float_val):    
        factor = float_val < 0 and -1 or 1
        val = abs(float_val)
        hour = factor * int(math.floor(val))
        minute = int(round((val % 1) * 60))
        return format(hour, '02') + ':' + format(minute, '02')

    @api.model
    def get_worktime(self, date):
        calendar_ids = self.env['resource.calendar'].search([('company_id', '=', self.employee_id.company_id.id)])

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

    @api.model
    def to_datetime(self, date_local_str, timezone_str='UTC'):
        date = datetime.strptime(date_local_str, DEFAULT_SERVER_DATETIME_FORMAT)
        if(timezone_str != 'UTC'):
            timezone = pytz.timezone(timezone_str)
            date = timezone.localize(timezone).astimezone(pytz.UTC)
        return date

    @api.one
    @api.onchange('date_day_from', 'day_time_from')
    def onchange_date_from_inherit(self):
        if self.date_day_from and self.day_time_from:
            worktime = self.get_worktime(self.date_day_from)
            time = worktime['midday'] if self.day_time_from=='midday' else worktime['morning']
            date_time = self.to_datetime(self.date_day_from + ' ' + self.float_time_convert(time) + ':00', self._context.get('tz'))
        else:
            date_time = False

        self.update({
            'date_from': date_time,
            'number_of_days_temp': self._compute_holidays_duration(date_time, self.to_datetime(self.date_to))
        })

    @api.one
    @api.onchange('date_day_to', 'day_time_to')
    def onchange_date_to_inherit(self):
        if self.date_day_to and self.day_time_to:
            worktime = self.get_worktime(self.date_day_to)
            time = worktime['midday'] if self.day_time_to=='midday' else worktime['evening']
            date_time = self.to_datetime(self.date_day_to + ' ' + self.float_time_convert(time) + ':00', self._context.get('tz'))
        else:
            date_time = False

        self.update({
            'date_to': date_time,
            'number_of_days_temp': self._compute_holidays_duration(self.to_datetime(self.date_to), date_time)
        })