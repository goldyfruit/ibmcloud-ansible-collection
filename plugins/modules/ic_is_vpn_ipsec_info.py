#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import vpn as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_vpn_ipsec_info
short_description: Manage VPC VPN IPsec policies on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module retrieves a paginated list of all IPsec policies that belong
    to this account.
notes:
  - The result contains a list of policies.
requirements:
  - "ibmcloud-python-sdk"
options:
  policy:
    description:
      - Restrict results to VPN IPsec policy with ID or name matching.
    type: str
'''

EXAMPLES = r'''
- name: Retrieve VPN IPsec policy list
  ic_is_vpn_ipsec_info:

- name: Retrieve a specific VPN IPsec policy
  ic_is_vpn_ipsec_info:
    policy: ibmcloud-vpn-ipsec-baby
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

    policy = module.params['policy']

    if policy:
        result = vpn.get_ipsec_policy(policy)
        if "errors" in result:
            module.fail_json(msg=result)
    else:
        result = vpn.get_ipsec_policies()
        if "errors" in result:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
