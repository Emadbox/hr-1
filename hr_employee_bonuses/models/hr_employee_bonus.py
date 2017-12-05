from openerp import models, fields, api

import logging
_logger = logging.getLogger(__name__)


class hr_employee_bonus(models.Model):
    _name = 'hr.employee.bonus'
    _description = 'Employee bonus'

    employee_id = fields.Many2one('hr.employee', 'Employee', required=True)
    user_id = fields.Many2one('res.users', 'Creator')
    date = fields.Date('Date', required=True)
    type = fields.Selection([('gift', 'Gift'), ('bonus', 'Bonus'), ('other', 'Other')], 'Type', required=True)
    description = fields.Text('Description')
    amount = fields.Float('Amount')

    _defaults = {
        'type': 'gift',
        'user_id': lambda self,cr,uid,ctx: uid,
        'employee_id': lambda self, cr, uid, ctx=None: ctx.get('default_employee_id') if ctx is not None else False,
    }

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "%s - %s: %s" % (record.employee_id.name, record.type, record.description)))
        return result
    