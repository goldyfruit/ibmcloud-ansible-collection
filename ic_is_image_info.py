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
module: ic_is_image_info
short_description: Retrieve VPC VSI images on IBM Cloud.
author: James Regis (@jregis)
version_added: "2.9"
description:
  - An image provides source data for a volume. Images are either
    system-provided, or created from another source, such as importing from
    object storage.
notes:
  - The result contains a list of images.
requirements:
  - "ibmcloud-python-sdk"
options:
  image:
    description:
      - Restrict results to image with ID or name matching.
    type: str
'''

EXAMPLES = r'''
- name: Retrieve image list
  ic_is_image_info:

- name: Retrieve specific image
  ic_is_image_info:
    image: ibm-redhat-7-6-minimal-amd64-1
'''


def run_module():
    module_args = dict(
        image=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    vsi_image = sdk.Image()

    image = module.params['image']

    if image:
        result = vsi_image.get_image(image)
        if "errors" in result:
            module.fail_json(msg=result["errors"])
    else:
        result = vsi_image.get_images()
        if "errors" in result:
            module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
