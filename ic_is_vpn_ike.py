#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
module: ic_is_vpn_ike
short_description: Create or delete VPN IKE policy.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - Create or delete VPN IKE policy on IBM Cloud.
requirements:
  - "ibmcloud-python-sdk"
options:
  policy:
    description:
      - The user-defined name for this IKE policy
    type: str
    required: true
  authentication_algorithm:
    description:
      - The authentication algorithm.
    type: str
    choices: [ md5, sha1, sha256 ]
  dh_group:
    description:
      - The Diffie-Hellman group.
    type: int
    choices: [ 2, 5, 14 ]
  encryption_algorithm:
    description:
      - The encryption algorithm.
    type: str
    choices: [ triple_des, aes128, aes256 ]
  ike_version:
    description:
      - The IKE protocol version.
    type: int
    choices: [ 1, 2 ]
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
    choices: [present, absent]
    default: present
'''

EXAMPLES = r'''
# Create VPN IKE v2 policy
- ic_is_vpn_ike:
    policy: ibmcloud-vpn-ike-baby
    authentication_algorithm: sha256
    dh_group: 2
    encryption_algorithm: aes256
    ike_version: 2
    key_lifetime: 28800

# Delete VPN IKE policy
- ic_is_vpn_ike:
    policy: ibmcloud-vpn-ike-baby
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
        dh_group=dict(
            type='int',
            required=False,
            choices=[2, 5, 14]),
        encryption_algorithm=dict(
            type='str',
            required=False,
            choices=['triple_des', 'aes128', 'aes256']),
        ike_version=dict(
            type='int',
            required=False,
            choices=[1, 2]),
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

    name = module.params['policy']
    authentication_algorithm = module.params['authentication_algorithm']
    dh_group = module.params['dh_group']
    encryption_algorithm = module.params['encryption_algorithm']
    ike_version = module.params['ike_version']
    key_lifetime = module.params['key_lifetime']
    resource_group = module.params['resource_group']
    state = module.params["state"]

    if state == "absent":
        result = vpn.delete_ike_policy(name)

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "not_found":
                    module.fail_json(msg=result["errors"])
                else:
                    module.exit_json(changed=False, msg=(
                        "policy {} doesn't exist".format(name)))

        module.exit_json(changed=True, msg=(
            "policy {} successfully deleted".format(name)))
    else:
        check = vpn.get_ike_policy(name)
        if "id" in check:
            module.exit_json(changed=False, msg=(check))

        result = vpn.create_ike_policy(
            name=name,
            authentication_algorithm=authentication_algorithm,
            dh_group=dh_group,
            encryption_algorithm=encryption_algorithm,
            ike_version=ike_version,
            key_lifetime=key_lifetime,
            resource_group=resource_group,
        )

        if "errors" in result:
            module.fail_json(msg=result["errors"])

        module.exit_json(changed=True, msg=(result))


def main():
    run_module()


if __name__ == '__main__':
    main()
