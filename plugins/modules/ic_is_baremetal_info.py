#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import baremetal as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_baremetal_info
short_description: Retrieve VPC Baremetal on IBM Cloud.
author: James Regis (@jamesregis)
version_added: "2.9"
description:
  - Retrieve detailed information about VPC (Virtual Provate Cloud) Baremetal
    from IBM Cloud.
notes:
  - The result contains a list of Baremetal instances.
requirements:
  - "ibmcloud-python-sdk"
options:
  instance:
    description:
      - Restrict results to instance with ID or name matching.
    type: str
'''

EXAMPLES = r'''
- name: Retrieve baremetal instances list
  ic_is_baremetal_info:

- name: Retrieve specific baremetal instance
  ic_is_baremetal_info:
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

    baremetal_instance = sdk.Baremetal()

    instance = module.params['instance']

    if instance:
        result = baremetal_instance.get_server(instance)
        if "errors" in result:
            module.fail_json(msg=result)
    else:
        result = baremetal_instance.get_servers()
        if "errors" in result:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
