#!/usr/bin/env python

# GNU General Public License v3.0+


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import image as sdk_image


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_is_image_info
short_description: Retrieve information VSI (Virtual Server Instance) images.
author: James Regis (jregis)
version_added: "2.9"
description:
    - Retrieve information about VSI (Virtual Server Instance) images from
      IBM Cloud.
notes:
    - The result contains a list of images.
requirements:
    - "ibmcloud-python-sdk"
options:
    image:
        description:
            - Restrict results to image with UUID or name matching.
        required: false
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Retrieve image list
- ic_is_image_info:

# Retrieve image list and register the value
- ic_is_image_info:
  register: images

# Display images registered value
- debug:
    var: images

# Retrieve a specific image by ID or by name
- ic_is_image_info:
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

    image = sdk_image.Image()

    name = module.params['image']

    if name:
        result = image.get_image(name)
        if "errors" in result:
            module.fail_json(msg=result["errors"])
    else:
        result = image.get_images()
        if "errors" in result:
            module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
