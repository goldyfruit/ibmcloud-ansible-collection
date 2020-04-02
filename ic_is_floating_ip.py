#!/usr/bin/env python

# GNU General Public License v3.0+

from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import floating_ip as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_is_floating_ip
short_description: Reserve or release floating IP.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Reserver or release floating IP on IBM Cloud.
requirements:
    - "ibmcloud-python-sdk"
options:
    fip:
        description:
            -  Name that has to be given to the floating IP to reserve
                or release.
                During the removal an UUID or the address could be used.
        required: true
    resource_group:
        description:
            -  Name or UUID of the resource group where the floating IP has to
               be created.
        required: false
    target:
        description:
            -  The target this address is to be bound to.
        required: false
    zone:
        description:
            -  The identity of the zone to provision a floating IP in.
        required: false
    state:
        description:
            - Should the resource be present, absent, attach or detach.
        required: false
        choices: [present, absent, attach, detach]
        default: present
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Reserve floating IP within a zone
- ic_is_floating_ip:
    fip: ibmcloud-fip-baby
    zone: us-south-3

# Reserve floating IP for a VSI (Virtual Server Instance) network interface
- ic_is_floating_ip:
    fip: ibmcloud-fip-baby
    target: r006-9914cbf3-f7cd-42dd-8e6f-bdbf902ca559

# Release floating IP
- ic_is_floating_ip:
    fip: 129.129.10.10
    state: absent
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
            choices=['absent', 'present', 'attach', 'detach'],
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    fip = sdk.Fip()

    name = module.params["fip"]
    resource_group = module.params["resource_group"]
    target = module.params["target"]
    zone = module.params["zone"]
    state = module.params["state"]

    if state == "absent" or state == "detach":
        result = fip.release_floating_ip(name)

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "not_found":
                    module.fail_json(msg=result["errors"])
                else:
                    module.exit_json(changed=False, msg=(
                        "floating IP {} doesn't exist")).format(name)

        module.exit_json(changed=True, msg=(
            "floating IP {} successfully release")).format(name)

    else:

        result = fip.reserve_floating_ip(
            name=name,
            resource_group=resource_group,
            target=target,
            zone=zone)

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "validation_unique_failed":
                    module.fail_json(msg=result["errors"])
                else:
                    exist = fip.get_floating_ip(name)
                    if "errors" in exist:
                        module.fail_json(msg=exist["errors"])
                    else:
                        module.exit_json(changed=False, msg=(exist))

        module.exit_json(changed=True, msg=(result))


def main():
    run_module()


if __name__ == '__main__':
    main()
