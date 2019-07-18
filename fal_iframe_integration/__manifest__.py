# -*- coding: utf-8 -*-
# Copyright 2016, 2017 Openworx
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "Iframe integrations",
    "summary": "Allow to embed iframes apps in Odoo easily",
    "version": "12.0.0.1",
    "category": "",
    "website": "",
    "description": """
		The apps will be added to the system tray (navigation bar), next to the activies button
    """,
    'images': [
    ],
    "author": "Benoit Lavorata",
    "license": "LGPL-3",
    "installable": True,
    "depends": [
        'web',
        'mail'
    ],
    'qweb': ['static/src/xml/fal_iframe_integration.xml'],
    "data": [
        "security/ir.model.access.csv",
        'views/assets.xml',
        'views/fal_iframe_integration.xml',
    ],
}
