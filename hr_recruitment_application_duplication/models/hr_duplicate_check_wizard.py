# -*- coding: utf-8 -*-
from openerp import models, api

import logging

_logger = logging.getLogger(__name__)


class HrDuplicateCheckWizard(models.TransientModel):
    _name = "hr_duplicate_check_wizard"

    def mass_check_duplicates(self):
        applicants = self.env['hr.applicant'].search([])
        for applicant in applicants:
            applicants._search_duplicates(applicant)
        return self.env.ref('hr_recruitment_application_duplication.list_duplicate_suspects_action').read()[0]
