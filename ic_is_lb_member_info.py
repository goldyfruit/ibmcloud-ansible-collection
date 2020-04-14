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
module: ic_is_lb_member_info
short_description: Retrieve information about members from load balancer.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Retrieve information about members from a pool within specific load
      balancers from IBM Cloud.
notes:
    - The result contains a list of members.
requirements:
    - "ibmcloud-python-sdk"
options:
    lb:
      description:
        - Load balancer name or ID.
      required: true
    pool:
      description:
        - Restrict results to pool with ID or name matching.
      required: true
    member:
      description:
        - Restrict results to member with ID matching.
      required: false
'''

EXAMPLES = r'''
# Retrieve member list specific pool
- ic_is_lb_member_info:
    lb: ibmcloud-lb-baby
    pool: ibmcloud-lb-pool-baby

# Retrieve member list and register the value
- ic_is_lb_member_info:
    lb: ibmcloud-lb-baby
    pool: ibmcloud-lb-pool-baby
  register: members

# Display members registered value
- debug:
    var: members

# Retrieve specific pool from a load balancer
- ic_is_lb_member_info:
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
    name = module.params['member']

    if name:
        result = loadbalancer.get_lb_pool_member(lb, pool, name)
        if "errors" in result:
            module.fail_json(msg=result["errors"])
    else:
        result = loadbalancer.get_lb_pool_members(lb, pool)
        if "errors" in result:
            module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
