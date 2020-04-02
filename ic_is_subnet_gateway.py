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
module: ic_is_subnet_gateway
short_description: Attach or detach public gateway from subnet.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Attach or detach public gateway from subnet on IBM Cloud.
requirements:
    - "ibmcloud-python-sdk"
options:
    subnet:
        description:
            -  Name that has to be given to the subnet to attach or detach,
                the public gateway. During the removal an UUID could be used.
        required: true
    gateway:
        description:
            -  Name or ID of the public gateway to attach to the subnet.
        required: false
    state:
        description:
            - Should the resource be present, absent, attach or detach.
        required: false
        choices: [present, absent, attach, detach]
        default: present
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Attach public gateway to a subnet
- ic_is_subnet_gateway:
    subnet: ibmcloud-subnet-baby
    gateway: ibmcloud-gateway-baby

# Detach public gateway to from a subnet
- ic_is_subnet_gateway:
    subnet: ibmcloud-subnet-baby
    state: absent
'''


def run_module():
    module_args = dict(
        subnet=dict(
            type='str',
            required=True),
        gateway=dict(
            type='str',
            required=False),
        state=dict(
            type='str',
            default='present',
            choices=['absent', 'present', 'attach', 'detach'],
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    subnet = sdk.Subnet()

    name = module.params["subnet"]
    gateway = module.params["gateway"]
    state = module.params["state"]

    if state == "absent" or state == "detach":
        result = subnet.detach_public_gateway(name)

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "not_found":
                    module.fail_json(msg=result["errors"])
                else:
                    module.exit_json(changed=False, msg=(
                        "subnet {} doesn't exist")).format(name)

        module.exit_json(changed=True, msg=(
            "public gateway successfully detached from subnet {}")).format(
                name)

    else:

        result = subnet.attach_public_gateway(subnet=name,
                                              public_gateway=gateway)

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "validation_unique_failed":
                    module.fail_json(msg=result["errors"])
                else:
                    exist = subnet.get_subnet_public_gateway(name)
                    if "errors" in exist:
                        module.fail_json(msg=exist["errors"])
                    else:
                        module.exit_json(changed=False, msg=(exist))

        module.exit_json(changed=True, msg=(result))


def main():
    run_module()


if __name__ == '__main__':
    main()
