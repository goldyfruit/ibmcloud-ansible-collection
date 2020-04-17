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
module: ic_is_lb_policy_info
short_description: Retrieve VPC load balancer policy on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - Retrieves a list of all policies belonging to the load balancer listener.
notes:
  - The result contains a list of policies.
requirements:
  - "ibmcloud-python-sdk"
options:
  lb:
    description:
      - Load balancer name or ID.
    type: str
    required: true
  listener:
    description:
      - Restrict results to listener with ID or port matching.
    type: str
    required: true
  policy:
    description:
      - Restrict results to policy with name or ID matching.
    type: str
'''

EXAMPLES = r'''
- name: Retrieve policy list from specific listener (ID filtering)
  ic_is_lb_policy_info:
    lb: ibmcloud-lb-baby
    listener: r006-e503af14-7ca1-4bb6-a8eb-f25b73323041

- name: Retrieve specific policy from listener (port filtering)
  ic_is_lb_policy_info:
    lb: ibmcloud-lb-baby
    listener: 443
    policy: ibmcloud-lb-policy-baby
'''


def run_module():
    module_args = dict(
        lb=dict(
            type='str',
            required=True),
        listener=dict(
            type='str',
            required=True),
        policy=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    loadbalancer = sdk.Loadbalancer()

    lb = module.params['lb']
    listener = module.params['listener']
    policy = module.params['policy']

    if policy:
        result = loadbalancer.get_lb_listener_policy(lb, listener, policy)
        if "errors" in result:
            module.fail_json(msg=result)
    else:
        result = loadbalancer.get_lb_listener_policies(lb, listener)
        if "errors" in result:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
