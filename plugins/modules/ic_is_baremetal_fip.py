#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import baremetal as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_instance_fip
short_description: Manage VPC floating IP attachments to BMS on IBM Cloud.
author: James Regis (@jamesregis)
version_added: "2.9"
description:
  - Associates the specified floating IP with the specified network interface,
    replacing any existing association. For this request to succeed, the
    existing floating IP must not be required by another resource, such as a
    public gateway.
requirements:
  - "ibmcloud-python-sdk"
options:
  instance:
    description:
      -  BMS (Bare Metal Server) name or ID.
    required: true
  floatin_ip:
    description:
      - The floating IP ID, name or address to attach on the BMS's network
        interface.
    required: true
  interface:
    description:
      - Network interface where the floating IP should be attached. If no
        interface is provided the attachment will happen on the primary
        network interface.
  state:
    description:
      - Should the resource be present or absent.
    type: str
    default: present
    choices: [present, absent, attach, detach]
'''

EXAMPLES = r'''
- name: Attach floating IP primary network interface of a BMS
  ic_is_baremetal_fip:
    instance: ibmcloud-bms-baby
    floating_ip: ibmcloud-fip-baby

- name: Attach floating IP on specific interface of a bms
  ic_is_baremetal_fip:
    instance: ibmcloud-bms-baby
    floating_ip: ibmcloud-vip-baby
    interface: ibmclouc-nic-baby

- name: Detach floating IP from baremetal
  ic_is_baremetal_fip:
    instance: ibmcloud-instance-baby
    floating_ip: ibmcloud-vip-baby
    state: detach
'''


def run_module():
    module_args = dict(
        instance=dict(
            type='str',
            required=True),
        floating_ip=dict(
            type='str',
            required=True),
        interface=dict(
            type='str',
            required=False),
        state=dict(
            type='str',
            default='attach',
            choices=['absent', 'present', 'attach', 'detach'],
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    bms_instance = sdk.Baremetal()

    server = module.params["instance"]
    floating_ip = module.params["floating_ip"]
    interface = module.params["interface"]
    state = module.params["state"]

    if not interface:
        instance_info = bms_instance.get_server(server)
        interface = instance_info["primary_network_interface"]["id"]

    check = bms_instance.get_server_interface_fip(server, interface,
                                                  floating_ip)

    if state == "absent" or state == "detach":
        if "id" in check:
            result = bms_instance.disassociate_floating_ip(server,
                                                           interface,
                                                           floating_ip)
            if "errors" in result:
                module.fail_json(msg=result)

            payload = {"floating_ip": floating_ip, "status": "detached"}
            module.exit_json(changed=True, msg=payload)

        payload = {"floating_ip": floating_ip, "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        if "id" in check:
            module.exit_json(changed=False, msg=check)

        result = bms_instance.associate_floating_ip(
            server=server,
            interface=interface,
            fip=floating_ip
        )

        if "errors" in result:
            module.fail_json(msg=result)

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
