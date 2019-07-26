# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from odoo import fields
from odoo import models,api, http
# import json

_logger = logging.getLogger(__name__)

class JSInjector(models.Model):
    _name = "js.injector"
    _description = "JS Injector"

    name = fields.Char('Purpose', required=True, select=1)

    js = fields.Text('Javascript',required=False, index=False,store=True)
    css = fields.Text('CSS',required=False, index=False,store=True)
    xml = fields.Text('XML',required=False, index=False,store=True)

    active = fields.Boolean('Active', default=True)
    groups = fields.Many2many('res.groups', 'groups_group_js', 'group_js_id', 'group_id', track_visibility='onchange' , string='Groups')

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The name of the Javascript available , You must change your javascript name or check the javascript code may available !!!')
    ]

    @api.model
    def gen_resource_xml(self,id=0):
        return "TEST"
    
    @api.model
    def get_current_user_static(self):

        user_group_ids = self.env.user.groups_id
        user_group_js_ids = []
        for user_group in user_group_ids:
            user_group_js_ids += user_group["js_injector"]
        
        output_javascripts = []
        output_css = []
        output_xml = []

        for user_group_js_item in user_group_js_ids:
            output_javascripts.append(user_group_js_item['js'])
            output_css.append(user_group_js_item['css'])
            output_xml.append(user_group_js_item['xml'])
        
        return {
            "js": ";".join(output_javascripts),
            "css": "\n".join(output_css),
            "xml": output_xml
        }