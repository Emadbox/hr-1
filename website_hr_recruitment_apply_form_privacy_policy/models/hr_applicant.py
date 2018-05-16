# -*- coding: utf-8 -*-

from openerp import models, fields, api, _

import logging
_logger = logging.getLogger(__name__)


class HRApplicant(models.Model):
    _inherit = 'hr.applicant'

    website_privacy_policy_accepted = fields.Boolean(default=False, website_form_blacklisted=False)

    def init(self, cr):
        cr.execute(
            "UPDATE ir_model_fields"
            " SET website_form_blacklisted=false"
            " WHERE model='hr.applicant' AND name='website_privacy_policy_accepted'")
