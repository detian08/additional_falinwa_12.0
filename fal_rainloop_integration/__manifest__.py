# -*- coding: utf-8 -*-
# Copyright 2016, 2017 Openworx
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "Cluedoo Rainloop Integration",
    "summary": "Odoo 12.0 rainloop webmail integration",
    "version": "12.0.0.1",
    "category": "Webmail",
    "website": "https://falinwa.com",
    "description": """
		Adds rainloop integration through iframe
    """,
    'images': [
    ],
    "author": "Falinwa",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        'web',
    ],
    'qweb': [
        'static/src/xml/fal_rainloop_integration.xml'
    ],
    "data": [
        'views/assets.xml'
    ],
}
