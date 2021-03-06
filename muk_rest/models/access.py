###################################################################################
#
#    Copyright (C) 2017 MuK IT GmbH
#
#    Odoo Proprietary License v1.0
#    
#    This software and associated files (the "Software") may only be used 
#    (executed, modified, executed after modifications) if you have
#    purchased a valid license from the authors, typically via Odoo Apps,
#    or if you have received a written agreement from the authors of the
#    Software (see the COPYRIGHT file).
#    
#    You may develop Odoo modules that use the Software as a library 
#    (typically by depending on it, importing it and using its resources),
#    but without copying any source code or material from the Software.
#    You may distribute those modules under the license of your choice,
#    provided that this license is compatible with the terms of the Odoo
#    Proprietary License (For example: LGPL, MIT, or proprietary licenses
#    similar to this one).
#    
#    It is forbidden to publish, distribute, sublicense, or sell copies of
#    the Software or modified copies of the Software.
#    
#    The above copyright notice and this permission notice must be included
#    in all copies or substantial portions of the Software.
#    
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
#    OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
#    THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#    FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
###################################################################################

import logging

from odoo import _, models, api, fields

_logger = logging.getLogger(__name__)

class Access(models.Model):
    
    _name = 'muk_rest.access'
    _description = "Access Control"

    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------

    active = fields.Boolean(
        string="Active",
        default=True)
    
    model = fields.Many2one(
        comodel_name='ir.model',
        string="Model", 
        index=True, 
        required=True, 
        ondelete='cascade',
        domain=[('transient', '=', False)])
    
    perm_read = fields.Boolean(
        string='Read Access',
        default=True)
    
    perm_write = fields.Boolean(
        string='Write Access',
        default=True)
    
    perm_create = fields.Boolean(
        string='Create Access',
        default=True)
    
    perm_unlink = fields.Boolean(
        string='Delete Access',
        default=True)
    
    oauth = fields.Many2one(
        comodel_name='muk_rest.oauth',
        string="OAuth Configuration",
        required=True, 
        ondelete='cascade')
    