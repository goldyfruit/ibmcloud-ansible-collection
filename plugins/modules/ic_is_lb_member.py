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
module: ic_is_lb_member
short_description: Manage VPC load balancer members on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module creates a new member and adds the member to the pool.
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
      - Pool name or ID.
    type: str
    required: true
  port:
    description:
      - The port number of the application running in the server member.
    type: int
  target:
    description:
      - The pool member target. Load balancers in the network family support
        instances. Load balancers in the application family support IP
        addresses.
    type: dict
    suboptions:
      instance:
        description:
          - The identity of the instance to be targeted by the pool member
        type: str
      address:
        description:
          - The IP address to be targeted by the pool member.
        type: str
  weight:
    description:
      - Weight of the server member. This takes effect only when the load
        balancing algorithm of its belonging pool is weighted_round_robin.
    type: int
  state:
    description:
      - Should the resource be present or absent.
    type: str
    default: present
    choices: [present, absent]
'''

EXAMPLES = r'''
- name: Create member using instance name
  ic_is_lb_member:
    lb: ibmcloud-lb-baby
    pool: ibmcloud-lb-pool-baby
    port: 443
    target:
      instance: ibmcloud-vsi-baby

- name: Create member with a weight using instance IP address
  ic_is_lb_member:
    lb: ibmcloud-lb-baby
    pool: ibmcloud-lb-pool-baby
    port: 443
    weight: 90
    target:
      address: 10.12.34.11

- name: Delete member using instance name
  ic_is_lb_member:
    lb: ibmcloud-lb-baby
    pool: ibmcloud-lb-pool-baby
    target:
      instance: ibmcloud-vsi-baby
    state: absent

- name: Delete member using instance IP address
  ic_is_lb_member:
    lb: ibmcloud-lb-baby
    pool: ibmcloud-lb-pool-baby
    target:
      address: 10.12.34.11
    state: absent
'''


def run_module():
    module_args = dict(
        lb=dict(
            type='str',
            required=True),
        pool=dict(
            type='str',
            required=True),
        port=dict(
            type='int',
            required=True),
        target=dict(
            type='str',
            required=False),
        weight=dict(
            type='int',
            required=False),
        state=dict(
          type='str',
          default='present',
          choices=['absent', 'present'],
          required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    loadbalancer = sdk.Loadbalancer()

    lb = module.params['lb']
    pool = module.params['pool']
    port = module.params['port']
    target = module.params['target']
    weight = module.params['weight']
    state = module.params["state"]

    check = loadbalancer.get_lb_pool_member(lb, pool, target)

    if state == "absent":
        if "id" in check:
            if check["port"] == port:
                result = loadbalancer.delete_member(lb, pool, target)
                if "errors" in result:
                    module.fail_json(msg=result)

            payload = {"member": target, "pool": pool, "status": "deleted"}
            module.exit_json(changed=True, msg=payload)

        payload = {"member": target, "pool": pool, "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        if "id" in check:
            if check["port"] == port:
                module.exit_json(changed=False, msg=check)

        result = loadbalancer.create_member(
            lb=lb,
            pool=pool,
            port=port,
            target=target,
            weight=weight
        )

        if "errors" in result:
            module.fail_json(msg=result)

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
