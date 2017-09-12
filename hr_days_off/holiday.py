# -*- coding: utf-8 -*-
##################################################################################
#
# Copyright (c) 2005-2006 Axelor SARL. (http://www.axelor.com)
# and 2004-2010 Tiny SPRL (<http://tiny.be>).
#
# $Id: hr.py 4656 2006-11-24 09:58:42Z Cyp $
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU Affero General Public License as
#     published by the Free Software Foundation, either version 3 of the
#     License, or (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the GNU Affero General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
import _strptime
import openerp.pooler
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import openerp.netsvc
import openerp.tools
import math

class hr_holidays(osv.osv):
    _inherit = "hr.holidays"
    _order = 'id desc'

    _columns = {
        'name': fields.char('Description', size=64,readonly=True, states={'draft':[('readonly',False)]}),
        'user_id':fields.related('employee_id', 'user_id', type='many2one', readonly=True, states={'draft':[('readonly',False)]},relation='res.users', string='User', store=True),
        'holiday_status_id': fields.many2one("hr.holidays.status", "Leave Type", required=True, states={'draft':[('readonly',False)]}),
        'notes': fields.text('Reasons',readonly=True, states={'draft':[('readonly',False)]}),

        'date_day_from': fields.date(string="Date From"),
        'date_day_to': fields.date(string="Date To"),

        'day_time_from': fields.selection([('morning', 'Morning'), ('midday', 'Midday')], string="Day Time From", default='morning'),
        'day_time_to': fields.selection([('midday', 'Midday'), ('evening', 'Evening')], string="Day Time From", default='evening')
    }

    def _get_number_of_days(self, cr, uid, date_from, date_to):
        """Returns a float equals to the timedelta between two dates given as string."""
        holiday_proxy = self.pool.get('training.holiday.year')
        if not holiday_proxy.search(cr, uid, [('year', '=', time.strftime('%Y'))]):
            return False
        DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
        from_dt = datetime.strptime(date_from, DATETIME_FORMAT)
        to_dt = datetime.strptime(date_to, DATETIME_FORMAT)
        from_date=from_dt
        i=0
        user = self.pool.get('res.users').browse(cr, uid, uid)
        while from_dt < to_dt:
            dayoff=self.pool.get('training.holiday.period').search(cr,uid,[
                '&',
                    '|',
                    ('company_ids', '=', False),
                    ('company_ids', '=', user.company_id.id),
                ('date_start','<=',from_dt),('date_stop','>=',from_dt)
            ])
            if dayoff:
                i+=1
            from_dt = from_dt + relativedelta(days=1)
        timedelta = to_dt - from_date
        diff_day = timedelta.days + float(timedelta.seconds) / 86400
        diff_day-=i
        return diff_day


    def onchange_date(self, cr, uid, ids, date_to, date_from, values = {}):
        values['number_of_days_temp'] = 0

        if date_to and date_from:
            diff_day = self._get_number_of_days(cr, uid,date_from, date_to)
            if not diff_day:
                return {
                    'warning': {
                       'title': _('Configuration Error !'),
                       'message' : _('Please, Can you configure the week-end holidays ?'),
                    }
                }

            values['number_of_days_temp'] = math.ceil(diff_day)

        return {
            'value': values
        }

    def float_time_convert(float_val):    
        factor = float_val < 0 and -1 or 1
        val = abs(float_val)
        hour = factor * int(math.floor(val))
        minute = int(round((val % 1) * 60))
        return format(hour, '02') + ':' + format(minute, '02')

    def get_worktime(self, cr, uid, ids, date):
        calendar_ids = self.pool.get('resource.calendar').search([('company_id', '=', self.employee_id.company_id.id)])

        worktime = {
            'morning': 8.5,
            'midday': 13.5,
            'evening': 17.5
        }

        if len(calendar_ids) > 0:
            for attendance in calendar_ids[0].attendance_ids:
                if int(attendance.dayofweek) == datetime.strptime(date, DEFAULT_SERVER_DATE_FORMAT).weekday():
                    worktime['morning'] = attendance.hour_from
                    worktime['midday'] = (attendance.hour_to + attendance.hour_from) / 2
                    worktime['evening'] = attendance.hour_to
                    break

        return worktime

    def to_utc(context, date_local):
        timezone = pytz.timezone(context.get('tz') or 'UTC')
        return timezone.localize(datetime.strptime(date_local, '%Y-%m-%d %H:%M:%S')).astimezone(pytz.UTC)
        

    def onchange_date_from_inherit(self, cr, uid, ids, date_to, date_day_from, day_time_from):
        if date_day_from and day_time_from:
            worktime = self.get_worktime(cr, uid, ids, date_day_from)
            time = worktime['midday'] if day_time_from=='midday' else worktime['morning']
            date_time = to_utc(self, context, date_day_from + ' ' + float_time_convert(time) + ':00')
        else:
            date_time = False

        return self.onchange_date(cr, uid, ids, date_to, date_time, {
            'date_from': date_time
        })

    def onchange_date_to_inherit(self, cr, uid, ids, date_from, date_day_to, day_time_to):
        if date_day_to and day_time_to:
            worktime = self.get_worktime(cr, uid, ids, date_day_to)
            time = worktime['midday'] if day_time_from=='midday' else worktime['evening']
            date_time = to_utc(self, context, date_day_to + ' ' + float_time_convert(time) + ':00')
        else:
            date_time = False

        return self.onchange_date(cr, uid, ids, date_time, date_from, {
            'date_to': date_time
        })

hr_holidays()
