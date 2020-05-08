#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import key as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_key
short_description: Manage VPC SSH keys on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - The prototype object is structured in the same way as a retrieved key,
    and contains the information necessary to create the new key. The public
    key value must be provided.
requirements:
  - "ibmcloud-python-sdk"
options:
  key:
    description:
      - The unique user-defined name for this key.
    type: str
    required: true
  resource_group:
    description:
      - The resource group to use. If unspecified, the account's default
        resource group is used.
    type: str
  public_key:
    description:
      - A unique public SSH key to import, encoded in PEM format. The key
        (prior to encoding) must be either 2048 or 4096 bits long.
    type: str
  type:
    description:
      - The cryptosystem used by this key
    default: rsa
    choices: [rsa]
  state:
    description:
      - Should the resource be present or absent.
    type: str
    default: present
    choices: [present, absent]
'''

EXAMPLES = r'''
- name: Create SSH key
  ic_is_key:
    key: ibmcloud-key-baby
    public_key: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQChXZYzE545Uc5PU...

- name: Delete SSH key
  ic_is_key:
    key: ibmcloud-key-baby
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

    vsi_key = sdk.Key()

    key = module.params['key']
    resource_group = module.params["resource_group"]
    public_key = module.params["public_key"]
    key_type = module.params["type"]
    state = module.params["state"]

    check = vsi_key.get_key(key)

    if state == "absent":
        if "id" in check:
            result = vsi_key.delete_key(key)
            if "errors" in result:
                module.fail_json(msg=result)

            payload = {"key": key, "status": "deleted"}
            module.exit_json(changed=True, msg=payload)

        payload = {"key": key, "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        if "id" in check:
            module.exit_json(changed=False, msg=check)

        # Not required in module_args because should not be required
        # for key deletion.
        if not public_key:
            module.fail_json(msg="public_key option is missing.")

        result = vsi_key.create_key(
            name=key,
            resource_group=resource_group,
            public_key=public_key,
            type=key_type
        )

        if "errors" in result:
            module.fail_json(msg=result)

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
