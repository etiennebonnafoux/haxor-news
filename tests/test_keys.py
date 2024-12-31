# -*- coding: utf-8 -*-

# Copyright 2024 Bonnafoux Etienne. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.



import unittest
from prompt_toolkit.input.defaults import create_pipe_input

from neo_haxor_news.haxor import Haxor

class KeysTest(unittest.TestCase):

    def setUp(self):
        self.haxor = Haxor()
        self.pipe_input = create_pipe_input()
        
        self.haxor.session.app.input = self.pipe_input

    def tearDown(self):
        self.pipe_input.close()

    def test_F2(self):
        orig_paginate = self.haxor.paginate_comments

        self.pipe_input.send_text('\x1b[12~') 

        self.haxor.session.app.run_async(sleep=0)
        
        self.assertNotEqual(orig_paginate, self.haxor.paginate_comments)

    def test_F10(self):
        with self.assertRaises(EOFError):
            self.pipe_input.send_text('\x1b[21~')  
            
            self.haxor.session.app.run_async(sleep=0)
