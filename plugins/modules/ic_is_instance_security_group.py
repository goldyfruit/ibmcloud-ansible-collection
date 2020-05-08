#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import security as sdk_security
from ibmcloud_python_sdk.vpc import instance as sdk_instance


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_instance_security_group
short_description: Manage VPC security group attachments to VSI on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - When a network interface is added to a security group, the security group
    rules are applied to the network interface. A request body is not required,
    and if supplied, is ignored.
requirements:
  - "ibmcloud-python-sdk"
options:
  instance:
    description:
      - VSI (Virtual Server Instance) where to attach the security group.
        If C(interface) options is not provided then security group will be
        attached to VSI primary network interface.
    type: str
    required: true
  interface:
    description:
      - VSI network interface where to attach the security group.
    type: str
  group:
    description:
      - The identity of the security group to attach to the interface.
    required: true
  state:
    description:
      - Should the resource be present or absent.
    type: str
    default: present
    choices: [present, absent, attach, detach]
'''

EXAMPLES = r'''
- name: Attach security group VSI primary network interface
  ic_is_instance_security_group:
    instance: ibmcloud-vsi-baby
    group: ibmcloud-sec-group-baby

- name: Attach security group on specific VSI network interface
  ic_is_instance_security_group:
    instance: ibmcloud-vsi-baby
    interface: ibmcloud-interface-baby
    group: ibmcloud-sec-group-baby

- name: Detach security group from VSI primary network interface
  ic_is_instance_security_group:
    instance: ibmcloud-vsi-baby
    group: ibmcloud-sec-group-baby
    state: detach

- name: Detach security group from specific VSI network interface
- ic_is_instance_security_group:
    instance: ibmcloud-vsi-baby
    interface: ibmcloud-interface-baby
    group: ibmcloud-sec-group-baby
    state: detach
'''


def run_module():
    module_args = dict(
        instance=dict(
            type='str',
            required=True),
        interface=dict(
            type='str',
            required=False),
        group=dict(
            type='str',
            required=True),
        state=dict(
            type='str',
            default='detach',
            choices=['absent', 'present', 'attach', 'detach'],
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    security = sdk_security.Security()
    instance = sdk_instance.Instance()

    group = module.params["group"]
    vsi = module.params["instance"]
    interface = module.params["interface"]
    state = module.params["state"]

    target = None
    if not interface:
        instance_info = instance.get_instance(vsi)
        if "errors" in instance_info:
            module.fail_json(msg=instance_info)
        target = instance_info["primary_network_interface"]["id"]
    else:
        nic_info = instance.get_instance_interface(vsi, interface)
        if "errors" in nic_info:
            module.fail_json(msg=nic_info)
        target = nic_info["id"]

    check = security.get_security_group_interface(group, target)

    if state == "absent" or state == "detach":
        if "id" in check:
            result = security.remove_interface_security_group(group, target)
            if "errors" in result:
                module.fail_json(msg=result)

            payload = {"security_group": group, "status": "detached"}
            module.exit_json(changed=True, msg=payload)

        payload = {"security_group": group, "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        if "id" in check:
            module.exit_json(changed=False, msg=check)

        result = security.add_interface_security_group(
            interface=target,
            security_group=group,
            instance=vsi)

        if "errors" in result:
            module.fail_json(msg=result)

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
