# -*- encoding: utf-8 -*-

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil import rrule

from openerp.osv import osv
from openerp.osv import fields
from openerp.tools.translate import _
from openerp.tools.misc import DEFAULT_SERVER_DATE_FORMAT as DT_FORMAT

class holiday_year(osv.osv):
    _name = 'training.holiday.year'
    _rec_name = 'year'
    _columns = {
        'year' : fields.char('Year', size=64, select=1, required=True),
        'period_ids' : fields.one2many('training.holiday.period', 'year_id', 'Holiday Periods'),
    }
    _defaults = {
        'year' : lambda *a: datetime.today().year,
    }
    _sql_constraints = [
        ('uniq_year', 'unique(year)', 'The year must be unique !'),
    ]

holiday_year()

class holiday_period_category(osv.osv):
    _name = 'training.holidays.category'
    _columns = {
        'name' : fields.char('Name', size=128, required=True),
    }

holiday_period_category()

class holiday_period(osv.osv):
    _name = 'training.holiday.period'
    _columns = {
        'year_id' : fields.many2one('training.holiday.year', 'Year', required=True, ondelete='cascade'),
        'name' : fields.char('Name', size=64, required=True),
        'date_start' : fields.date('Date Start', required=True),
        'date_stop' : fields.date('Date Stop', required=True),
        'active' : fields.boolean('Active'),
        'categ' : fields.many2one('training.holidays.category', 'Category'),
        'company_ids': fields.many2many('res.company', id1='period_id', id2='company_id', string='Specific Companies', help='Apply this period only for specific companies (otherwise it is a common period)')
        }
    _defaults = {
        'active' : lambda *a: 1,
        'date_start' : lambda *a: time.strftime(DT_FORMAT),
        'date_stop' : lambda *a: time.strftime(DT_FORMAT)
    }

    def _check_date_start_stop(self, cr, uid, ids, context=None):
        if not ids:
            return False
        obj = self.browse(cr, uid, ids[0], context=context)
        return obj.date_start <= obj.date_stop

    def is_in_period(self, cr, date):
        if not date:
            raise osv.except_osv(_('Error'),
                                 _('No date specified for \'Is in period\' holiday period check'))
        cr.execute("SELECT count(id) "
                   "FROM training_holiday_period "
                   "WHERE %s BETWEEN date_start AND date_stop AND active='1'",
                   (date,))
        return cr.fetchone()[0] > 0

    _constraints = [
        (_check_date_start_stop, "Please, check the start date !", ['date_start', 'date_stop']),
    ]

holiday_period()

class holiday_year_wizard(osv.osv):
    _name = 'training.holiday.year.wizard'
    _columns = {
        'year_id' : fields.many2one('training.holiday.year', 'Year')
    }

    def action_cancel(self, cr, uid, ids, context=None):
        return {'type': 'ir.actions.act_window_close'}

    def action_apply(self, cr, uid, ids, context=None):
        if not ids:
            return False
        holiday_period_obj = self.pool.get('training.holiday.period')
        categ=self.pool.get('training.holidays.category').search(cr,uid,[('name','=','Week-End')])
        if not categ:
            cat=self.pool.get('training.holidays.category').create(cr,uid,{'name': 'Week-End'})
            categ=[cat]
        wizard = self.browse(cr, uid, ids[0], context=context)

        try:
            year_start = datetime.strptime('%04s-01-01' % (wizard.year_id.year,), DT_FORMAT)
            year_end = datetime.strptime('%04s-12-31' % (wizard.year_id.year,), DT_FORMAT)
        except:
            raise osv.except_osv(_('Error!'),
                                _('The selected year name is not a valid year name'))

        # Generate holiday periods for each week-end of requested year
        # NOTE: we use ISO week number, but if the 1st saturday of the
        #       year is before the 1st thursday we force week-num to 0
        year_rule = rrule.rrule(rrule.DAILY, dtstart=year_start, until=year_end, byweekday=(rrule.SA))
        for saturday in year_rule:
            iso_year, iso_weeknum, iso_weekday = saturday.isocalendar()
            weeknum = iso_year == int(wizard.year_id.year) and iso_weeknum or 0
            holiday_period_obj.create(cr, uid, {
                'year_id' : wizard.year_id.id,
                'date_start' : saturday.strftime(DT_FORMAT),
                'date_stop' : (saturday+relativedelta(days=1)).strftime(DT_FORMAT),
                'name' : _('Week-End %02d') % (weeknum,),
                'categ': categ[0],
            }, context=context),

        return {
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'training.holiday.period',
            'type': 'ir.actions.act_window',
            'target': 'current'
        }
    
holiday_year_wizard()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
