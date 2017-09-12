# -*- coding: utf-8 -*-

from openerp import models, fields, api, exceptions, _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil import rrule

import logging
_logger = logging.getLogger(__name__)

class HrHolidaysYearWizard(models.Model):
    _name = 'hr.holidays.year.wizard'
    
    year_id = fields.Many2one('hr.holidays.year', string="Year", required=True)

    @api.model
    def _check_fields(self, values):
        if values.get('date_start', self.date_start) > values.get('date_stop', self.date_stop):
            raise exceptions.ValidationError(_('Stop date must be greater or equal to start date.'))
            return False

        return True

    @api.one
    def action_cancel(self):
        return {
            'type': 'ir.actions.act_window_close'
        }

    @api.one
    def action_apply(self):
        category_ids = self.env['hr.holidays.period.category'].search([('name', '=', 'Week-End')])
        if not category_ids:
            category = self.env['hr.holidays.period.category'].create({'name': 'Week-End'})
        else:
            category = category_ids[0]

        try:
            year_start = datetime.strptime('%04s-01-01' % (self.year_id.year), DEFAULT_SERVER_DATE_FORMAT)
            year_end = datetime.strptime('%04s-12-31' % (self.year_id.year), DEFAULT_SERVER_DATE_FORMAT)
        except:
            raise exceptions.ValidationError(_('The selected year name is not a valid year name.'))

        # Generate holiday periods for each week-end of requested year
        # NOTE: we use ISO week number, but if the 1st saturday of the
        #       year is before the 1st thursday we force week-num to 0
        year_rule = rrule.rrule(rrule.DAILY, dtstart=year_start, until=year_end, byweekday=(rrule.SA))
        for saturday in year_rule:
            iso_year, iso_weeknum, iso_weekday = saturday.isocalendar()
            weeknum = iso_year == int(self.year_id.year) and iso_weeknum or 0
            self.env['hr.holidays.period'].create({
                'year_id' : self.year_id.id,
                'date_start' : saturday.strftime(DEFAULT_SERVER_DATE_FORMAT),
                'date_stop' : (saturday+relativedelta(days=1)).strftime(DEFAULT_SERVER_DATE_FORMAT),
                'name' : _('Week-End %02d') % (weeknum,),
                'categ': category,
            })

        return {
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'hr.holidays.period',
            'type': 'ir.actions.act_window',
            'target': 'current'
        }