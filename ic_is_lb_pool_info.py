#!/usr/bin/env python

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
short_description: Retrieve information about pools within load balancer.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Retrieve information about pools within specific load balancers from
      IBM Cloud.
notes:
    - The result contains a list of pools.
requirements:
    - "ibmcloud-python-sdk"
options:
    lb:
      description:
        - Load balancer name or ID.
      required: true
    pool:
      description:
        - Restrict results to pool with UUID or name matching.
      required: false
'''

EXAMPLES = r'''
# Retrieve pool list specific load balancer
- ic_is_lb_pool_info:
    lb: ibmcloud-lb-baby

# Retrieve pool list and register the value
- ic_is_lb_pool_info:
    lb: ibmcloud-lb-baby
  register: pools

# Display pools registered value
- debug:
    var: pools

# Retrieve specific pool from a load balancer
- ic_is_lb_info:
    lb: ibmcloud-lb-baby
    pool: ibmcloud-pool-baby
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
    name = module.params['pool']

    if name:
        result = loadbalancer.get_lb_pool(lb, name)
        if "errors" in result:
            module.fail_json(msg=result["errors"])
    else:
        result = loadbalancer.get_lb_pools(lb)
        if "errors" in result:
            module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
