# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError

class fal_iframe_integration(models.Model):
    #_inherit = ['mail.thread', 'mail.activity.mixin']
    #_order = "sequence"

    _name = "fal.iframe_integration"
    _description = "Iframe Integration"

    name = fields.Char("Name", default="Process")
    active = fields.Boolean("Active", default=True)
    title = fields.Char("Title", default="Iframe")
    url = fields.Char("URL", default="https://")
    icon = fields.Char("Icon", default="random")
    