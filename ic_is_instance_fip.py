#!/usr/bin/env python

# GNU General Public License v3.0+

from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import instance as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_is_instance_fip
short_description: Attach or detach a floating IP from VSI.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Attach or detach a floating IP from VSI (Virtual Server Instance)
      on IBM Cloud.
requirements:
    - "ibmcloud-python-sdk"
options:
    instance:
        description:
            -  Instance name or ID
        required: true
    floatin_ip:
        description:
            -  The floating IP to attach on the VSI's network interface.
        required: false
    interface:
        description:
            - Network interface where the floating IP should be binded. If
              no interface is provided the binding will happened on the
              primary network interface.
        required: false
    state:
        description:
            - Should the resource be present or absent.
        required: false
        choices: [present, absent, attach, detach]
        default: present
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Attach floating IP on VSI's primary network interface
- ic_is_instance_fip:
    instance: ibmcloud-vsi-baby
    floating_ip: ibmcloud-vip-baby

# Attach floating IP on VSI specific interface
- ic_is_instance_fip:
    instance: ibmcloud-vsi-baby
    floating_ip: ibmcloud-vip-baby
    interface: ibmclouc-nic-baby

# Detach floating IP from VSI
- ic_is_instance_fip:
    instance: ibmcloud-instance-baby
    floating_ip: ibmcloud-vip-baby
    state: absent
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
            default='present',
            choices=['absent', 'present', 'attach', 'detach'],
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    instance = sdk.Instance()

    name = module.params["instance"]
    floating_ip = module.params["floating_ip"]
    interface = module.params["interface"]
    state = module.params["state"]

    if not interface:
        instance_info = instance.get_instance(name)
        interface = instance_info["primary_network_interface"]["id"]

    if state == "absent" or state == "detach":
        result = instance.disassociate_floating_ip(
            name, interface, floating_ip)

        if "errors" in result:
            module.fail_json(msg=result["errors"])

        module.exit_json(changed=True, msg=(
            "fip {} successfully disassociated from {}").format(
                floating_ip, name))

    else:
        result = instance.associate_floating_ip(
            instance=name,
            interface=interface,
            fip=floating_ip)

        if "errors" in result:
            module.fail_json(msg=result["errors"])

        module.exit_json(changed=True, msg=(result))


def main():
    run_module()


if __name__ == '__main__':
    main()
