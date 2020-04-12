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
module: ic_is_lb_pool
short_description: Create or delete pool within a load balancer.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - Create or delete pool within a load balancer on IBM Cloud.
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
      - Pool name. An ID could be used for the deletion.
    type: str
    required: true
  algorithm:
    description:
      - The load balancing algorithm.
    type: str
    required: true
    choices: [ least_connections, round_robin, weighted_round_robin ]
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
  protocol:
    description:
      - The pool protocol.
    type: str
    required: true
    choices: [ http, https, tcp ]
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
        choices: [ source_ip, app_cookie, http_cookie ]
  health_monitor:
    description:
      - The health monitor of this pool.
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
      choices: [ http, https, tcp ]
    state:
      description:
        - Should the resource be present or absent.
      type: str
      choices: [present, absent]
      default: present
'''

EXAMPLES = r'''
# Create pool into load balancer
- ic_is_lb_pool:
    lb: ibmcloud-lb-baby
    pool: ibmcloud-lb-pool-baby
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

# Create pool into load balancer without members
- ic_is_lb_pool:
    lb: ibmcloud-lb-baby
    pool: ibmcloud-lb-pool-baby
    algorithm: round_robin
    protocol: http
    health_monitor:
      delay: 5
      max_retries: 2
      timeout: 2
      type: http
      url_path: /

# Delete pool from load balancer
- ic_is_lb:
    lb: ibmcloud-lb-baby
    pool: ibmcloud-lb-pool-baby
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
        algorithm=dict(
            type='str',
            required=False,
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
        protocol=dict(
            type='str',
            required=False,
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
    name = module.params['pool']
    algorithm = module.params['algorithm']
    members = module.params['members']
    protocol = module.params['protocol']
    session_persistence = module.params['session_persistence']
    health_monitor = module.params['health_monitor']
    state = module.params["state"]

    if state == "absent":
        result = loadbalancer.delete_pool(lb, name)

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "not_found":
                    module.fail_json(msg=result["errors"])
                else:
                    module.exit_json(changed=False, msg=(
                        "pool {} doesn't exist in load balancer {}".format(
                          name, lb)))

        module.exit_json(changed=True, msg=(
            "pool {} successfully deleted from load balancer {}".format(
              name, lb)))
    else:
        check = loadbalancer.get_lb_pool(lb, name)
        if "id" in check:
            module.exit_json(changed=False, msg=(check))

        result = loadbalancer.create_pool(
            lb=lb,
            name=name,
            algorithm=algorithm,
            members=members,
            protocol=protocol,
            session_persistence=session_persistence,
            health_monitor=health_monitor
        )

        if "errors" in result:
            module.fail_json(msg=result["errors"])

        module.exit_json(changed=True, msg=(result))


def main():
    run_module()


if __name__ == '__main__':
    main()
