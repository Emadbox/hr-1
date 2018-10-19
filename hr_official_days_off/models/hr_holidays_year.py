# -*- coding: utf-8 -*-
# (c) AbAKUS IT Solutions
import logging
from datetime import datetime
from odoo import models, fields, api, exceptions, _

_logger = logging.getLogger(__name__)


class HrHolidaysYear(models.Model):
    _name = 'hr.holidays.year'
    _sql_constraints = [
        ('uniq_year', 'unique(year)', 'The year must be unique.'),
    ]

    name = fields.Char(readonly=True)
    year = fields.Char(required=True, default=lambda *a: datetime.today().year)
    period_ids = fields.One2many('hr.holidays.period', 'year_id', 'Holiday Periods')

    def _compute_fields(self, values):
        if values.get('year'):
            values['name'] = values['year']

        return values

    @api.model
    def create(self, values):
        values = self._compute_fields(values)
        return super(HrHolidaysYear, self).create(values)

    @api.one
    def write(self, values):
        values = self._compute_fields(values)
        return super(HrHolidaysYear, self).write(values)
