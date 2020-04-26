#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.resource import resource_key as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_resource_key
short_description: Manage resource keys on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module creates a new resource key. Keys are credentials that are
    used to connect (bind) a service to another application.
requirements:
  - "ibmcloud-python-sdk"
options:
  key:
    description:
      - The new name of the resource key.
    type: str
    required: true
  source:
    description:
      - The short or long ID of resource instance or alias.
    type: str
  parameters:
    description:
      - Configuration options represented as key-value pairs. Service defined
        options are passed through to the target resource brokers, whereas
        platform defined options are not.
      - Must be a JSON object.
    type: str
  role:
    description:
      - The role name.
    type: str
    choices: [writer, reader, manager, administrator, operator, viewer, editor]
  state:
    description:
      - Should the resource be present or absent.
    type: str
    default: present
    choices: [present, absent]
'''

EXAMPLES = r'''
- name: Create resource key
  ic_resource_key:
    key: ibmcloud-resource-key-baby
    source: ibmcloud-resource-instance-baby
    role: writer

- name: Delete resource key
  ic_resource_key:
    key: ibmcloud-resource-key-baby
    state: absent
'''


def run_module():
    module_args = dict(
        key=dict(
            type='str',
            required=True),
        source=dict(
            type='str',
            required=False),
        parameters=dict(
            type='str',
            required=False),
        role=dict(
            type='str',
            choices=['writer', 'reader', 'manager', 'administrator',
                     'operator', 'viewer', 'editor'],
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

    resource = sdk.ResourceKey()

    key = module.params['key']
    source = module.params["source"]
    parameters = module.params["parameters"]
    role = module.params["role"]
    state = module.params["state"]

    check = resource.get_resource_key(key)

    if state == "absent":
        if "id" in check:
            result = resource.delete_key(key)
            if "errors" in result:
                module.fail_json(msg=result)

            payload = {"resource_key": key, "status": "deleted"}
            module.exit_json(changed=True, msg=payload)

        payload = {"resource_key": key, "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        if "id" in check:
            module.exit_json(changed=False, msg=check)

        result = resource.create_key(
            name=key,
            source=source,
            parameters=parameters,
            role=role
        )

        if "errors" in result:
            module.fail_json(msg=result)

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
