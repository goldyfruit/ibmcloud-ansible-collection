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
module: ic_is_instance_config_info
short_description: Retrieve initial configuration used by a VSI on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - Retrieves configuration variables used to initialize the instance,
    such as SSH keys and the Windows administrator password.
notes:
  - The result contains the VSI configuration.
requirements:
  - "ibmcloud-python-sdk"
options:
  instance:
    description:
      - VSI (Virtual Server Instance) name or ID.
    type: str
    required: true
'''

EXAMPLES = r'''
- name: Retrieve VSI configuration
  ic_is_instance_config_info:
    instance: ibmcloud-vsi-baby
'''


def run_module():
    module_args = dict(
        instance=dict(
            type='str',
            required=True),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    vsi_instance = sdk.Instance()

    instance = module.params['instance']

    result = vsi_instance.get_instance_configuration(instance)
    if "errors" in result:
        module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
