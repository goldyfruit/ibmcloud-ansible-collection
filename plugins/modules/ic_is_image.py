#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import image as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_image
short_description: Manage VPC VSI images on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module creates a new image from an image prototype object.
    The prototype object is structured in the same way as a retrieved image,
    and contains the information necessary to create the new image.
  - A URL to the image file on object storage must be provided.
notes:
  - The image should be first uploaded into the Cloud Object Storage (COS).
requirements:
  - "ibmcloud-python-sdk"
options:
  image:
    description:
      - The unique user-defined name for this image.
    type: str
    required: true
  resource_group:
    description:
      - The resource group to use. If unspecified, the account's default
        resource group is used.
    type: str
  file:
    description:
      - The file from which to create the image.
    type: str
  format:
    description:
      - The format of the image and the image file.
    type: str
    choices: [box, ova, qcow2, raw, vdi, vhd, vhdx, vmdk]
  source_volume:
    description:
      - The volume from which to create the image.
    type: str
  operating_system:
    description:
      - The unique name of the operating system.
    type: str
  state:
    description:
      - Should the resource be present or absent.
    type: str
    default: present
    choices: [present, absent]
'''

EXAMPLES = r'''
- name: Create an image based on COS object
  ic_is_image:
    image: ibmcloud-image-baby
    file: cos://us-south/ibmcloud-bucket-baby/CentOS-8.1.1911.x86_64.qcow2
    format: qcow2
    operating_system: centos-7-amd64

- name: Delete an image
  ic_is_image:
    image: ibmcloud-image-baby
    state: absent
'''


def run_module():
    module_args = dict(
        image=dict(
            type='str',
            required=False),
        resource_group=dict(
            type='str',
            required=False),
        file=dict(
            type='str',
            required=False),
        format=dict(
            type='str',
            choices=['box', 'ova', 'qcow2', 'raw', 'vdi', 'vhd',
                     'vhdx', 'vmdk'],
            required=False),
        operating_system=dict(
            type='str',
            required=False),
        source_volume=dict(
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

    vsi_image = sdk.Image()

    image = module.params['image']
    resource_group = module.params['resource_group']
    file = module.params['file']
    format = module.params['format']
    operating_system = module.params['operating_system']
    source_volume = module.params['source_volume']
    state = module.params['state']

    check = vsi_image.get_image(image)

    if state == "absent":
        if "id" in check:
            result = vsi_image.delete_image(image)
            if "errors" in result:
                module.fail_json(msg=result)

            payload = {"image": image, "status": "deleted"}
            module.exit_json(changed=True, msg=payload)

        payload = {"image": image, "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        if "id" in check:
            module.exit_json(changed=False, msg=check)

        result = vsi_image.create_image(
            name=image,
            resource_group=resource_group,
            file=file,
            format=format,
            operating_system=operating_system,
            source_volume=source_volume
        )

        if "errors" in result:
            module.fail_json(msg=result)

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
