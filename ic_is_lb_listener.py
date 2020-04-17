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
module: ic_is_lb_listener
short_description: Manage VPC load balancer listener IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module creates a new listener to the load balancer.
requirements:
  - "ibmcloud-python-sdk"
options:
  lb:
    description:
      - Load balancer name or ID.
    type: str
    required: true
  connection_limit:
    description:
      - The connection limit of the listener.
    type: int
  policies:
    description:
      - The list of policies of this listener
    type: list
    suboptions:
      action:
        description:
          - The policy action.
        type: str
        choices: [forward, redirect, target]
      name:
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
  protocol:
    description:
      - The connection limit of the listener.
    type: str
    choices: [http, https, tcp]
  port:
    description:
      - The listener port number.
      - C(port) option should be used as listener matcher for the deletion.
    type: int
    required: true
  default_pool:
    description:
      - The default pool associated with the listener.
    type: str
  state:
    description:
      - Should the resource be present or absent.
    type: str
    default: present
    choices: [present, absent]
'''

EXAMPLES = r'''
- name: Create listener
  ic_is_lb_listener:
    lb: ibmcloud-lb-baby
    default_pool: ibmcloud-lb-pool-baby
    port: 443
    protocol: http

- name: Create listener with policy and rule
  ic_is_lb_listener:
    lb: ibmcloud-lb-baby
    default_pool: ibmcloud-lb-pool-baby
    port: 443
    protocol: http
    connection_limit: 2000
    policies:
      - name: ibmcloud-lb-policy-baby
        action: forward
        priority: 5
        rules:
          - condition: contains
            field: MY-APP-HEADER
            type: header
            value: string
        target:
          id: r006-0c1b2e3f-d38a-4c48-9f08-b4432c9601a6

- name: Delete listener from load balancer
  ic_is_lb_listener:
    lb: ibmcloud-lb-baby
    port: 443
    state: absent
'''


def run_module():
    module_args = dict(
        lb=dict(
            type='str',
            required=True),
        connection_limit=dict(
            type='int',
            required=False),
        certificate_instance=dict(
            type='str',
            required=False),
        policies=dict(
            type='list',
            options=dict(
                action=dict(
                    type='int',
                    required=True),
                name=dict(
                    type='int',
                    required=False),
                priority=dict(
                    type='int',
                    required=True),
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
            ),
            required=False),
        port=dict(
            type='int',
            required=True),
        protocol=dict(
            type='str',
            required=False,
            choices=['http', 'https', 'tcp']),
        default_pool=dict(
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
    connection_limit = module.params['connection_limit']
    certificate_instance = module.params['certificate_instance']
    policies = module.params['policies']
    port = module.params['port']
    protocol = module.params['protocol']
    default_pool = module.params['default_pool']
    state = module.params["state"]

    check = loadbalancer.get_lb_listener(lb, port)

    if state == "absent":
        if "id" in check:
            result = loadbalancer.delete_listener(lb, port)
            if "errors" in result:
                module.fail_json(msg=result)

            payload = {"listener": port, "lb": lb, "status": "deleted"}
            module.exit_json(changed=True, msg=payload)

        payload = {"listener": port, "lb": lb, "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        if "id" in check:
            module.exit_json(changed=False, msg=check)

        result = loadbalancer.create_listener(
            lb=lb,
            connection_limit=connection_limit,
            certificate_instance=certificate_instance,
            policies=policies,
            port=port,
            protocol=protocol,
            default_pool=default_pool
        )

        if "errors" in result:
            module.fail_json(msg=result)

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
