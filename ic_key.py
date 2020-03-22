#!/usr/bin/env python

# GNU General Public License v3.0+

from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk import key as ic


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_key
short_description: Create or delete a SSH key
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Create or delete a SSH key on IBM Cloud.
requirements:
    - "python >= 3.6"
    - "ibmcloud-python-sdk"
options:
    key:
        description:
            -  Name that has to be given to the SSH key to create or delete.
                During the removal an UUID could be used.
        required: true
    resource_group:
        description:
            -  Name or UUID of the resource group where the SSH key has to
               be created.
        required: false
    public_key:
        description:
            -  A unique public SSH key to import, encoded in PEM format.
                The key (prior to encoding) must be either 2048 or 4096
                bits long.
        required: true
    type:
        description:
            -  Indicates whether this VPC should be connected to Classic
               Infrastructure.
        required: false
        choices: [rsa]
        default: rsa
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
# Create SSH key
- ic_key:
    name: ibmcloud-key-user1
    public_key: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQChXZYzE545Uc5PU...
    resouge_group: advisory
    type: rsa

# Delete SSH key
- ic_key:
    vpc: ibmcloud-key-user1
    resouge_group: advisory
    state: absent
'''


def run_module():
    module_args = dict(
        key=dict(
            type='str',
            required=True),
        resource_group=dict(
            type='str',
            required=False),
        public_key=dict(
            type='str',
            required=True),
        type=dict(
            type='str',
            default='rsa',
            choices=["rsa"],
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

    key = ic.Key()

    if module.params["state"] == "absent":
        result = key.delete_key_by_name(module.params['key'])

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "not_found":
                    module.fail_json(msg=result["errors"])
                else:
                    module.exit_json(changed=False, msg=(
                        f"key {module.params['key']} already absent"))

        module.exit_json(changed=True, msg=(
            f"key {module.params['key']} successfully deleted"))

    else:
        result = key.create_key(name=module.params['key'],
                                resource_group=module.params["resource_group"],
                                public_key=module.params["public_key"],
                                type=module.params["type"])

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "conflict_field":
                    module.fail_json(msg=result["errors"])
                else:
                    module.exit_json(changed=False, msg=(
                        f"key {module.params['key']} already exists"))

        module.exit_json(changed=True, msg=(
            f"key {module.params['key']} successfully created"))


def main():
    run_module()


if __name__ == '__main__':
    main()
