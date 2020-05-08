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
module: ic_cis_baremetal_power
short_description: Manage CIS baremetal server power state on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module set a power state on a baremetal server in CIS
    (Cloud Infrastructure).
requirements:
  - "ibmcloud-python-sdk"
options:
  baremetal:
    description:
      - Baremetal name or ID.
    type: str
    required: true
  power_state:
    description:
      - Target power state.
    type: str
    choices: [on, off, reboot]
    required: true
'''

EXAMPLES = r'''
- name: Retrieve baremetal server power state
  ic_cis_baremetal_info:
    baremetal: ibmcloud-baremetal-baby
'''


def run_module():
    module_args = dict(
        baremetal=dict(
            type='str',
            required=True),
        power_state=dict(
            type='str',
            choices=['on', 'off', 'reboot'],
            required=True),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    hardware = sdk.Hardware()

    baremetal = module.params['baremetal']
    power_state = module.params['power_state']

    check = hardware.get_baremetal_power_state(baremetal)

    if check["power_state"] == power_state:
        module.exit_json(changed=False, msg=check)

    result = hardware.set_baremetal_power_state(
      baremetal=baremetal,
      power_state=power_state
    )
    if "errors" in result:
        module.fail_json(msg=result)

    module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
