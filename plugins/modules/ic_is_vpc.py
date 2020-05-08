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
module: ic_is_vpc
short_description: Manage VPC (Virtual Private Cloud) on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module  creates a new VPC from a VPC prototype object. The prototype
    object is structured in the same way as a retrieved VPC, and contains the
    information necessary to create the new VPC.
requirements:
  - "ibmcloud-python-sdk"
options:
  vpc:
    description:
      - The unique user-defined name for this VPC.
    type: str
    required: true
  resource_group:
    description:
      - The resource group to use. If unspecified, the account's default
        resource group is used.
    type: str
  address_prefix_management:
    description:
      - Indicates whether a default address prefix should be automatically
        created for each zone in this VPC. If manual, this VPC will be
        created with no default address prefixes.
    type: str
    default: auto
    choices: [auto, manual]
  classic_access:
    description:
      - Indicates whether this VPC should be connected to Classic
        Infrastructure. If true, this VPC's resources will have private
        network connectivity to the account's Classic Infrastructure resources.
      - Only one VPC, per region, may be connected in this way. This value is
        set at creation and subsequently immutable.
    type: bool
    default: false
    choices: [true, false]
  state:
    description:
      - Should the resource be present or absent.
    type: str
    default: present
    choices: [present, absent]
'''

EXAMPLES = r'''
- name: Create VPC
  ic_is_vpc:
    vpc: ibmcloud-vpc-baby

- name: Create VPC without default address prefixes
  ic_is_vpc:
    vpc: ibmcloud-vpc-baby
    address_prefix_management: manual

- name: Delete VPC
  ic_is_vpc:
    vpc: ibmcloud-vpc-baby
    state: absent
'''


def run_module():
    module_args = dict(
        vpc=dict(
            type='str',
            required=True),
        resource_group=dict(
            type='str',
            required=False),
        address_prefix_management=dict(
            type='str',
            default='auto',
            choices=['auto', 'manual'],
            required=False),
        classic_access=dict(
            type='bool',
            default=False,
            choices=[True, False],
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

    vpc = sdk.Vpc()

    name = module.params['vpc']
    resource_group = module.params["resource_group"]
    address_prefix_mgmt = module.params['address_prefix_management']
    classic_access = module.params['classic_access']
    state = module.params['state']

    check = vpc.get_vpc(name)

    if "id" in check:
        if state == "absent":
            result = vpc.delete_vpc(name)
            if "errors" in result:
                module.fail_json(msg=result)

            payload = {"vpc": name, "status": "deleted"}
            module.exit_json(changed=True, msg=payload)

        payload = {"vpc": name, "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        if "id" in check:
            module.exit_json(changed=False, msg=check)

        result = vpc.create_vpc(name=name,
                                resource_group=resource_group,
                                address_prefix_management=address_prefix_mgmt,
                                classic_access=classic_access)

        if "errors" in result:
            module.fail_json(msg=result)

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
