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
module: ic_resource_binding_info
short_description: Retrieve available resource bindings on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - Get a list of all resource bindings.
notes:
  - The result contains a list of resource bindings.
requirements:
  - "ibmcloud-python-sdk"
options:
  binding:
    description:
      - Restrict results to key with name matching.
  type: str
'''

EXAMPLES = r'''
- name: Retrieve resource binding list
  ic_resource_binding_info:

- name: Retrieve specific resource binding
  ic_resource_binding_info:
    binding: ibmcloud-rb-baby
'''


def run_module():
    module_args = dict(
        binding=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    resource = sdk.ResourceBinding()

    binding = module.params['binding']

    if binding:
        result = resource.get_resource_binding(binding)
        if "errors" in result:
            module.fail_json(msg=result)
    else:
        result = resource.get_resource_bindings()
        if "errors" in result:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
