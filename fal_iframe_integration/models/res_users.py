from odoo import models,fields

class res_groups(models.Model):
    _inherit = "res.groups"

    fal_iframe_integration = fields.Many2many('fal.iframe_integration', 'groups_group_js', 'group_id', 'group_js_id', string='Iframes' )
