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
module: ic_is_lb_policy
short_description: Manage VPC load balancer rules on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - Creates a new rule for the load balancer listener policy.
requirements:
  - "ibmcloud-python-sdk"
options:
  lb:
    description:
      - Load balancer name or ID.
    type: str
    required: true
  listeners:
    description:
      - Listener port or ID
    type: str
    required: true
  policy:
    description:
      - Policy name or ID.
    type: str
    required: true
  rule:
    description:
      - Rule ID.
    type: str
  condition:
    description:
      - The condition of the rule.
    type: str
    choices: [contains, equals, matches_regex]
  field:
    description:
      - HTTP header field.
    type: str
  type:
    description:
      - The type of the rule.
    type: str
    choices: [header, hostname, path]
  value
    description:
      - Value to be matched for rule condition.
    type: str
  state:
    description:
      - Should the resource be present or absent.
    type: str
    default: present
    choices: [present, absent]
'''

EXAMPLES = r'''
- name: Create rule
  ic_is_lb_rule:
    lb: ibmcloud-lb-baby
    listener: 443
    policy: ibmcloud-lb-policy-baby
    condition: contains
    field: MY-APP-HEADER
    type: header
    value: string

- name: Delete rule
  ic_is_lb_rule:
    lb: ibmcloud-lb-baby
    listener: r006-ac61921a-63d3-4af2-9063-2b734a817c95
    policy: ibmcloud-lb-policy-baby
    rule: 70294e14-4e61-11e8-bcf4-0242ac110004
    state: absent
'''


def run_module():
    module_args = dict(
        lb=dict(
            type='str',
            required=True),
        listener=dict(
            type='str',
            required=False),
        policy=dict(
            type='str',
            required=True),
        rule=dict(
            type='str',
            required=False),
        condition=dict(
            type='str',
            required=False,
            choices=['contains', 'equals', 'matches_regex']),
        field=dict(
            type='str',
            required=False),
        type=dict(
            type='str',
            required=False,
            choices=['header', 'hostname', 'path']),
        value=dict(
            type='str',
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
    listener = module.params['listener']
    policy = module.params['policy']
    rule = module.params['rule']
    condition = module.params['condition']
    field = module.params['field']
    type = module.params['type']
    value = module.params['value']
    state = module.params["state"]

    if not rule:
        rule = None
    check = loadbalancer.get_lb_listener_policy_rule(lb, listener, policy,
                                                     rule)
    if state == "absent":
        if "id" in check:
            result = loadbalancer.delete_rule(lb, listener, policy, rule)
            if "errors" in result:
                module.fail_json(msg=result)

            payload = {"rule": rule, "policy": policy, "listener": listener,
                       "lb": lb, "status": "deleted"}
            module.exit_json(changed=True, msg=payload)

        payload = {"rule": rule, "policy": policy, "listener": listener,
                   "lb": lb, "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        if "id" in check:
            module.exit_json(changed=False, msg=check)

        result = loadbalancer.create_rule(
            lb=lb,
            listener=listener,
            policy=policy,
            condition=condition,
            field=field,
            type=type,
            value=value
        )

        if "errors" in result:
            module.fail_json(msg=result)

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
