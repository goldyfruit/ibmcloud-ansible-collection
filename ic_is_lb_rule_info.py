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
module: ic_is_lb_rule_info
short_description: Retrieve information about rules from load balancer.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Retrieve information about rules within policy from listeners for
      specific load balancers from IBM Cloud.
notes:
    - The result contains a list of rules.
requirements:
    - "ibmcloud-python-sdk"
options:
    lb:
      description:
        - Load balancer name or ID.
      required: true
    listener:
      description:
        - Restrict results to listener with ID or port matching.
      required: false
    port:
      description:
        - Restrict results to listener with port matching.
      required: false
    policy:
      description:
        - Restrict results to policy with name or ID matching.
      required: true
    rule:
      description:
        - Restrict results to rule with name or ID matching.
    required: false
'''

EXAMPLES = r'''
# Retrieve rule list from specific policy
- ic_is_lb_rule_info:
    lb: ibmcloud-lb-baby
    listener: r006-e503af14-7ca1-4bb6-a8eb-f25b73323041
    policy: ibmcloud-lb-policy-baby

# Retrieve rule list and register the value
- ic_is_lb_rule_info:
    lb: ibmcloud-lb-baby
    listener: r006-e503af14-7ca1-4bb6-a8eb-f25b73323041
    policy: ibmcloud-lb-policy-baby
  register: rules

# Display rules registered value
- debug:
    var: rules

# Retrieve specific policy from listener (port filtering)
- ic_is_lb_rule_info:
    lb: ibmcloud-lb-baby
    port: 443
    policy: ibmcloud-lb-policy-baby
    rule: ibmcloud-lb-rule-baby
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

    if id:
        listener = id
    elif port:
        listener = int(port)

    if name:
        result = loadbalancer.get_lb_listener_policy_rule(lb, listener, policy,
                                                          name)
        if "errors" in result:
            module.fail_json(msg=result["errors"])
    else:
        result = loadbalancer.get_lb_listener_policy_rules(lb, listener,
                                                           policy)
        if "errors" in result:
            module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
