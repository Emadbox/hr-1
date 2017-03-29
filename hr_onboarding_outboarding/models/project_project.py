from openerp import models, fields, api

import logging
_logger = logging.getLogger(__name__)


class project_onboarding(models.Model):
    _inherit = 'project.project'

    onboarding_project = fields.Boolean('Is an Onboarding Project')
    outboarding_project = fields.Boolean('Is an Outboarding Project')
    on_out_boarding_employee_id = fields.Many2one('hr.employee', 'Employee')