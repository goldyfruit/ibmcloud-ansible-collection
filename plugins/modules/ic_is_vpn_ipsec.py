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
module: ic_is_vpn_ipsec
short_description: Manage VPC VPN IPsec policies on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module creates a new IPsec policy.
requirements:
  - "ibmcloud-python-sdk"
options:
  policy:
    description:
      - The user-defined name for this IPsec policy.
    type: str
    required: true
  authentication_algorithm:
    description:
      - The authentication algorithm.
    type: str
    choices: [md5, sha1, sha256]
  pfs:
    description:
      - Perfect Forward Secrecy.
    type: str
    choices: [disabled, group_14, group_2, group_5]
  encryption_algorithm:
    description:
      - The encryption algorithm.
    type: str
    choices: [triple_des, aes128, aes256]
  key_lifetime:
    description:
      - The key lifetime in seconds.
    type: int
  resource_group:
    description:
      - The resource group to use.
    type: str
  state:
    description:
      - Should the resource be present or absent.
    type: str
    default: present
    choices: [present, absent]
'''

EXAMPLES = r'''
- name: Create VPN IPsec policy
  ic_is_vpn_ipsec:
    policy: ibmcloud-vpn-ipsec-baby
    authentication_algorithm: sha256
    encryption_algorithm: triple_des
    ike_version: 2
    pfs: disabled
    key_lifetime: 3600

- name: Delete VPN IPsec policy
  ic_is_vpn_ipsec:
    policy: ibmcloud-vpn-ipsec-baby
    state: absent
'''


def run_module():
    module_args = dict(
        policy=dict(
            type='str',
            required=True),
        authentication_algorithm=dict(
            type='str',
            required=False,
            choices=['md5', 'sha1', 'sha256']),
        pfs=dict(
            type='str',
            required=False,
            choices=['disabled', 'group_14', 'group_2', 'group_5']),
        encryption_algorithm=dict(
            type='str',
            required=False,
            choices=['triple_des', 'aes128', 'aes256']),
        key_lifetime=dict(
            type='int',
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

    vpn = sdk.Vpn()

    policy = module.params['policy']
    authentication_algorithm = module.params['authentication_algorithm']
    pfs = module.params['pfs']
    encryption_algorithm = module.params['encryption_algorithm']
    key_lifetime = module.params['key_lifetime']
    resource_group = module.params['resource_group']
    state = module.params["state"]

    check = vpn.get_ipsec_policy(policy)

    if state == "absent":
        if "id" in check:
            result = vpn.delete_ipsec_policy(policy)
            if "errors" in result:
                module.fail_json(msg=result)

            payload = {"policy": policy, "status": "deleted"}
            module.exit_json(changed=True, msg=payload)

        payload = {"policy": policy, "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        if "id" in check:
            module.exit_json(changed=False, msg=check)

        result = vpn.create_ipsec_policy(
            name=policy,
            authentication_algorithm=authentication_algorithm,
            pfs=pfs,
            encryption_algorithm=encryption_algorithm,
            key_lifetime=key_lifetime,
            resource_group=resource_group,
        )

        if "errors" in result:
            module.fail_json(msg=result)

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
