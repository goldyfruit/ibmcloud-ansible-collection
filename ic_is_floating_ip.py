#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import floating_ip as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_floating_ip
short_description: Manage VPC floating IP on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - Floating IPs allow inbound and outbound traffic from the Internet
    to an instance.
requirements:
  - "ibmcloud-python-sdk"
options:
  fip:
    description:
      - The unique user-defined name for this floating IP.
    type: str
    required: true
  resource_group:
    description:
      - The resource group to use. If unspecified, the account's default
        resource group is used.
    type: str
  target:
    description:
      - The target this address is to be bound to.
    type: str
  zone:
    description:
      - The name of the zone to provision a floating IP in.
    type: str
  state:
    description:
      - Should the resource be present, absent, attach or detach.
    default: present
    choices: [present, absent, reserve, release]
'''

EXAMPLES = r'''
- name: Reserve floating IP within a zone
  ic_is_floating_ip:
    fip: ibmcloud-fip-baby
    zone: us-south-3

- name: Reserve floating IP and bound it to a reserved IP
  ic_is_floating_ip:
    fip: ibmcloud-fip-baby
    target: 69e55145-cc7d-4d8e-9e1f-cc3fb60b1793

- name: Release floating IP
- ic_is_floating_ip:
    fip:  ibmcloud-fip-baby
    state: release
'''


def run_module():
    module_args = dict(
        fip=dict(
            type='str',
            required=True),
        resource_group=dict(
            type='str',
            required=False),
        target=dict(
            type='str',
            required=False),
        zone=dict(
            type='str',
            required=False),
        state=dict(
            type='str',
            default='present',
            choices=['absent', 'present', 'reserve', 'release'],
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    floating_ip = sdk.Fip()

    fip = module.params["fip"]
    resource_group = module.params["resource_group"]
    target = module.params["target"]
    zone = module.params["zone"]
    state = module.params["state"]

    check = floating_ip.get_floating_ip(fip)

    if state == "absent" or state == "release":
        if "id" in check:
            result = floating_ip.release_floating_ip(fip)
            if "errors" in result:
                module.fail_json(msg=result["errors"])

            payload = {"floating_ip": fip, "status": "deleted"}
            module.exit_json(changed=True, msg=payload)

        payload = {"floating_ip": fip, "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        if "id" in check:
            module.exit_json(changed=False, msg=check)

        result = floating_ip.reserve_floating_ip(
            name=fip,
            resource_group=resource_group,
            target=target,
            zone=zone
        )

        if "errors" in result:
            module.fail_json(msg=result["errors"])

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
