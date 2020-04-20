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
module: ic_is_zone_info
short_description: Retrieve VPC zones per regions on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module lists all zones in a region. Zones represent logically-isolated
    data centers with high-bandwidth and low-latency interconnects to other
    zones in the same region.
  - Faults in a zone do not affect other zones.
notes:
  - The result contains a list of zones.
requirements:
  - "ibmcloud-python-sdk"
options:
  region:
    description:
      - Region name.
    type: str
  zone:
    description:
      - Restrict results to zone with name matching.
    type: str
'''

EXAMPLES = r'''
- name: Retrieve zone list for a specific region
  ic_is_zone_info:
    region: ibmcloud-region-baby

- name: Retrieve specific zone for a specific region
  ic_is_zone_info:
    region: ibmcloud-region-baby
    zone: ibmcloud-region-baby-1
'''


def run_module():
    module_args = dict(
        region=dict(
            type='str',
            required=True),
        zone=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    geo = sdk.Geo()

    region = module.params['region']
    zone = module.params['zone']

    if zone:
        result = geo.get_region_zone(region, zone)
        if "errors" in result:
            module.fail_json(msg=result)
    else:
        result = geo.get_region_zones(region)
        if "errors" in result:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
