# Copyright (c) 2016, Intel Corporation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from openstackclient.tests.functional import base


class NetworkQosRuleTypeTests(base.TestCase):
    """Functional tests for Network QoS rule type. """

    AVAILABLE_RULE_TYPES = ['dscp_marking',
                            'bandwidth_limit',
                            'minimum_bandwidth']

    def test_qos_rule_type_list(self):
        raw_output = self.openstack('network qos rule type list')
        for rule_type in self.AVAILABLE_RULE_TYPES:
            self.assertIn(rule_type, raw_output)
