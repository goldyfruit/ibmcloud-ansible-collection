#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.resource import resource_instance as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_resource_instance_info
short_description: Retrieve resource instances on IBM Cloud.
author: James Regis (@jregis)
version_added: "2.9"
description:
  - This module retrieve information about resource instances.
notes:
  - The result contains a list of resource instances.
requirements:
  - "ibmcloud-python-sdk"
options:
  instance:
    description:
      - Restrict results to a resource instance with GUID or name matching.
'''

EXAMPLES = r'''
- name: Retrieve resource instance list
  ic_resource_instance_info:

- name: Retrieve specific resource instance
  ic_resource_instance_info
    instance: ibmcloud-ri-baby
'''


def run_module():
    module_args = dict(
        instance=dict(
            type='str',
            default=None,
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    resource_instance = sdk.ResourceInstance()

    instance = module.params['instance']

    if instance:
        result = resource_instance.get_resource_instance(instance)
        if "errors" in result:
            module.fail_json(msg=result)
    else:
        result = resource_instance.get_resource_instances()
        if "errors" in result:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
