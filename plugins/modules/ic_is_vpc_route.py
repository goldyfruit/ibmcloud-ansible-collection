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
module: ic_is_vpc_route
short_description: Manage VPC routes from default routing table on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module creates a new route in the VPC's default routing table.
    The route prototype object is structured in the same way as a retrieved
    route, and contains the information necessary to create the new route.
  - The request will fail if the new route will cause a loop.
requirements:
  - "ibmcloud-python-sdk"
options:
  vpc:
    description:
      - VPC name or ID.
    type: str
    required: true
  route:
    description:
      - The unique user-defined name for this route.
    type: str
    required: true
  destination:
    description:
      - The destination of the route. Must not overlap with destinations for
        existing user-defined routes within the VPC.
    type: str
  next_hop:
    description:
      - The next hop that packets will be delivered to.
    type: str
  zone:
    description:
      - The zone this route is to belong to.
    type: str
  state:
    description:
      - Should the resource be present or absent.
    type: str
    default: present
    choices: [present, absent]
'''

EXAMPLES = r'''
- name: Create route
  ic_is_vpc_route:
    vpc: ibmcloud-vpc-baby
    route: ibmcloud-route-baby
    destination: 192.168.0.0/24
    next_hop: 10.10.0.4
    zone: ibmcloud-zone-baby

- name: Delete route
  ic_is_vpc_route:
    vpc: ibmcloud-vpc-baby
    route: ibmcloud-route-baby
    state: absent
'''


def run_module():
    module_args = dict(
        vpc=dict(
            type='str',
            required=True),
        route=dict(
            type='str',
            required=True),
        destination=dict(
            type='str',
            required=False),
        next_hop=dict(
            type='str',
            required=False),
        zone=dict(
            type='str',
            required=False),
        state=dict(
            type='str',
            default='present',
            choices=['absent', 'present'],
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    sdk_vpc = sdk.Vpc()

    vpc = module.params['vpc']
    route = module.params['route']
    destination = module.params["destination"]
    next_hop = module.params['next_hop']
    zone = module.params['zone']
    state = module.params['state']

    check = sdk_vpc.get_route(vpc, route)

    if state == "absent":
        if "id" in check:
            result = sdk_vpc.delete_route(vpc, route)
            if "errors" in result:
                module.fail_json(msg=result)

            payload = {"route": route, "vpc": vpc, "status": "deleted"}
            module.exit_json(changed=True, msg=payload)

        payload = {"route": route, "vpc": vpc, "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        if "id" in check:
            module.exit_json(changed=False, msg=check)

        result = sdk_vpc.create_route(
            vpc=vpc,
            name=route,
            destination=destination,
            next_hop=next_hop,
            zone=zone
        )

        if "errors" in result:
            module.fail_json(msg=result)

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
