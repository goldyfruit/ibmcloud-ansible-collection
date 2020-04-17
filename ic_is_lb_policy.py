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
short_description: Manage VPC load balancer policies on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - Creates a new policy to the load balancer listener.
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
  action:
    description:
      - The policy action.
    type: str
    choices: [forward, redirect, target]
  policy:
    description:
      - The user-defined name for this policy.
    type: str
    required: true
  priority:
    description:
      - Priority of the policy.
    type: int
    required: true
  rules:
    description:
      - The list of rules of this policy.
    type: list
  suboptions:
    condition:
      description:
        - The condition of the rule.
      type: str
      required: true
      choices: [contains, equals, matches_regex]
    field:
      description:
        - HTTP header field.
      type: str
    type:
      description:
        - The type of the rule.
      type: str
      required: true
      choices: [header, hostname, path]
    value
      description:
        - Value to be matched for rule condition.
      type: str
      required: true
  target:
    description:
      - Target depending the action defined.
    type: dict
    suboptions:
      id:
        description
          - Identifies a load balancer pool by ID property.
        type: str
      http_status_code:
        description
          - The http status code in the redirect response.
        type: int
      choices: [301, 302, 303, 307, 308]
      url:
        description
          - The redirect target URL.
        type: str
  state:
    description:
      - Should the resource be present or absent.
    type: str
      default: present
    choices: [present, absent]
'''

EXAMPLES = r'''
- name: Create policy
  ic_is_lb_policy:
    lb: ibmcloud-lb-baby
    listeners: 443
    policy: ibmcloud-lb-policy-baby
    action: forward
    priority: 5
    rules:
      - condition: contains
        field: MY-APP-HEADER
        type: header
        value: string
    target:
      id: r006-0c1b2e3f-d38a-4c48-9f08-b4432c9601a6

- name: Delete policy
  ic_is_lb_policy:
    lb: ibmcloud-lb-baby
    listeners: 443
    policy: ibmcloud-lb-policy-baby
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
        action=dict(
            type='str',
            required=False),
        priority=dict(
            type='int',
            required=False),
        rules=dict(
            type='list',
            options=dict(
                condition=dict(
                    type='str',
                    required=True,
                    choices=['contains', 'equals', 'matches_regex']),
                field=dict(
                    type='str',
                    required=False),
                type=dict(
                    type='str',
                    required=True,
                    choices=['header', 'hostname', 'path']),
                value=dict(
                    type='str',
                    required=True),
            ),
            required=False),
        target=dict(
            type='dict',
            options=dict(
                id=dict(
                    type='str',
                    required=False),
                http_status_code=dict(
                    type='int',
                    required=False,
                    choices=[301, 302, 303, 307, 308]),
                url=dict(
                    type='str',
                    required=False),
            ),
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
    action = module.params['action']
    priority = module.params['priority']
    rules = module.params['rules']
    target = module.params['target']
    state = module.params["state"]

    check = loadbalancer.get_lb_listener_policy(lb, listener, policy)

    if state == "absent":
        if "id" in check:
            result = loadbalancer.delete_policy(lb, listener, policy)
            if "errors" in result:
                module.fail_json(msg=result)

            payload = {"policy": policy, "listener": listener, "lb": lb,
                       "status": "deleted"}
            module.exit_json(changed=True, msg=payload)

            payload = {"policy": policy, "listener": listener, "lb": lb,
                       "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        if "id" in check:
            module.exit_json(changed=False, msg=check)

        result = loadbalancer.create_policy(
            lb=lb,
            listener=listener,
            action=action,
            name=policy,
            priority=priority,
            rules=rules,
            target=target
        )

        if "errors" in result:
            module.fail_json(msg=result)

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
