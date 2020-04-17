#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import instance as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_instance_info
short_description: Retrieve VPC VSI on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - Retrieve detailed information about VPC (Virtual Provate Cloud) VSI
    (Virtual Server Instance) from IBM Cloud.
notes:
  - The result contains a list of VSI.
requirements:
  - "ibmcloud-python-sdk"
options:
  instance:
    description:
      - Restrict results to instance with ID or name matching.
    type: str
'''

EXAMPLES = r'''
- name: Retrieve VSI list
  ic_is_instance_info:

- name: Retrieve specific VSI
  ic_is_instance_info:
    instance: ibmcloud-vsi-baby
'''


def run_module():
    module_args = dict(
        instance=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    vsi_instance = sdk.Instance()

    instance = module.params['instance']

    if instance:
        result = vsi_instance.get_instance(instance)
        if "errors" in result:
            module.fail_json(msg=result)
    else:
        result = vsi_instance.get_instances()
        if "errors" in result:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
