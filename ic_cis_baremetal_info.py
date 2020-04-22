#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.cis.baremetal import hardware as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_cis_baremetal_info
short_description: Retrieve CIS baremetal servers on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module lists baremetal servers from CIS (Cloud Infrastructure).
notes:
  - The result contains a list of servers.
requirements:
  - "ibmcloud-python-sdk"
options:
  baremetal:
    description:
      - Restrict results to server with ID or name matching.
    type: str
'''

EXAMPLES = r'''
- name: Retrieve baremetal server list
  ic_cis_baremetal_info:

- name: Retrieve specific baremetal server
  ic_cis_baremetal_info:
    baremetal: ibmcloud-baremetal-baby
'''


def run_module():
    module_args = dict(
        baremetal=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    hardware = sdk.Hardware()

    baremetal = module.params['baremetal']

    if baremetal:
        result = hardware.get_baremetal(baremetal)
        if "errors" in result:
            module.fail_json(msg=result)
    else:
        result = hardware.get_baremetals()
        if "errors" in result:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
