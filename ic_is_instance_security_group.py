#!/usr/bin/env python

# GNU General Public License v3.0+

from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import security as sdk_security
from ibmcloud_python_sdk.vpc import instance as sdk_instance


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_is_instance_security_group
short_description: Attach or detach a security group from a VSI.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Attach or detach a security group from VSI (Virtual Server Instance)
      on IBM Cloud.
requirements:
    - "ibmcloud-python-sdk"
options:
    instance:
        description:
            - Instance name or ID where to attach the security group. If no
              interface is provide then ecurity group will be attached to
              primary network interface.
        required: false
    interface:
        description:
            -  Interface name or ID where to attach the security group on
               the instance.
        required: false
    group:
        description:
            -  The identity of the security group to attach to the
               instance/interface.
        required: true
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
# Attach security group to VSI's primary network interface
- ic_is_instance_security_group:
    instance: ibmcloud-vsi-baby
    group: ibmcloud-sec-group-baby

# Attach security group on specific VSI's network interface
- ic_is_instance_security_group:
    instance: ibmcloud-vsi-baby
    interface: ibmcloud-interface-baby
    group: ibmcloud-sec-group-baby

# Detach security group from VSI's primary network interface
- ic_is_instance_security_group:
    instance: ibmcloud-vsi-baby
    group: ibmcloud-sec-group-baby
    state: absent

# Detach security group from specific VSI's network interface
- ic_is_instance_security_group:
    instance: ibmcloud-vsi-baby
    interface: ibmcloud-interface-baby
    group: ibmcloud-sec-group-baby
    state: absent
'''

security = sdk_security.Security()
instance = sdk_instance.Instance()


def run_module():
    module_args = dict(
        instance=dict(
            type='str',
            required=False),
        interface=dict(
            type='str',
            required=False),
        group=dict(
            type='str',
            required=True),
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

    name = module.params["group"]
    vsi = module.params["instance"]
    interface = module.params["interface"]
    state = module.params["state"]

    target = None
    if not interface:
        instance_info = instance.get_instance(vsi)
        if "errors" in instance_info:
            module.fail_json(msg=instance_info["errors"])
        target = instance_info["primary_network_interface"]["id"]
    else:
        nic_info = instance.get_instance_interface(vsi, interface)
        if "errors" in nic_info:
            module.fail_json(msg=nic_info["errors"])
        target = nic_info["id"]

    if state == "absent" or state == "detach":
        result = security.remove_interface_security_group(name, target)
        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "not_found":
                    module.fail_json(msg=result["errors"])
                else:
                    module.exit_json(changed=False, msg=(
                        "security group {} is not attach to {}").format(
                            name, target))

        module.exit_json(changed=True, msg=(
            "security group {} successfully detached from {}".format(
                name, target)))
    else:

        result = security.add_interface_security_group(
            interface=target,
            security_group=name,
            instance=vsi)

        if "errors" in result:
            module.fail_json(msg=result["errors"])

        module.exit_json(changed=True, msg=(result))


def main():
    run_module()


if __name__ == '__main__':
    main()
