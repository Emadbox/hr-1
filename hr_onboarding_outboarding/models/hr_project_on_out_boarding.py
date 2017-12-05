from openerp import models, fields, api

import logging
_logger = logging.getLogger(__name__)


class hr_project_on_out_boarding(models.Model):
    _name = 'hr.project.on.out.boarding'
    _description = 'Project On/Out Boarding Templates'

    name = fields.Char('Name', required=True)
    type = fields.Selection([('onboarding', 'Onboarding'), ('outboarding', 'Outboarding')], 'Type')
    project_id = fields.Many2one('project.project', 'Project template')