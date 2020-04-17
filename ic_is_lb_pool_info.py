#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import loadbalancer as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_lb_pool_info
short_description: Retrieve VPC load balancer pools on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module lists all pools that belong to the load balancer.
notes:
  - The result contains a list of pools.
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
'''

EXAMPLES = r'''
- name: Retrieve pool list from load balancer
  ic_is_lb_pool_info:
    lb: ibmcloud-lb-baby

- name: Retrieve specific pool from load balancer
  ic_is_lb_info:
    lb: ibmcloud-lb-baby
    pool: ibmcloud-lb-pool-baby
'''


def run_module():
    module_args = dict(
        lb=dict(
            type='str',
            required=True),
        pool=dict(
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

    if pool:
        result = loadbalancer.get_lb_pool(lb, pool)
        if "errors" in result:
            module.fail_json(msg=result)
    else:
        result = loadbalancer.get_lb_pools(lb)
        if "errors" in result:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
