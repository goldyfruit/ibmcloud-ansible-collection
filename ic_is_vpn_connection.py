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
module: ic_is_vpn_connection
short_description: Manage VPC VPN connections on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module creates a new VPN connection on a specific VPN gateway.
requirements:
  - "ibmcloud-python-sdk"
options:
  gateway:
    description:
      - The user-defined name for this VPN gateway.
    type: str
    required: true
  connection:
    description:
      - The user-defined name for this VPN connection.
    type: str
    required: true
  admin_state_up:
    description:
      - If set to false, the VPN connection is shut down.
    type: bool
    choices: [true, false]
  dead_peer_detection:
    description:
      - The Dead Peer Detection settings.
    type: dict
    suboptions:
      action:
        description:
          - Dead Peer Detection actions.
        type: str
        default: restart
        choices: [clear, hold, none, restart]
      interval:
        description:
          - Dead Peer Detection interval in seconds.
        type: int
        default: 2
      timeout
        description:
          - Dead Peer Detection timeout in seconds. Must be at least the
            interval.
        type: int
        default: 10
  ike_policy:
    description:
      - IKE policy configuration. The absence of a policy indicates
        autonegotiation.
    type: str
  ipsec_policy:
    description:
      - IPsec policy configuration. The absence of a policy indicates
        autonegotiation.
    type: str
  local_cidrs:
    description:
      - A collection of local CIDRs for this resource.
    type: list
  peer_address:
    description:
      - The IP address of the peer VPN gateway.
    type: str
  peer_cidrs:
    description:
      - A collection of peer CIDRs for this resource.
    type: list
  psk:
    description:
      - The preshared key.
    type: str
  state:
    description:
      - Should the resource be present or absent.
    type: str
    default: present
    choices: [present, absent]
'''

EXAMPLES = r'''
- name: Create VPN connection with IKE and IPsec auto-negotiation
  ic_is_vpn_connection:
    gateway: ibmcloud-vpn-gateway-baby
    connection: ibmcloud-vpn-connection-baby
    local_cidrs:
      - 192.168.0.0/24
    peer_address: 10.123.12.123
    peer_cidrs:
      - 10.0.0.0/24
    psk: "@!Il0v3IBMCl0udB4by!@"

- name: Create VPN connection with custom policies and dead peer configuration
  ic_is_vpn_connection:
    gateway: ibmcloud-vpn-gateway-baby
    connection: ibmcloud-vpn-connection-baby
    ipsec_policy: ibmcloud-vpn-ipsec-baby
    ike_policy: ibmcloud-vpn-ike-baby
    dead_peer_detection:
      action: restart
      interval: 2
      timeout: 10
    local_cidrs:
      - 192.168.0.0/24
    peer_address: 10.123.12.123
    peer_cidrs:
      - 10.0.0.0/24
    psk: "@!Il0v3IBMCl0udB4by!@"

- name: Delete VPN connection
  ic_is_vpn_connection:
    gateway: ibmcloud-vpn-gateway-baby
    connection: ibmcloud-vpn-connection-baby
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
        admin_state_up=dict(
            type='bool',
            required=False,
            choices=[True, False]),
        dead_peer_detection=dict(
            type='dict',
            options=dict(
                action=dict(
                    type='str',
                    required=True,
                    default='restart',
                    choices=['clear', 'hold', 'none', 'restart']),
                interval=dict(
                    type='int',
                    required=True,
                    default=2),
                timeout=dict(
                    type='int',
                    required=True,
                    default=10),
            ),
            required=False),
        ike_policy=dict(
            type='str',
            required=False),
        ipsec_policy=dict(
            type='str',
            required=False),
        local_cidrs=dict(
            type='list',
            required=False),
        peer_address=dict(
            type='str',
            required=False),
        peer_cidrs=dict(
            type='list',
            required=False),
        psk=dict(
            type='str',
            required=False,
            no_log=True),
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
    admin_state_up = module.params['admin_state_up']
    dead_peer_detection = module.params['dead_peer_detection']
    ike_policy = module.params['ike_policy']
    ipsec_policy = module.params['ipsec_policy']
    local_cidrs = module.params['local_cidrs']
    peer_address = module.params['peer_address']
    peer_cidrs = module.params['peer_cidrs']
    psk = module.params['psk']
    state = module.params["state"]

    check = vpn.get_vpn_gateway_connection(gateway, connection)

    if state == "absent":
        if "id" in check:
            result = vpn.delete_connection(gateway, connection)
            if "errors" in result:
                module.fail_json(msg=result)

            payload = {"connection": connection, "gateway": gateway,
                       "status": "deleted"}
            module.exit_json(changed=True, msg=payload)

        payload = {"connection": connection, "gateway": gateway,
                   "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        if "id" in check:
            module.exit_json(changed=False, msg=check)

        result = vpn.create_connection(
            gateway=gateway,
            name=connection,
            admin_state_up=admin_state_up,
            dead_peer_detection=dead_peer_detection,
            ike_policy=ike_policy,
            ipsec_policy=ipsec_policy,
            local_cidrs=local_cidrs,
            peer_address=peer_address,
            peer_cidrs=peer_cidrs,
            psk=psk,
        )

        if "errors" in result:
            module.fail_json(msg=result)

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
