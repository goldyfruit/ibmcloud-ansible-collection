#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import vpc as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_vpc_route_info
short_description: Retrieve routes from VPC on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module retrieves routes in the VPC's default routing table.
    For compatibility, routes with action values other than deliver are
    omitted.
  - Each route is zone-specific and directs any packets matching its
    destination CIDR block to a next_hop IP address. The most specific route
    matching a packet's destination will be used. If multiple equally-specific
    routes exist, traffic will be distributed across them.
notes:
  - The result contains a list of routes.
requirements:
  - "ibmcloud-python-sdk"
options:
  vpc:
    description:
      - VPC name or ID
    type: str
    required: true
  route:
    description:
      - Restrict results to route with ID or name matching.
    type: str
'''

EXAMPLES = r'''
- name: Retrieve routes list
  ic_is_vpc_route_info:
    vpc: ibmcloud-vpc-baby

- name: Retrieve specific route
  ic_is_vpc_route_info:
    vpc: ibmcloud-vpc-baby
    route: ibmcloud-route-baby
'''


def run_module():
    module_args = dict(
        vpc=dict(
            type='str',
            required=True),
        route=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    sdk_vpc = sdk.Vpc()

    vpc = module.params['vpc']
    route = module.params['route']

    if route:
        result = sdk_vpc.get_route(vpc, route)
        if "errors" in result:
            module.fail_json(msg=result)
    else:
        result = sdk_vpc.get_routes(vpc)
        if "errors" in result:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
