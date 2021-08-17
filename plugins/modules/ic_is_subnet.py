#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import subnet as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_subnet
short_description: Manage VPC subnets on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module creates a new subnet from a subnet prototype object.
    The prototype object is structured in the same way as a retrieved subnet,
    and contains the information necessary to create the new subnet. For this
    request to succeed, the prototype's CIDR block must not overlap with an
    existing subnet in the VPC.
requirements:
  - "ibmcloud-python-sdk"
options:
  subnet:
    description:
      - Subnet name or ID.
    type: str
    required: true
  resource_group:
    description:
      - The resource group to use. If unspecified, the account's default
        resource group is used.
    type: str
  ip_version:
    description:
      - The IP version(s) supported by this subnet; if unspecified, ipv4 is
        used.
    type: str
    choices: [both, ipv4, ipv6]
  ipv4_cidr_block:
    description:
      - The IPv4 range of the subnet, expressed in CIDR format. The prefix
        length of the subnet's CIDR must be between 8 and 29. The IPv4 range
        of the subnet's CIDR must fall within an existing address prefix in
        the VPC. The subnet will be created in the zone of the address prefix
        that contains the IPv4 CIDR. If zone is specified, it must match the
        zone of the address prefix that contains the subnet's IPv4 CIDR.
    type: str
  network_acl:
    description:
      - The network ACL to use for this subnet; if unspecified, the default
        network ACL for the VPC is used.
    type: str
  public_gateway:
    description:
      - The public gateway to handle internet bound traffic for this subnet.
    type: str
  routing_table:
    description:
      - The routing table to use for this subnet; if unspecified, the default
        routing table for the VPC is used.
    type: str
  total_ipv4_address_count:
    description:
      - The total number of IPv4 addresses required. Must be a power of 2.
        The VPC must have a default address prefix in the specified zone, and
        that prefix must have a free CIDR range with at least this number of
        addresses.
    type: int
  zone:
    description:
      - The zone the subnet is to reside in.
    type: str
  vpc:
    description:
      - The VPC the subnet is to be a part of.
    type: str
    required: true
  state:
    description:
      - Should the resource be present or absent.
    type: str
    default: present
    choices: [present, absent]
'''

EXAMPLES = r'''
- name: Create subnet
  ic_is_subnet:
    subnet: ibmcloud-subnet-baby
    vpc: ibmcloud-vpc-baby
    ipv4_cidr_block: 192.168.10.0/24

- name: Delete subnet
  ic_is_subnet:
    subnet: ibmcloud-volume-baby
    vpc: ibmcloud-vpc-baby
    state: absent
'''


def run_module():
    module_args = dict(
        subnet=dict(
            type='str',
            required=True),
        resource_group=dict(
            type='str',
            required=False),
        ip_version=dict(
            type='str',
            choices=['both', 'ipv4', 'ipv6'],
            required=False),
        ipv4_cidr_block=dict(
            type='str',
            required=False),
        network_acl=dict(
            type='str',
            required=False),
        public_gateway=dict(
            type='str',
            required=False),
        routing_table=dict(
            type='str',
            required=False),
        total_ipv4_address_count=dict(
            type='int',
            required=False),
        zone=dict(
            type='str',
            required=False),
        vpc=dict(
            type='str',
            required=True),
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

    vsi_subnet = sdk.Subnet()

    subnet = module.params["subnet"]
    resource_group = module.params["resource_group"]
    ip_version = module.params["ip_version"]
    ipv4_cidr_block = module.params["ipv4_cidr_block"]
    network_acl = module.params["network_acl"]
    public_gateway = module.params["public_gateway"]
    total_ipv4_address_count = module.params["total_ipv4_address_count"]
    zone = module.params["zone"]
    vpc = module.params["vpc"]
    state = module.params["state"]

    check = vsi_subnet.get_subnet(subnet)

    if state == "absent":
        if "id" in check:
            result = vsi_subnet.delete_subnet(subnet)
            if "errors" in result:
                module.fail_json(msg=result)

            payload = {"subnet": subnet, "status": "deleted"}
            module.exit_json(changed=True, msg=payload)

        payload = {"subnet": subnet, "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        if "id" in check:
            module.exit_json(changed=False, msg=check)

        if total_ipv4_address_count and not zone:
            module.fail_json(msg="total_ipv4_address_count needs zone option")

        result = vsi_subnet.create_subnet(
            name=subnet,
            resource_group=resource_group,
            ip_version=ip_version,
            ipv4_cidr_block=ipv4_cidr_block,
            network_acl=network_acl,
            public_gateway=public_gateway,
            total_ipv4_address_count=total_ipv4_address_count,
            zone=zone,
            vpc=vpc
        )

        if "errors" in result:
            module.fail_json(msg=result)

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
