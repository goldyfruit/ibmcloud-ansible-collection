#!/usr/bin/env python

# GNU General Public License v3.0+

from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import key as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_is_key
short_description: Create or delete a SSH key
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Create or delete a SSH key on IBM Cloud.
requirements:
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
- ic_is_key:
    name: ibmcloud-key-user1
    public_key: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQChXZYzE545Uc5PU...
    resouge_group: advisory
    type: rsa

# Delete SSH key
- ic_is_key:
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
            required=False),
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

    key = sdk.Key()

    name = module.params['key']
    resource_group = module.params["resource_group"]
    public_key = module.params["public_key"]
    key_type = module.params["type"]
    state = module.params["state"]

    if state == "absent":
        result = key.delete_key(name)

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "not_found":
                    module.fail_json(msg=result["errors"])
                else:
                    module.exit_json(changed=False, msg=(
                        "key {} doesn't exist").format(name))

        module.exit_json(changed=True, msg=(
            "key {} successfully deleted")).format(name)

    else:
        result = key.create_key(name=name, resource_group=resource_group,
                                public_key=public_key, type=key_type)

        if "errors" in result:
            for key_name in result["errors"]:
                if key_name["code"] != "conflict_field":
                    module.fail_json(msg=result["errors"])
                else:
                    exist = key.get_key(name)
                    if "errors" in exist:
                        module.fail_json(msg=exist["errors"])
                    else:
                        module.exit_json(changed=False, msg=(exist))

        module.exit_json(changed=True, msg=(result))


def main():
    run_module()


if __name__ == '__main__':
    main()
