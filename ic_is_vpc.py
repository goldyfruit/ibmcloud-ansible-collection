#!/usr/bin/env python

# GNU General Public License v3.0+

from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import vpc as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_is_vpc
short_description: Create or delete VPC (Virtual Private Cloud).
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Create or delete VPC (Virtual Private Cloud) on IBM Cloud.
requirements:
    - "ibmcloud-python-sdk"
options:
    vpc:
        description:
            -  Name that has to be given to the VPC to create or delete.
                During the removal an UUID could be used.
        required: true
    resource_group:
        description:
            -  Name or UUID of the resource group where the VPC has to
               be created.
        required: false
    address_prefix_management:
        description:
            -  Indicates whether a default address prefix should be
               automatically created for each zone in this VPC.
        required: false
        choices: [auto, manual]
        default: auto
    classic_access:
        description:
            -  Indicates whether this VPC should be connected to Classic
               Infrastructure.
        required: false
        choices: [true, false]
        default: false
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
# Create VPC
- ic_is_vpc:
    vpc: ibmcloud-vpc-baby
    resource_group: ibmcloud-rg-baby

# Create VPC without address prefix
- ic_is_vpc:
    vpc: ibmcloud-vpc-baby
    resource_group: ibmcloud-rg-baby
    address_prefix_management: true

# Delete VPC
- ic_is_vpc:
    vpc: ibmcloud-vpc-baby
    resource_group: ibmcloud-rg-baby
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
            default='false',
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

    if state == "absent":
        result = vpc.delete_vpc(name)

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "not_found":
                    module.fail_json(msg=result["errors"])
                else:
                    module.exit_json(changed=False, msg=(
                        "vpc {} doesn't exist")).format(name)

        module.exit_json(changed=True, msg=(
            "vpc {} successfully deleted")).format(name)

    else:
        result = vpc.create_vpc(name=name,
                                resource_group=resource_group,
                                address_prefix_management=address_prefix_mgmt,
                                classic_access=classic_access)

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "validation_unique_failed":
                    module.fail_json(msg=result["errors"])
                else:
                    exist = vpc.get_vpc(name)
                    if "errors" in exist:
                        module.fail_json(msg=exist["errors"])
                    else:
                        module.exit_json(changed=False, msg=(exist))

        module.exit_json(changed=True, msg=(result))


def main():
    run_module()


if __name__ == '__main__':
    main()
