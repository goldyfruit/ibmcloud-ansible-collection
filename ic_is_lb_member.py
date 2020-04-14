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
module: ic_is_lb_member
short_description: Create or delete pool member within a load balancer.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - Create or delete member within a pool from a load balancer on IBM Cloud.
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
    suboptions
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
    choices: [present, absent]
    default: present
'''

EXAMPLES = r'''
# Create member in a pool using instance name
- ic_is_lb_member:
    lb: ibmcloud-lb-baby
    pool: ibmcloud-lb-pool-baby
    port: 443
    target:
      instance: ibmcloud-vsi-baby

# Create member in a pool using instance IP address and a weight
- ic_is_lb_member:
    lb: ibmcloud-lb-baby
    pool: ibmcloud-lb-pool-baby
    port: 443
    weight: 90
    target:
      address: 10.12.34.11

# Delete member from a pool using instance name
- ic_is_lb_member:
    lb: ibmcloud-lb-baby
    pool: ibmcloud-lb-pool-baby
    target:
      instance: ibmcloud-vsi-baby
    state: absent

# Delete member from a pool using IP address
- ic_is_lb_member:
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

    if state == "absent":
        result = loadbalancer.delete_member(lb, pool, target)

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "not_found":
                    module.fail_json(msg=result["errors"])
                else:
                    module.exit_json(changed=False, msg=(
                        "member {} doesn't exist in pool {} for load balancer"
                        " {}".format(target, pool, lb)))

        module.exit_json(changed=True, msg=(
            "member {} successfully deleted from pool {} for load balancer"
            " {}".format(target, pool, lb)))
    else:

        data = loadbalancer.get_lb_pool_members(lb, pool)
        if "errors" in data:
            module.fail_json(msg=data)

        for member in data["members"]:
            if (
                member["port"] == port
                and member["target"]["address"] == target
              ):
                module.exit_json(changed=False, msg=member)

        result = loadbalancer.create_member(
            lb=lb,
            pool=pool,
            port=port,
            target=target,
            weight=weight,
        )

        if "errors" in result:
            module.fail_json(msg=result["errors"])

        module.exit_json(changed=True, msg=(result))


def main():
    run_module()


if __name__ == '__main__':
    main()
