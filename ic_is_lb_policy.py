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
module: ic_is_lb_policy
short_description: Create or delete policy within a load balancer.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - Create or delete policy within a listener from a load balancer
    on IBM Cloud.
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
      - Listener ID (port number could be used to match the listener).
    type: str
  port:
    description:
      - The listener port number (instead of using listener ID).
    type: int
  action:
    description:
      - The policy action.
    type: str
    choices: [ forward, redirect, target ]
  policy:
    description:
      - The user-defined name for this policy.
    type: str
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
      choices: [ contains, equals, matches_regex ]
    field:
      description:
        - HTTP header field.
      type: str
    type:
      description:
        - The type of the rule.
      type: str
      required: true
      choices: [ header, hostname, path ]
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
        required: false
      http_status_code:
        description
          - The http status code in the redirect response.
        type: int
        required: false
      choices: [ 301, 302, 303, 307, 308 ]
      url:
        description
          - The redirect target URL.
        type: str
        required: false
  state:
    description:
      - Should the resource be present or absent.
    type: str
    choices: [present, absent]
    default: present
'''

EXAMPLES = r'''
# Create policy (mathing listener by using port)
- ic_is_lb_policy:
    lb: ibmcloud-lb-baby
    port: 443
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


# Delete listener from load balancer by using listener ID
- ic_is_lb_listener:
    lb: ibmcloud-lb-baby
    listener: r006-ac61921a-63d3-4af2-9063-2b734a817c95
    state: absent

# Delete listener from load balancer by using port number
- ic_is_lb_listener:
    lb: ibmcloud-lb-baby
    port: 443
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
        port=dict(
            type='int',
            required=False),
        policy=dict(
            type='str',
            required=False),
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
    id = module.params['listener']
    port = module.params['port']
    name = module.params['policy']
    action = module.params['action']
    priority = module.params['priority']
    rules = module.params['rules']
    target = module.params['target']
    state = module.params["state"]

    if state == "absent":
        listener = id
        if port:
            listener = int(port)
        result = loadbalancer.delete_policy(lb, listener, name)

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "not_found":
                    module.fail_json(msg=result["errors"])
                else:
                    module.exit_json(changed=False, msg=(
                        "policy {} doesn't exist in listener {} for load"
                        " balancer {}".format(name, listener, lb)))

        module.exit_json(changed=True, msg=(
            "policy {} successfully deleted from listener {} in load"
            " balancer {}".format(name, listener, lb)))
    else:
        listener = id
        if port:
            listener = int(port)
        check = loadbalancer.get_lb_listener_policy(lb, listener, name)

        if "id" in check:
            module.exit_json(changed=False, msg=check)

        result = loadbalancer.create_policy(
            lb=lb,
            listener=listener,
            action=action,
            name=name,
            priority=priority,
            rules=rules,
            target=target
        )

        if "errors" in result:
            module.fail_json(msg=result["errors"])

        module.exit_json(changed=True, msg=(result))


def main():
    run_module()


if __name__ == '__main__':
    main()
