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
module: ic_is_vpn_cidr
short_description: Add or remove CIDR from VPN connection.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - Add or remove local/peer CIDR from VPN connection on IBM Cloud.
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
    choices: [present, absent]
    default: present
'''

EXAMPLES = r'''
# Add peer CIDR to VPN connection
- ic_is_vpn_cidr:
    gateway: ibmcloud-vpn-gateway-baby
    connection: ibmcloud-vpn-connection-baby
    target: peer
    cidr: 10.0.0.0/24

# Add local CIDR to VPN connection
- ic_is_vpn_cidr:
    gateway: ibmcloud-vpn-gateway-baby
    connection: ibmcloud-vpn-connection-baby
    target: local
    cidr: 172.0.0.0/24

# Delete peer CIDR from VPN connection
- ic_is_vpn_cidr:
    gateway: ibmcloud-vpn-gateway-baby
    connection: ibmcloud-vpn-connection-baby
    target: peer
    cidr: 10.0.0.0/24
    state: absent

# Delete local CIDR from VPN connection
- ic_is_vpn_cidr:
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
    name = module.params['cidr']
    state = module.params["state"]

    # Split CIDR to get address and length
    if name:
        prefix_address = name.split('/')[0]
        prefix_length = name.split('/')[1]

    if target == "local":
        check = vpn.check_vpn_gateway_local_cidr(
          gateway, connection, prefix_address, prefix_length)
    else:
        check = vpn.check_vpn_gateway_peer_cidr(
          gateway, connection, prefix_address, prefix_length)

    if state == "absent":
        if "errors" in check:
            for key in check["errors"]:
                if key["code"] != "vpn_connection_cidr_not_found":
                    module.fail_json(msg=check["errors"])
                else:
                    module.exit_json(changed=False, msg=(
                        "{} cidr {} doesn't exist in connection {}".format(
                          target, name, connection)))

        if target == "local":
            result = vpn.remove_local_cidr(gateway, connection,
                                           prefix_address, prefix_length)
        else:
            result = vpn.remove_peer_cidr(gateway, connection,
                                          prefix_address, prefix_length)

        module.exit_json(changed=True, msg=(
            "{} cidr {} successfully removed from connection {}".format(
              target, name, connection)))
    else:
        if "peer_cidr" in check or "local_cidr" in check:
            module.exit_json(change=False,
                             msg="{} cidr {} already exists in connection"
                                 " {}.".format(target, name, connection))
        elif "errors" in check:
            for key in check["errors"]:
                if key["code"] != "vpn_connection_cidr_not_found":
                    module.fail_json(msg=check["errors"])

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
            module.fail_json(msg=result["errors"])

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
