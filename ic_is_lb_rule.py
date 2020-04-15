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
    choices: [ contains, equals, matches_regex ]
  field:
    description:
      - HTTP header field.
    type: str
  type:
    description:
      - The type of the rule.
    type: str
    choices: [ header, hostname, path ]
  value
    description:
      - Value to be matched for rule condition.
    type: str
  state:
    description:
      - Should the resource be present or absent.
    type: str
    choices: [present, absent]
    default: present
'''

EXAMPLES = r'''
# Create rule (mathing listener by using port)
- ic_is_lb_policy:
    lb: ibmcloud-lb-baby
    port: 443
    policy: ibmcloud-lb-policy-baby
    condition: contains
    field: MY-APP-HEADER
    type: header
    value: string


# Delete listener from load balancer by using listener ID
- ic_is_lb_listener:
    lb: ibmcloud-lb-baby
    listener: r006-ac61921a-63d3-4af2-9063-2b734a817c95
    policy: ibmcloud-lb-policy-baby
    rule: 70294e14-4e61-11e8-bcf4-0242ac110004
    state: absent

# Delete listener from load balancer by using port number
- ic_is_lb_listener:
    lb: ibmcloud-lb-baby
    port: 443
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
        port=dict(
            type='int',
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
    id = module.params['listener']
    port = module.params['port']
    policy = module.params['policy']
    name = module.params['rule']
    condition = module.params['condition']
    field = module.params['field']
    type = module.params['type']
    value = module.params['value']
    state = module.params["state"]

    if state == "absent":
        listener = id
        if port:
            listener = int(port)
        result = loadbalancer.delete_rule(lb, listener, policy, name)

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "not_found":
                    module.fail_json(msg=result["errors"])
                else:
                    module.exit_json(changed=False, msg=(
                        "rule {} doesn't exist within policy {} in listener {}"
                        " for load balancer {}".format(name, policy, listener,
                                                       lb)))

        module.exit_json(changed=True, msg=(
            "rule {} successfully deleted from policy {} for listener {} in"
            " load balancer {}".format(name, policy, listener, lb)))
    else:
        listener = id
        if port:
            listener = int(port)
        check = loadbalancer.get_lb_listener_policy_rule(lb, listener, policy,
                                                         name)

        if "id" in check:
            module.exit_json(changed=False, msg=check)

        result = loadbalancer.create_rule(
            lb=lb,
            listener=listener,
            policy=policy,
            condition=condition,
            field=field,
            type=type,
            value=value,
        )

        if "errors" in result:
            module.fail_json(msg=result["errors"])

        module.exit_json(changed=True, msg=(result))


def main():
    run_module()


if __name__ == '__main__':
    main()
