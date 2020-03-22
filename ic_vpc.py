#!/usr/bin/env python

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_vpc
short_description: Create or delete VPC (Virtual Private Cloud)
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Create or delete VPC on IBM Cloud.
requirements:
    - "python >= 3.6"
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
- ic_vpc:
    vpc: ibmcloud-baby
    resouge_group: advisory

# Create VPC without address prefix
- ic_vpc:
    vpc: ibmcloud-baby
    resouge_group: advisory
    address_prefix_management: true

# Delete VPC
- ic_vpc:
    vpc: ibmcloud-baby
    resouge_group: advisory
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

    vpc = ic.Vpc()

    if module.params["state"] == "absent":
        result = vpc.delete_vpc_by_name(module.params['vpc'])

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "not_found":
                    module.fail_json(msg=result["errors"])
                else:
                    module.exit_json(changed=False, msg=(
                        f"vpc {module.params['vpc']} already absent"))

        module.exit_json(changed=True, msg=(
            f"vpc {module.params['vpc']} successfully deleted"))

    else:
        # pep8 trick
        addr_mgmt = module.params["address_prefix_management"]
        result = vpc.create_vpc(name=module.params['vpc'],
                                resource_group=module.params["resource_group"],
                                addr_mgmt=addr_mgmt,
                                classic_access=module.params["classic_access"])

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "validation_unique_failed":
                    module.fail_json(msg=result["errors"])
                else:
                    module.exit_json(changed=False, msg=(
                        f"vpc {module.params['vpc']} already exists"))

        module.exit_json(changed=True, msg=(
            f"vpc {module.params['vpc']} successfully created"))


def main():
    run_module()


if __name__ == '__main__':
    main()
