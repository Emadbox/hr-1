# -*- coding: utf-8 -*-
from openerp import models, fields, api

import logging

_logger = logging.getLogger(__name__)


class HrRecruitmentApplicant(models.Model):
    _inherit = 'hr.applicant'

    suspect_ids = fields.One2many('hr_duplicate_suspect', 'origin_id', ondelete='cascade')

    @api.model
    def create(self, vals):
        res = super(HrRecruitmentApplicant, self).create(vals)
        self._search_duplicates(res)
        return res

    def write(self, vals):
        result = super(HrRecruitmentApplicant, self).write(vals)
        self._search_duplicates(self)
        return result

    @api.model
    def _action_check_duplicates(self):
        for applicant in self:
            self._search_duplicates(applicant)

    @api.multi
    def _search_duplicates(self, vals):
        for suspect_rec in vals.suspect_ids:
            suspect_rec.unlink()
        corresponding_records = self.env['hr.applicant'].search(
            ['&',
             ('name', '=', vals.name),
             ('partner_name', '=', vals.partner_name),
             ('id', '!=', vals.id)
             ])

        for rec in corresponding_records:
            self.env['hr_duplicate_suspect'].create(
                {
                    'duplicate_id': rec.id,
                    'origin_id': vals.id
                })
