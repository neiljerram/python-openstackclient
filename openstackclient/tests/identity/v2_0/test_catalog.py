#   Licensed under the Apache License, Version 2.0 (the "License"); you may
#   not use this file except in compliance with the License. You may obtain
#   a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#   WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#   License for the specific language governing permissions and limitations
#   under the License.
#

import mock

from openstackclient.identity.v2_0 import catalog
from openstackclient.tests.identity.v2_0 import fakes as identity_fakes
from openstackclient.tests import utils


class TestCatalog(utils.TestCommand):

    fake_service = {
        'id': 'qwertyuiop',
        'type': 'compute',
        'name': 'supernova',
        'endpoints': [
            {
                'region': 'one',
                'publicURL': 'https://public.one.example.com',
                'internalURL': 'https://internal.one.example.com',
                'adminURL': 'https://admin.one.example.com',
            },
            {
                'region': 'two',
                'publicURL': 'https://public.two.example.com',
                'internalURL': 'https://internal.two.example.com',
                'adminURL': 'https://admin.two.example.com',
            },
            {
                'region': None,
                'publicURL': 'https://public.none.example.com',
                'internalURL': 'https://internal.none.example.com',
                'adminURL': 'https://admin.none.example.com',
            },
        ],
    }

    def setUp(self):
        super(TestCatalog, self).setUp()

        self.sc_mock = mock.MagicMock()
        self.sc_mock.service_catalog.catalog.return_value = [
            self.fake_service,
        ]

        self.auth_mock = mock.MagicMock()
        self.app.client_manager.session = self.auth_mock

        self.auth_mock.auth.get_auth_ref.return_value = self.sc_mock


class TestCatalogList(TestCatalog):

    columns = (
        'Name',
        'Type',
        'Endpoints',
    )

    def setUp(self):
        super(TestCatalogList, self).setUp()

        # Get the command object to test
        self.cmd = catalog.ListCatalog(self.app, None)

    def test_catalog_list(self):
        auth_ref = identity_fakes.fake_auth_ref(
            identity_fakes.TOKEN,
            fake_service=self.fake_service,
        )
        self.ar_mock = mock.PropertyMock(return_value=auth_ref)
        type(self.app.client_manager).auth_ref = self.ar_mock

        arglist = []
        verifylist = []
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # In base command class Lister in cliff, abstract method take_action()
        # returns a tuple containing the column names and an iterable
        # containing the data to be listed.
        columns, data = self.cmd.take_action(parsed_args)

        self.assertEqual(self.columns, columns)
        datalist = ((
            'supernova',
            'compute',
            'one\n  publicURL: https://public.one.example.com\n  '
            'internalURL: https://internal.one.example.com\n  '
            'adminURL: https://admin.one.example.com\n'
            'two\n  publicURL: https://public.two.example.com\n  '
            'internalURL: https://internal.two.example.com\n  '
            'adminURL: https://admin.two.example.com\n'
            '<none>\n  publicURL: https://public.none.example.com\n  '
            'internalURL: https://internal.none.example.com\n  '
            'adminURL: https://admin.none.example.com\n',
        ), )
        self.assertEqual(datalist, tuple(data))

    def test_catalog_list_with_endpoint_url(self):
        fake_service = {
            'id': 'qwertyuiop',
            'type': 'compute',
            'name': 'supernova',
            'endpoints': [
                {
                    'region': 'one',
                    'publicURL': 'https://public.one.example.com',
                },
                {
                    'region': 'two',
                    'publicURL': 'https://public.two.example.com',
                    'internalURL': 'https://internal.two.example.com',
                },
            ],
        }
        auth_ref = identity_fakes.fake_auth_ref(
            identity_fakes.TOKEN,
            fake_service=fake_service,
        )
        self.ar_mock = mock.PropertyMock(return_value=auth_ref)
        type(self.app.client_manager).auth_ref = self.ar_mock

        arglist = []
        verifylist = []
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # In base command class Lister in cliff, abstract method take_action()
        # returns a tuple containing the column names and an iterable
        # containing the data to be listed.
        columns, data = self.cmd.take_action(parsed_args)

        self.assertEqual(self.columns, columns)
        datalist = ((
            'supernova',
            'compute',
            'one\n  publicURL: https://public.one.example.com\n'
            'two\n  publicURL: https://public.two.example.com\n  '
            'internalURL: https://internal.two.example.com\n'
        ), )
        self.assertEqual(datalist, tuple(data))


class TestCatalogShow(TestCatalog):

    def setUp(self):
        super(TestCatalogShow, self).setUp()

        # Get the command object to test
        self.cmd = catalog.ShowCatalog(self.app, None)

    def test_catalog_show(self):
        auth_ref = identity_fakes.fake_auth_ref(
            identity_fakes.UNSCOPED_TOKEN,
            fake_service=self.fake_service,
        )
        self.ar_mock = mock.PropertyMock(return_value=auth_ref)
        type(self.app.client_manager).auth_ref = self.ar_mock

        arglist = [
            'compute',
        ]
        verifylist = [
            ('service', 'compute'),
        ]
        parsed_args = self.check_parser(self.cmd, arglist, verifylist)

        # In base command class ShowOne in cliff, abstract method take_action()
        # returns a two-part tuple with a tuple of column names and a tuple of
        # data to be shown.
        columns, data = self.cmd.take_action(parsed_args)

        collist = ('endpoints', 'id', 'name', 'type')
        self.assertEqual(collist, columns)
        datalist = (
            'one\n  publicURL: https://public.one.example.com\n  '
            'internalURL: https://internal.one.example.com\n  '
            'adminURL: https://admin.one.example.com\n'
            'two\n  publicURL: https://public.two.example.com\n  '
            'internalURL: https://internal.two.example.com\n  '
            'adminURL: https://admin.two.example.com\n'
            '<none>\n  publicURL: https://public.none.example.com\n  '
            'internalURL: https://internal.none.example.com\n  '
            'adminURL: https://admin.none.example.com\n',
            'qwertyuiop',
            'supernova',
            'compute',
        )
        self.assertEqual(datalist, data)
