#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import volume as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_volume
short_description: Manage VPC volumes on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module creates a new volume from a volume prototype object. The
    prototype object is structured in the same way as a retrieved volume,
    and contains the information necessary to create the new volume.
requirements:
  - "ibmcloud-python-sdk"
options:
  volume:
    description:
      - The unique user-defined name for this volume.
    type: str
    required: true
  resource_group:
    description:
      - The resource group to use. If unspecified, the account's default
        resource group is used.
    type: str
  encryption_key:
    description:
      - The key to use for encrypting this volume. If no encryption key is
        provided, the volume's encryption will be provider-managed.
    type: str
  iops:
    description:
      - The bandwidth for the volume.
    type: int
  capacity:
    description:
      - The capacity of the volume in gigabytes.
    type: int
  profile:
    description:
      - The profile to use for this volume.
    type: str
  zone:
    description:
      - The location of the volume.
    type: str
  state:
    description:
      - Should the resource be present or absent.
  type: str
  default: present
  choices: [present, absent]
'''

EXAMPLES = r'''
- name: Create volume
  ic_is_volume:
    volume: ibmcloud-volume-baby
    profile: ibmcloud-volume-profile-baby
    capacity: 100
    zone: ibmcloud-zone-baby

- name: Delete volume
  ic_is_volume:
    volume: ibmcloud-volume-baby
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
        encryption_key=dict(
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

    vpc_volume = sdk.Volume()

    volume = module.params["volume"]
    resource_group = module.params["resource_group"]
    iops = module.params["iops"]
    capacity = module.params["capacity"]
    profile = module.params["profile"]
    zone = module.params["zone"]
    encryption_key = module.params["encryption_key"]
    state = module.params["state"]

    check = vpc_volume.get_volume(volume)

    if "id" in check:
        if state == "absent":
            result = vpc_volume.delete_volume(volume)
            if "errors" in result:
                module.fail_json(msg=result)

            payload = {"volume": volume, "status": "deleted"}
            module.exit_json(changed=True, msg=payload)

        payload = {"volume": volume, "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        if "id" in check:
            module.exit_json(changed=False, msg=check)

        result = vpc_volume.create_volume(
            name=volume,
            resource_group=resource_group,
            iops=iops,
            capacity=capacity,
            profile=profile,
            zone=zone,
            encryption_key=encryption_key
        )

        if "errors" in result:
            module.fail_json(msg=result)

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
