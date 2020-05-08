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
module: ic_is_subnet_acl
short_description: Manage VPC subnet network ACL on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - Attach network ACL on subnet on IBM Cloud.
requirements:
  - "ibmcloud-python-sdk"
options:
  subnet:
    description:
      - Subnet name or ID.
    type: str
    required: true
  acl:
    description:
      - Network ACL name or ID.
    type: str
    required: true
  state:
    description:
      - Should the resource be present or attach.
    type: str
    default: attach
    choices: [present, attach]
'''

EXAMPLES = r'''
- name: Attach network ACL to a subnet
  ic_is_subnet_acl:
    subnet: ibmcloud-subnet-baby
    acl: ibmcloud-acl-baby
'''


def run_module():
    module_args = dict(
        subnet=dict(
            type='str',
            required=True),
        acl=dict(
            type='str',
            required=True),
        state=dict(
            type='str',
            default='attach',
            choices=['present', 'attach'],
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    vsi_subnet = sdk.Subnet()

    subnet = module.params["subnet"]
    acl = module.params["acl"]

    check = vsi_subnet.get_subnet_network_acl(subnet)

    if "id" in check:
        module.exit_json(changed=False, msg=check)

    result = vsi_subnet.attach_network_acl(subnet=subnet,
                                           network_acl=acl)
    if "errors" in result:
        module.fail_json(msg=result)

    module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
