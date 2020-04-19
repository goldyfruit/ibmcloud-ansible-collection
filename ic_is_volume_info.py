#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import volume as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_volume_info
short_description: Retrieve VPC volumes on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module lists all volume profiles available in the region. A volume
    profile specifies the performance characteristics and pricing model for
    a volume.
notes:
  - The result contains a list of volumes.
requirements:
  - "ibmcloud-python-sdk"
options:
  volume:
    description:
      - Restrict results to volume with ID or name matching.
    type: str
'''

EXAMPLES = r'''
- name: Retrieve volume list
  ic_is_volume_info:

- name: Retrieve specific volume
  ic_is_volume_info:
    volume: ibmcloud-volume-baby
'''


def run_module():
    module_args = dict(
        volume=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    vpc_volume = sdk.Volume()

    volume = module.params['volume']

    if volume:
        result = vpc_volume.get_volume(volume)
        if "errors" in result:
            module.fail_json(msg=result)
    else:
        result = vpc_volume.get_volumes()
        if "errors" in result:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
