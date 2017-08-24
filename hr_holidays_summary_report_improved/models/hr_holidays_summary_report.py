# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions, _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

import time
import calendar

import logging
_logger = logging.getLogger(__name__)
    
    
class HrHolidaysSummaryReport(models.AbstractModel):
    _inherit = 'report.hr_holidays.report_holidayssummary'

    def _get_header_info(self, start_date, holiday_type):

        values = super(HrHolidaysSummaryReport, self)._get_header_info(start_date, holiday_type)

        start_dt = datetime.strptime(start_date, DEFAULT_SERVER_DATE_FORMAT)

        last_day = calendar.monthrange(int(start_dt.strftime('%Y')), int(start_dt.strftime('%m')))[1]

        values['end_date'] = start_dt.strftime('%Y-%m') + '-' + str(last_day)

        return values

    def _get_leaves_summary_old(self, cr, uid, ids, start_date, empid, holiday_type, context=None):
        res = []
        self.status_sum_emp = {}
        count = 0
        start_date = datetime.strptime(start_date, DEFAULT_SERVER_DATE_FORMAT)
        start_date = fields.datetime.context_timestamp(cr, uid, start_date, context=context).date()
        end_date = start_date + relativedelta(days=59)
        for index in range(0, 60):
            current = start_date + timedelta(index)
            res.append({'day': current.day, 'color': ''})
            if current.strftime('%a') == 'Sat' or current.strftime('%a') == 'Sun':
                res[index]['color'] = '#ababab'
        # count and get leave summary details.
        holidays_obj = self.pool['hr.holidays']
        holiday_type = ['confirm','validate'] if holiday_type == 'both' else ['confirm'] if holiday_type == 'Confirmed' else ['validate']
        holidays_ids = holidays_obj.search(cr, uid, [('employee_id', '=', empid), ('state', 'in', holiday_type), ('type', '=', 'remove'), ('date_from', '<=', str(end_date)), ('date_to', '>=', str(start_date))], context=context)
        for holiday in holidays_obj.browse(cr, uid, holidays_ids, context=context):
            # Convert date to user timezone, otherwise the report will not be consistent with the
            # value displayed in the interface.
            date_from = datetime.strptime(holiday.date_from, DEFAULT_SERVER_DATETIME_FORMAT)
            date_from = fields.datetime.context_timestamp(cr, uid, date_from, context=context).date()
            date_to = datetime.strptime(holiday.date_to, DEFAULT_SERVER_DATETIME_FORMAT)
            date_to = fields.datetime.context_timestamp(cr, uid, date_to, context=context).date()
            for index in range(0, ((date_to - date_from).days + 1)):
                if date_from >= start_date and date_from <= end_date:
                    res[(date_from-start_date).days]['color'] = holiday.holiday_status_id.color_name
                    self.status_sum_emp.setdefault(holiday.holiday_status_id, 0)
                    self.status_sum_emp[holiday.holiday_status_id] += 1
                    count+=1
                date_from += timedelta(1)
        self.sum = count
        return res

    def _get_data_from_report(self, cr, uid, ids, data, context=None):
        res = []
        self.status_sum = {}
        emp_obj = self.pool['hr.employee']
        department_obj = self.pool['hr.department']
        if 'depts' in data:
            for department in department_obj.browse(cr, uid, data['depts'], context=context):
                res.append({'dept' : department.name, 'data': [], 'color': self._get_day(data['date_from'])})
                employee_ids = emp_obj.search(cr, uid, [('department_id', '=', department.id)], context=context)
                employees = emp_obj.browse(cr, uid, employee_ids, context=context)
                for emp in employees:
                    res[len(res)-1]['data'].append({
                        'emp': emp.name,
                        'display': self._get_leaves_summary(cr, uid, ids, data['date_from'], emp.id, data['holiday_type'], context=context),
                        'sum': self.sum
                    })
                    for status in self.status_sum_emp:
                        self.status_sum.setdefault(status, 0)
                        self.status_sum[status] += self.status_sum_emp[status]
        elif 'emp' in data:
            employees = emp_obj.browse(cr, uid, data['emp'], context=context)
            res.append({'data':[]})
            for emp in employees:
                res[0]['data'].append({
                    'emp': emp.name,
                    'display': self._get_leaves_summary(cr, uid, ids, data['date_from'], emp.id, data['holiday_type'], context=context),
                    'sum': self.sum
                })
                for status in self.status_sum_emp:
                    self.status_sum.setdefault(status, 0)
                    self.status_sum[status] += self.status_sum_emp[status]
        return res

    def _get_holidays_status(self, cr, uid, ids, context=None):
        res = []
        for status in self.status_sum:
            res.append({'color': status.color_name, 'name': status.name})
        return res