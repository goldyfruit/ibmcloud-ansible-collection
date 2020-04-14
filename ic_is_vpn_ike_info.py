#!/usr/bin/env python

# GNU General Public License v3.0+


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import vpn as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_vpn_ike_info
short_description: Retrieve information about VPN IKE policy.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - Retrieve information about VPN IKE policy from IBM Cloud.
notes:
  - The result contains a list of policies.
requirements:
  - "ibmcloud-python-sdk"
options:
  policy:
    description:
      - Restrict results to VPN IKE policy with ID or name matching.
'''

EXAMPLES = r'''
# Retrieve VPN IKE policy list
- ic_is_vpn_ike_info:

# Retrieve VPN IKE policy list and register the value
- ic_is_vpn_ike_info:
  register: policies

# Display VPN IKE policies registered value
- debug:
    var: policies

# Retrieve a specific VPN IKE policy
- ic_is_vpn_ike_info:
    policy: ibmcloud-vpn-ike-policy-baby
'''


def run_module():
    module_args = dict(
        policy=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    vpn = sdk.Vpn()

    name = module.params['policy']

    if name:
        result = vpn.get_ike_policy(name)
        if "errors" in result:
            module.fail_json(msg=result["errors"])
    else:
        result = vpn.get_ike_policies()
        if "errors" in result:
            module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
