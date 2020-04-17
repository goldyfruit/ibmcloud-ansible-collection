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
module: ic_is_lb
short_description: Manage VPC load balancers on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module creates and provisions a new load balancer.
requirements:
  - "ibmcloud-python-sdk"
options:
  lb:
    description:
      - Load balancer name. An ID could be used for the deletion.
    type: str
    required: true
  subnets:
    description:
      - The subnets to provision this load balancer.
    type: list
  is_public:
    description:
      - The type of this load balancer, public or private.
    type: bool
    choices: [true, false]
  profile:
    description:
      - The profile to use for this load balancer.
    type: str
  resource_group:
    description:
      - The resource group for this load balancer.
    type: str
  pools:
    description:
      - The pools of this load balancer.
    type: list
    suboptions:
      algorithm:
        description:
          - The load balancing algorithm.
        type: str
        required: true
        choices: [least_connections, round_robin, weighted_round_robin]
      members:
        description:
          - The members for this load balancer pool.
        type: list
        suboptions:
          port:
            description:
              - The port number of the application running in the server
                member.
            type: int
            required: true
          target:
            description:
              - The pool member target.
            type: dict
            required: true
            suboptions
              instance:
                description:
                  - The unique identifier for this virtual server instance.
                type: str
              address:
                description:
                  - The IP address to be targeted by the pool member.
                type: str
          weight:
            description:
              - Weight of the server member.
            type: int
      name:
        description:
          - The user-defined name for this load balancer pool.
        type: str
      protocol:
        description:
          - The pool protocol.
        type: str
        required: true
        choices: [http, https, tcp]
      session_persistence:
        description:
          - The session persistence of this pool.
        type: dict
        suboptions:
          cookie_name:
            description:
              - Session persistence cookie name.
            type: str
          type:
            description:
              - The session persistence type.
            type: str
            required: true
            choices: [source_ip, app_cookie, http_cookie]
      health_monitor:
        description:
          - The health monitor of this pool.
        type: dict
        suboptions:
          delay:
            description:
              - The health check interval in seconds
            type: int
            required: true
        max_retries:
          description:
            - The health check max retries.
          type: int
          required: true
        port:
          description:
            - The health check port number.
          type: int
        timeout:
          description:
            - The health check timeout in seconds.
          type: int
          required: true
        url_path:
          description:
            - The health check URL.
        type:
          description:
            - The pool protocol.
          type: str
          required: true
          choices: [http, https, tcp]
    listeners:
      description:
        - The listeners of this load balancer.
      type: list
      suboptions:
        connection_limit:
          description:
            - The connection limit of the listener.
          type: int
        protocol:
          description:
            - The connection limit of the listener.
          type: str
          required: true
          choices: [http, https, tcp]
        port:
          description:
            - The listener port number.
          type: int
          required: true
        default_pool:
          description:
            - The default pool associated with the listener.
          suboptions:
            name:
              description:
                - The user-defined name for this load balancer pool.
              type: str
              required: true
  state:
    description:
      - Should the resource be present or absent.
    type: str
    default: present
    choices: [present, absent]
'''

EXAMPLES = r'''
- name: Create load balancer
  ic_is_lb:
    lb: ibmcloud-lb-baby
    is_public: true
    subnets:
      - ibmcloud-subnet-baby

- name: Create load balancer with pool and listener
  ic_is_lb:
    lb: ibmcloud-lb-baby
    is_public: true
    subnets:
      - ibmcloud-subnet-baby
    pools:
      - name: ibmcloud-lb-pool-baby
        algorithm: round_robin
        protocol: http
        health_monitor:
          delay: 5
          max_retries: 2
          timeout: 2
          type: http
          url_path: /
        members:
          - port: 80
            target:
              address: 10.0.12.15
          - port: 80
            target:
              address: 10.0.12.16
    listeners:
      - default_pool:
          name: ibmcloud-lb-pool-baby
        port: 80
        protocol: http

- name: Delete load balancer
  ic_is_lb:
    lb: ibmcloud-lb-baby
    state: absent
'''


def run_module():
    module_args = dict(
        lb=dict(
            type='str',
            required=True),
        subnets=dict(
            type='list',
            required=False),
        pools=dict(
            type='list',
            options=dict(
                algorithm=dict(
                    type='str',
                    required=True,
                    choices=['least_connections', 'round_robin',
                             'weighted_round_robin']),
                members=dict(
                    type='list',
                    options=dict(
                        port=dict(
                            type='int',
                            required=True),
                        target=dict(
                            type='dict',
                            options=dict(
                                instance=dict(
                                    type='str',
                                    required=False),
                                address=dict(
                                    type='str',
                                    required=False),
                            ),
                            required=True),
                        weight=dict(
                            type='int',
                            required=False),
                    ),
                    required=False),
                name=dict(
                    type='str',
                    required=False),
                protocol=dict(
                    type='str',
                    required=True,
                    choices=['http', 'https', 'tcp']),
                session_persistence=dict(
                    type='dict',
                    options=dict(
                        cookie_name=dict(
                            type='str',
                            required=False),
                        type=dict(
                            type='str',
                            required=True,
                            choices=['source_ip', 'app_cookie',
                                     'http_cookie']),
                    ),
                    required=False),
                health_monitor=dict(
                    type='dict',
                    options=dict(
                        delay=dict(
                            type='int',
                            required=True),
                        max_retries=dict(
                            type='int',
                            required=True),
                        port=dict(
                            type='int',
                            required=False),
                        timeout=dict(
                            type='int',
                            required=True),
                        url_path=dict(
                            type='str',
                            required=False),
                        type=dict(
                            type='str',
                            required=True,
                            choices=['http', 'https', 'tcp']),
                    ),
                    required=True),
                ),
            required=False),
        listeners=dict(
            type='list',
            options=dict(
                connection_limit=dict(
                    type='int',
                    required=False),
                port=dict(
                    type='int',
                    required=True),
                protocol=dict(
                    type='str',
                    required=True,
                    choices=['http', 'https', 'tcp']),
                default_pool=dict(
                    options=dict(
                        name=dict(
                            type='str',
                            required=True),
                    ),
                    required=False),
                ),
            required=False),
        is_public=dict(
            type='bool',
            required=False,
            choices=[True, False]),
        profile=dict(
            type='str',
            required=False),
        resource_group=dict(
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
    subnets = module.params['subnets']
    pools = module.params['pools']
    listeners = module.params['listeners']
    is_public = module.params['is_public']
    profile = module.params['profile']
    resource_group = module.params["resource_group"]
    state = module.params["state"]

    check = loadbalancer.get_lb(lb)

    if state == "absent":
        if "id" in check:
            result = loadbalancer.delete_lb(lb)
            if "errors" in result:
                module.fail_json(msg=result)

            payload = {"lb": lb, "status": "deleted"}
            module.exit_json(changed=True, msg=payload)

        payload = {"lb": lb, "status": "not_found"}
        module.exit_json(changed=True, msg=payload)
    else:
        if "id" in check:
            module.exit_json(changed=False, msg=check)

        result = loadbalancer.create_lb(
            name=lb,
            subnets=subnets,
            pools=pools,
            listeners=listeners,
            is_public=is_public,
            profile=profile,
            resource_group=resource_group
        )

        if "errors" in result:
            module.fail_json(msg=result)

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
