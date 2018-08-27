# -*- coding: utf-8 -*-
# (c) AbAKUS IT Solutions
import base64
import werkzeug
from odoo import http
from odoo.http import request
from odoo.addons.web.controllers.main import serialize_exception


class HrExpenseWattach(http.Controller):
    @http.route('/web/binary/download_document', type='http', auth="public")
    @serialize_exception
    def download_document(self, model, field, id, filename=None, **kwargs):
        """
        Download link for binary files
        """
        the_model = request.env[model].sudo().search([('id', '=', int(id))])
        file_content = base64.b64decode(the_model[field] or '')
        headers = werkzeug.datastructures.Headers()

        if not file_content:
            return request.not_found()
        else:
            if not filename:
                filename = '%s_%s' % (model.replace('.', '_'), id)

            headers.add('Content-Disposition', 'attachment', filename=filename)
            return request.make_response(file_content, headers)
