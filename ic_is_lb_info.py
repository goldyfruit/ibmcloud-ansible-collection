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
module: ic_is_lb_info
short_description: Retrieve information about load balancers.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Retrieve information about load balancers from IBM Cloud.
notes:
    - The result contains a list of load balancers.
requirements:
    - "ibmcloud-python-sdk"
options:
    lb:
      description:
        - Restrict results to load balancer with UUID or name matching.
      required: false
'''

EXAMPLES = r'''
# Retrieve load balancer list
- ic_is_lb_info:

# Retrieve load balancer list and register the value
- ic_is_lb_info:
  register: lbs

# Display lbs registered value
- debug:
    var: lbs

# Retrieve a specific load balancer
- ic_is_lb_info:
    lb: ibmcloud-lb-baby
'''


def run_module():
    module_args = dict(
        lb=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    loadbalancer = sdk.Loadbalancer()

    name = module.params['lb']

    if name:
        result = loadbalancer.get_lb(name)
        if "errors" in result:
            module.fail_json(msg=result["errors"])
    else:
        result = loadbalancer.get_lbs()
        if "errors" in result:
            module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
