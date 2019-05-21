##################################################################################
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

import os
import json
import urllib
import logging
import requests
import unittest

import requests

from odoo import _, SUPERUSER_ID
from odoo.tests import common

from odoo.addons.muk_utils.tools.json import RecordEncoder
from odoo.addons.muk_rest.tests.common import active_authentication, RestfulCase

_path = os.path.dirname(os.path.dirname(__file__))
_logger = logging.getLogger(__name__)

class CommonTestCase(RestfulCase):
    
    def test_version(self):
        self.assertTrue(self.url_open(self.version_url))
    
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_user(self):
        client = self.authenticate()
        response = client.get(self.user_url)
        self.assertTrue(response)
        self.assertTrue(response.json().get('uid'))
    
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_userinfo(self):
        client = self.authenticate()
        response = client.get(self.userinfo_url)
        self.assertTrue(response)
        self.assertTrue(response.json().get('name'))
    
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_session(self):
        client = self.authenticate()
        response = client.get(self.session_url)
        self.assertTrue(response)
        self.assertTrue(response.json().get('login'))
    
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_call_kwargs(self):
        client = self.authenticate()
        fields_list = ['name']
        tester = self.json_prepare(self.env['res.partner'].default_get(fields_list), RecordEncoder)
        kwargs = json.dumps({'fields_list': fields_list})
        response = client.post(self.call_url, data={'model': 'res.partner', 'method': 'default_get', 'kwargs': kwargs})
        self.assertTrue(response)
        self.assertEquals(response.json(), tester)
        
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_call_args(self):
        client = self.authenticate()
        fields_list = ['name']
        tester = self.json_prepare(self.env['res.partner'].default_get(fields_list), RecordEncoder)
        args = json.dumps([fields_list])
        response = client.post(self.call_url, data={'model': 'res.partner', 'method': 'default_get', 'args': args})
        self.assertTrue(response)
        self.assertEquals(response.json(), tester)
        
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_call_ids(self):
        client = self.authenticate()
        ids = [1]
        tester = self.json_prepare(self.env['res.partner'].browse(ids).copy().name_get(), RecordEncoder)
        response = client.post(self.call_url, data={'model': 'res.partner', 'method': 'copy', 'ids': json.dumps(ids)})
        self.assertTrue(response)
        self.assertEquals(response.json()[0][1], tester[0][1])

    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_binary(self):
        client = self.authenticate()
        response = client.get(self.binary_url, data={'id': 1})
        self.assertTrue(response)
        self.assertTrue(response.json().get('content'))
        
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_binary_file(self):
        client = self.authenticate()
        response = client.get(self.binary_url, data={'id': 1, 'file_response': True})
        self.assertTrue(response)
        self.assertTrue(response.content)
        
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_reports(self):
        client = self.authenticate()
        response = client.get(self.reports_url)
        self.assertTrue(response)
        self.assertTrue(response.json())
        
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_report_single(self):
        client = self.authenticate()
        response = client.get(self.report_url, data={'report': 'base.report_irmodulereference', 'ids': json.dumps([1])})
        self.assertTrue(response)
        self.assertTrue(response.json().get('content'))
        
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_report_multiple(self):
        client = self.authenticate()
        response = client.get(self.report_url, data={'report': 'base.report_irmodulereference', 'ids': json.dumps([1, 2])})
        self.assertTrue(response)
        self.assertTrue(response.json().get('content'))
        
    @unittest.skipIf(not active_authentication, "Skipped because no authentication is available!")
    def test_report_file(self):
        client = self.authenticate()
        data = {'report': 'base.report_irmodulereference', 'ids': json.dumps([1]), 'file_response': True}
        response = client.get(self.report_url, data=data)
        self.assertTrue(response)
        self.assertTrue(response.content)
