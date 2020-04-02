#!/usr/bin/env python

# GNU General Public License v3.0+

from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import volume as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_is_volume
short_description: Create or delete volume.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Create or delete volume on IBM Cloud.
requirements:
    - "ibmcloud-python-sdk"
options:
    volume:
        description:
            -  Name that has to be given to the volume to create or delete.
                During the removal an UUID could be used.
        required: true
    resource_group:
        description:
            -  Name or UUID of the resource group where the volume has to
               be created.
        required: false
    iops:
        description:
            -  The bandwidth for the volume.
        required: false
    capacity:
        description:
            -  The capacity of the volume in gigabytes.
        required: false
    profile:
        description:
            -  The profile to use for this volume.
        required: false
    zone:
        description:
            -  The location of the volume.
        required: false
    state:
        description:
            - Should the resource be present or absent.
        required: false
        choices: [present, absent]
        default: present
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Create volume
- ic_is_volume:
    volume: ibmcloud-baby
    resouge_group: advisory

# Create VPC without address prefix
- ic_is_volume:
    vpc: ibmcloud-baby
    resouge_group: advisory
    address_prefix_management: true

# Delete volume
- ic_is_volume:
    volume: ibmcloud-volume-baby
    resouge_group: advisory
    state: absent
'''


def run_module():
    module_args = dict(
        volume=dict(
            type='str',
            required=True),
        resource_group=dict(
            type='str',
            required=False),
        iops=dict(
            type='int',
            required=False),
        capacity=dict(
            type='int',
            required=False),
        profile=dict(
            type='str',
            required=False),
        zone=dict(
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

    volume = sdk.Volume()

    name = module.params["volume"]
    resource_group = module.params["resource_group"]
    iops = module.params["iops"]
    capacity = module.params["capacity"]
    profile = module.params["profile"]
    zone = module.params["zone"]
    state = module.params["state"]

    if state == "absent":
        result = volume.delete_volume(name)

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "not_found":
                    module.fail_json(msg=result["errors"])
                else:
                    module.exit_json(changed=False, msg=(
                        "volume {} doesn't exist")).format(name)

        module.exit_json(changed=True, msg=(
            "vpc {} successfully deleted")).format(name)

    else:
        result = volume.create_volume(name=name,
                                      resource_group=resource_group,
                                      iops=iops,
                                      capacity=capacity,
                                      profile=profile,
                                      zone=zone)

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "volume_name_duplicate":
                    module.fail_json(msg=result["errors"])
                else:
                    exist = volume.get_volume(name)
                    if "errors" in exist:
                        module.fail_json(msg=exist["errors"])
                    else:
                        module.exit_json(changed=False, msg=(exist))

        module.exit_json(changed=True, msg=(result))


def main():
    run_module()


if __name__ == '__main__':
    main()
