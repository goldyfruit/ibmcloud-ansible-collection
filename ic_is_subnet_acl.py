#!/usr/bin/env python

# GNU General Public License v3.0+

from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import subnet as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_is_subnet_acl
short_description: Attach network ACL on subnet.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Attach network ACL on subnet on IBM Cloud.
requirements:
    - "ibmcloud-python-sdk"
options:
    subnet:
        description:
            -  Name that has to be given to the subnet to attach or detach,
                the network ACL. During the removal an UUID could be used.
        required: true
    acl:
        description:
            -  Name or ID of the network ACL to attach to the subnet.
        required: false
    state:
        description:
            - Should the resource be present or attach.
        required: false
        choices: [present, attach]
        default: present
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Attach network ACL to a subnet
- ic_is_subnet_acl:
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
            required=False),
        state=dict(
            type='str',
            default='present',
            choices=['present', 'attach'],
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    subnet = sdk.Subnet()

    name = module.params["subnet"]
    acl = module.params["acl"]

    result = subnet.attach_network_acl(subnet=name,
                                       network_acl=acl)

    if "errors" in result:
        module.fail_json(msg=result["errors"])

    module.exit_json(changed=True, msg=(result))


def main():
    run_module()


if __name__ == '__main__':
    main()
