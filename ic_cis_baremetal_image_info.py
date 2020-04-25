#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.cis.baremetal import order as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_cis_baremetal_image_info
short_description: Retrieve CIS baremetal images on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - Retrieves operating systems (images) available per baremetal packages.
  - If no package is specified then default package C(BARE_METAL_SERVER) will
    be used.
notes:
  - The result contains a list of images.
requirements:
  - "ibmcloud-python-sdk"
options:
  package:
    description:
      - Package name.
    type: str
  image:
    description:
      - Image name from the package.
    type: str
'''

EXAMPLES = r'''
- name: Retrieve baremetal images
  ic_cis_baremetal_image_info:

- name: Retrieve baremetal images for a specific package
  ic_cis_baremetal_image_info:
    package: ibmcloud-package-baby

- name: Retrieve baremetal specific image for a specific package
  ic_cis_baremetal_image_info:
    package: ibmcloud-package-baby
    image: ibmcloud-package-image-baby
'''


def run_module():
    module_args = dict(
        package=dict(
            type='str',
            required=False),
        image=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    order = sdk.Order()

    package = module.params['package']
    image = module.params['image']

    result = None
    if package:
        if image:
            result = order.get_operating_system(image, package.upper())
        else:
            result = order.get_operating_systems(package.upper())
    else:
        if image:
            result = order.get_operating_system(image)
        else:
            result = order.get_operating_systems()

    if "errors" in result:
        module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
