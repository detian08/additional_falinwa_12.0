# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import http

class xvi_HttpEndpoints(http.Controller):

    @http.route('/xvi/resources', type='http', auth='user', methods=['GET'])
    def gen_resources(self, **kw):
        #env['js.injector'].search([''])
        return "TEST ME" + str(kw[0])