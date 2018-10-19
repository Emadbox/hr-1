# -*- coding: utf-8 -*-
# (c) AbAKUS IT Solutions
import logging
from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class HRJob(models.Model):
    _inherit = 'hr.job'

    @api.model
    def get_default_stages(self):
        return self.env['hr.recruitment.stage'].search([('name', '=', "New")]).ids

    stage_ids = fields.Many2many('hr.recruitment.stage', 'job_stage_rel', 'job_id', 'stage_id', 'Job Stages',
                                 default=get_default_stages)
