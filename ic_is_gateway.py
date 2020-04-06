#!/usr/bin/env python

# GNU General Public License v3.0+

from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import gateway as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_is_gateway
short_description: Create or delete public gateway.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Create or delete public gateway on IBM Cloud.
requirements:
    - "ibmcloud-python-sdk"
options:
    gateway:
        description:
            -  Name that has to be given to the public gateway to create
                or delete.
                During the removal an UUID could be used.
        required: true
    resource_group:
        description:
            -  Name or UUID of the resource group where the public gateway has
                 to be created.
        required: false
    floating_ip:
        description:
            -  Identifies a floating IP by a unique property.
        required: false
    zone:
        description:
            -  The location of the public gateway.
        required: false
    vpc:
        description:
            -  The VPC the public gateway is to be a part of.
        required: false
    state:
        description:
            - Should the resource be present or absent.
        required: false
        choices: [present, absent]
        default: present
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Create public gateway
- ic_is_gateway:
    gateway: ibmcloud-gateway-baby
    vpc: ibmcloud-vpc-baby
    zone: us-south-3

# Delete public gateway
- ic_is_gateway:
    gateway: ibmcloud-gateway-baby
    state: absent
'''


def run_module():
    module_args = dict(
        gateway=dict(
            type='str',
            required=True),
        resource_group=dict(
            type='str',
            required=False),
        floating_ip=dict(
            type='str',
            required=False),
        zone=dict(
            type='str',
            required=False),
        vpc=dict(
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

    gateway = sdk.Gateway()

    name = module.params["gateway"]
    resource_group = module.params["resource_group"]
    floating_ip = module.params["floating_ip"]
    zone = module.params["zone"]
    vpc = module.params["vpc"]
    state = module.params["state"]

    if state == "absent":
        result = gateway.delete_public_gateway(name)

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "not_found":
                    module.fail_json(msg=result["errors"])
                else:
                    module.exit_json(changed=False, msg=(
                        "public gateway {} doesn't exist")).format(name)

        module.exit_json(changed=True, msg=(
            "public gateway {} successfully deleted")).format(name)

    else:

        # Check if the public gateway exist before of possible quota issue.
        check = gateway.get_public_gateway(name)
        if "id" in check:
            module.exit_json(changed=False, msg=(check))

        result = gateway.create_public_gateway(
            name=name,
            resource_group=resource_group,
            floating_ip=floating_ip,
            zone=zone,
            vpc=vpc)

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "validation_unique_failed":
                    module.fail_json(msg=result["errors"])
                else:
                    exist = gateway.get_public_gateway(name)
                    if "errors" in exist:
                        module.fail_json(msg=exist["errors"])
                    else:
                        module.exit_json(changed=False, msg=(exist))

        module.exit_json(changed=True, msg=(result))


def main():
    run_module()


if __name__ == '__main__':
    main()
