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
module: ic_is_vpn_cidr
short_description: Manage VPC VPN local or peer CIDRs on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module adds the specified CIDR to the specified resource. A request
    body is not required, and if supplied, is ignored. This request succeeds
    if the CIDR already exists on the resource.
requirements:
  - "ibmcloud-python-sdk"
options:
  gateway:
    description:
      - VPN gateway ID or name.
    type: str
    required: true
  connection:
    description:
      - VPN connection ID or name.
    type: str
    required: true
  target:
    description:
      - Retrieve local or peer CIDRs.
    type: str
    default: local
    choices: [local, peer]
  cidr:
    description:
      - Restrict results to specific CIDR.
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
- name: Add peer CIDR to VPN connection
  ic_is_vpn_cidr:
    gateway: ibmcloud-vpn-gateway-baby
    connection: ibmcloud-vpn-connection-baby
    target: peer
    cidr: 10.0.0.0/24

- name: Add local CIDR to VPN connection
  ic_is_vpn_cidr:
    gateway: ibmcloud-vpn-gateway-baby
    connection: ibmcloud-vpn-connection-baby
    target: local
    cidr: 172.0.0.0/24

- name: Delete peer CIDR from VPN connection
  ic_is_vpn_cidr:
    gateway: ibmcloud-vpn-gateway-baby
    connection: ibmcloud-vpn-connection-baby
    target: peer
    cidr: 10.0.0.0/24
    state: absent

- name: Delete local CIDR from VPN connection
  ic_is_vpn_cidr:
    gateway: ibmcloud-vpn-gateway-baby
    connection: ibmcloud-vpn-connection-baby
    target: local
    cidr: 172.0.0.0/24
    state: absent
'''


def run_module():
    module_args = dict(
        gateway=dict(
            type='str',
            required=True),
        connection=dict(
            type='str',
            required=True),
        target=dict(
            type='str',
            default='local',
            choices=['local', 'peer']),
        cidr=dict(
            type='str',
            required=True),
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

    gateway = module.params['gateway']
    connection = module.params['connection']
    target = module.params['target']
    cidr = module.params['cidr']
    state = module.params["state"]

    # Split CIDR to get address and length
    if cidr:
        prefix_address = cidr.split('/')[0]
        prefix_length = cidr.split('/')[1]

    if target == "local":
        check = vpn.check_vpn_gateway_local_cidr(
          gateway, connection, prefix_address, prefix_length)
    else:
        check = vpn.check_vpn_gateway_peer_cidr(
          gateway, connection, prefix_address, prefix_length)

    if state == "absent":
        if "peer_cidr" in check or "local_cidr" in check:
            if target == "local":
                result = vpn.remove_local_cidr(gateway, connection,
                                               prefix_address, prefix_length)
            else:
                result = vpn.remove_peer_cidr(gateway, connection,
                                              prefix_address, prefix_length)

            if "errors" in result:
                module.fail_json(msg=result)

            payload = {"cidr": cidr, "target": target,
                       "connection": connection, "status": "deleted"}
            module.exit_json(changed=True, msg=payload)

        payload = {"cidr": cidr, "target": target,
                   "connection": connection, "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        if "peer_cidr" in check or "local_cidr" in check:
            payload = {"cidr": cidr, "target": target,
                       "connection": connection, "status": "already_exists"}
            module.exit_json(change=False, msg=payload)

        if target == "local":
            result = vpn.add_local_cidr_connection(
              gateway=gateway,
              connection=connection,
              prefix_address=prefix_address,
              prefix_length=prefix_length,
            )
        else:
            result = vpn.add_peer_cidr_connection(
              gateway=gateway,
              connection=connection,
              prefix_address=prefix_address,
              prefix_length=prefix_length,
            )

        if "errors" in result:
            module.fail_json(msg=result)

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
