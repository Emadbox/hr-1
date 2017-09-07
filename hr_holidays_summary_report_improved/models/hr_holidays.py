# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions, _

import time

import logging
_logger = logging.getLogger(__name__)
    
    
class HrHolidays(models.Model):
    _inherit = 'hr.holidays'

    date_day_from = fields.Date(string="Date From")
    date_day_to = fields.Date(string="Date To")

    day_time_from = fields.Selection([('morning', 'Morning'), ('midday', 'Midday')], string="Day Time From", default='morning')
    day_time_to = fields.Selection([('midday', 'Midday'), ('evening', 'Evening')], string="Day Time From", default='evening')

    @api.model
    def float_time_convert(self, float_val):    
        factor = float_val < 0 and -1 or 1
        val = abs(float_val)
        hour = factor * int(math.floor(val))
        minute = int(round((val % 1) * 60))
        return format(hour, '02') + ':' + format(minute, '02')

    @api.one
    @api.onchange('date_day_from', 'day_time_from')
    def onchange_date_from(self):
        calendar_ids = self.env['resource.calendar'].search([('company_id', '=', self.employee_id.company_id.id)])

        morning = 8
        midday = 13

        _logger.info('\n\na\n\n')

        if len(calendar_ids) > 0:

            _logger.info('\n\nb\n\n')

            for attendance in calendar_ids[0].attendance_ids:

                _logger.info('\n\nc\n\n')

                if int(attendance.dayofweek) == date_day_from.weekday():

                    _logger.info('\n\nd\n\n')

                    morning = attendance.hour_from
                    midday = (attendance.hour_to + attendance.hour_from) / 2
                    break

        date_from = date_day_from + ' ' + self.float_time_convert(midday if self.day_time_from=='midday' else morning)

    # @api.one
    # @api.onchange('date_day_to', 'day_time_to')
    # def onchange_date_to(self):
    #     calendar_ids = self.env['resource.calendar'].search([('company_id', '=', self.employee_id.company_id.id)])

    #     evening = 18
    #     midday = 13

    #     if len(calendar_ids) > 0:
    #         for attendance in calendar_ids[0].attendance_ids:
    #             if int(attendance.dayofweek) == date_day_to.weekday():
    #                 evening = attendance.hour_to
    #                 midday = (attendance.hour_to + attendance.hour_from) / 2
    #                 break

    #     date_to = date_day_to + ' ' + self.float_time_convert(midday if self.day_time_to=='evening' else evening)