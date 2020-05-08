#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import loadbalancer as sdk

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_lb_member_info
short_description: Retrieve VPC members from load balancer on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module retrieves a paginated list of all members that belong to the
    pool.
notes:
  - The result contains a list of members.
requirements:
  - "ibmcloud-python-sdk"
options:
  lb:
    description:
      - Load balancer name or ID.
    type: str
    required: true
  pool:
    description:
      - Restrict results to pool with ID or name matching.
    type: str
    required: true
  member:
    description:
      - Restrict results to member with ID matching.
    type: str
'''

EXAMPLES = r'''
- name: Retrieve member list from pool
  ic_is_lb_member_info:
    lb: ibmcloud-lb-baby
    pool: ibmcloud-lb-pool-baby

- name: Retrieve specific member from pool
  ic_is_lb_member_info:
    lb: ibmcloud-lb-baby
    pool: ibmcloud-lb-pool-baby
    member: r006-177cfb48-093d-4ead-84b5-cd3e59759ee4
'''


def run_module():
    module_args = dict(
        lb=dict(
            type='str',
            required=True),
        pool=dict(
            type='str',
            required=True),
        member=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    loadbalancer = sdk.Loadbalancer()

    lb = module.params['lb']
    pool = module.params['pool']
    member = module.params['member']

    if member:
        result = loadbalancer.get_lb_pool_member(lb, pool, member)
        if "errors" in result:
            module.fail_json(msg=result)
    else:
        result = loadbalancer.get_lb_pool_members(lb, pool)
        if "errors" in result:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
