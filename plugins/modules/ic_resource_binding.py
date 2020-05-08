#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.resource import resource_binding as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_resource_binding
short_description: Manage resource bindings on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module creates a new resource binding. A resource binding is the
    representation of an association between an application and a resource
    (service) instance.
  - Often, resource bindings contain the credentials (keys) that the
    application uses to communicate with the resource instance.
requirements:
  - "ibmcloud-python-sdk"
options:
  binding:
    description:
      - The name of the binding. Must be 180 characters or less and cannot
        include any special characters other than (space) - . _ :.
    type: str
    required: true
  target:
    description:
      - The CRN of application to bind to in a specific environment, e.g.
        Dallas YP, CFEE instance.
    type: str
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
- name: Create resource binding
  ic_resource_binding:
    binding: ibmcloud-resource-binding-baby
    source: ibmcloud-resource-instance-baby
    target: ibmcloud-resource-target-baby

- name: Delete resource binding
  ic_resource_binding:
    binding: ibmcloud-resource-binding-baby
    state: absent
'''


def run_module():
    module_args = dict(
        binding=dict(
            type='str',
            required=True),
        target=dict(
            type='str',
            required=False),
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

    resource = sdk.ResourceBinding()

    binding = module.params['binding']
    target = module.params["target"]
    source = module.params["source"]
    parameters = module.params["parameters"]
    role = module.params["role"]
    state = module.params["state"]

    check = resource.get_resource_binding(binding)

    if state == "absent":
        if "id" in check:
            result = resource.delete_binding(binding)
            if "errors" in result:
                module.fail_json(msg=result)

            payload = {"resource_binding": binding, "status": "deleted"}
            module.exit_json(changed=True, msg=payload)

        payload = {"resource_binding": binding, "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        if "id" in check:
            module.exit_json(changed=False, msg=check)

        result = resource.create_binding(
            name=binding,
            target=target,
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
