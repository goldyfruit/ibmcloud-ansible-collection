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
module: ic_is_vpc_address_prefix
short_description: Manage VPC address pool prefixes on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module creates a new prefix from a prefix prototype object.
    The prototype object is structured in the same way as a retrieved prefix,
    and contains the information necessary to create the new prefix.
requirements:
  - "ibmcloud-python-sdk"
options:
  vpc:
    description:
      - VPC name or ID.
    type: str
    required: true
  prefix:
    description:
      - The unique user-defined name for this address prefix.
    type: str
    required: true
  cidr:
    description:
      - The CIDR block for this address prefix. The request must not overlap
        with any existing address prefixes in the VPC, or the reserved CIDR
        blocks 169.254.0.0/16 and 161.26.0.0/16.
    type: str
  is_default:
    description:
      - Indicates whether this is the default prefix for this zone in this VPC.
        If true, this prefix will become the default prefix for this zone in
        this VPC. This fails if the VPC currently has a default address prefix
        for this zone.
    type: bool
    default: false
    choices: [true, false]
  zone:
    description:
      - The zone this address prefix is to belong to.
    type: str
  state:
    description:
      - Should the resource be present or absent.
    type: str
    default: present
    choices: [present, absent]
'''

EXAMPLES = r'''
- name: Create address prefix
  ic_is_vpc_address_prefix:
    vpc: ibmcloud-vpc-baby
    prefix: ibmcloud-address-prefix-baby
    cidr: 10.0.0.0/24
    zone: ibmcloud-zone-baby

- name: Delete address prefix
  ic_is_vpc_address_prefix:
    vpc: ibmcloud-vpc-baby
    prefix: ibmcloud-address-prefix-baby
    state: absent
'''


def run_module():
    module_args = dict(
        vpc=dict(
            type='str',
            required=True),
        prefix=dict(
            type='str',
            required=True),
        cidr=dict(
            type='str',
            required=False),
        is_default=dict(
            type='bool',
            default=False,
            choices=[True, False],
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
    prefix = module.params['prefix']
    cidr = module.params["cidr"]
    is_default = module.params['is_default']
    zone = module.params['zone']
    state = module.params['state']

    check = sdk_vpc.get_address_prefix(vpc, prefix)

    if state == "absent":
        if "id" in check:
            result = sdk_vpc.delete_address_prefix(vpc, prefix)
            if "errors" in result:
                module.fail_json(msg=result)

            payload = {"prefix": prefix, "vpc": vpc, "status": "deleted"}
            module.exit_json(changed=True, msg=payload)

        payload = {"prefix": prefix, "vpc": vpc, "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        if "id" in check:
            module.exit_json(changed=False, msg=check)

        result = sdk_vpc.create_address_prefix(
            vpc=vpc,
            name=prefix,
            cidr=cidr,
            is_default=is_default,
            zone=zone
        )

        if "errors" in result:
            module.fail_json(msg=result)

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
