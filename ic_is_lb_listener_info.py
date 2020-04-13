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
module: ic_is_lb_listener_info
short_description: Retrieve information about listeners within load balancer.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Retrieve information about listeners within specific load balancers from
      IBM Cloud.
notes:
    - The result contains a list of listeners.
requirements:
    - "ibmcloud-python-sdk"
options:
    lb:
      description:
        - Load balancer name or ID.
      required: true
    listener:
      description:
        - Restrict results to listener with UUID matching.
      required: false
    port:
      description:
        - Restrict results to listener with port matching.
      required: false
'''

EXAMPLES = r'''
# Retrieve listener list specific load balancer
- ic_is_lb_listener_info:
    lb: ibmcloud-lb-baby

# Retrieve listener list and register the value
- ic_is_lb_listener_info:
    lb: ibmcloud-lb-baby
  register: listeners

# Display listeners registered value
- debug:
    var: listeners

# Retrieve specific listener from a load balancer
- ic_is_lb_listener_info:
    lb: ibmcloud-lb-baby
    listener: ibmcloud-listener-baby

# Retrieve specific listener from a load balancer by using port
- ic_is_lb_listener_info:
    lb: ibmcloud-lb-baby
    port: 443
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
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    loadbalancer = sdk.Loadbalancer()

    lb = module.params['lb']
    id = module.params['listener']
    port = module.params['port']

    if id:
        listener = id
    elif port:
        listener = int(port)

    if listener:
        result = loadbalancer.get_lb_listener(lb, listener)
        if "errors" in result:
            module.fail_json(msg=result["errors"])
    else:
        result = loadbalancer.get_lb_listeners(lb)
        if "errors" in result:
            module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
