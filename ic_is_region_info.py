#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import geo as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_region_info
short_description: Retrieve VPC regions on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module lists all regions. Each region is a separate geographic area
    that contains multiple isolated zones. Resources can be provisioned into
    a one or more zones in a region. Each zone is isolated, but connected to
    other zones in the same region with low-latency and high-bandwidth links.
  - Regions represent the top-level of fault isolation available. Resources
    deployed within a single region also benefit from the low latency afforded
    by geographic proximity.
notes:
  - The result contains a list of regions.
requirements:
  - "ibmcloud-python-sdk"
options:
  region:
    description:
      - Restrict results to region with name matching.
    required: false
'''

EXAMPLES = r'''
- name: Retrieve region list
  ic_is_region_info:

- Retrieve specific region
  ic_is_region_info:
    region: ibmcloud-region-baby
'''


def run_module():
    module_args = dict(
        region=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    geo = sdk.Geo()

    region = module.params['region']

    if region:
        result = geo.get_region(region)
        if "errors" in result:
            module.fail_json(msg=result)
    else:
        result = geo.get_regions()
        if "errors" in result:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
