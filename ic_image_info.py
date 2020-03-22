#!/usr/bin/env python

# GNU General Public License v3.0+


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk import image as ic


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_image_info
short_description: Retrieve information about images
author: James Regis
version_added: "2.9"
description:
    - Retrieve information about images from IBM Cloud.
notes:
    - The result contains a list of images.
requirements:
    - "python >= 3.6"
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
- ic_image_info:

# Retrieve image list and register the value
- ic_image_info:
  register: images

# Display images registered value
- debug:
    var: images

# Retrieve a specific image by ID or by name
- ic_image_info:
    image: r006-ea930372-2abd-4aa1-bf8c-3db3ac8cb765
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

    image = ic.Image()

    if module.params['image']:
        result = image.get_image_by_name(module.params['image'])
        if "errors" in result:
            result = image.get_image_by_id(module.params['image'])
            if "errors" in result:
                module.fail_json(msg="image not found")
    else:
        result = image.get_images()
        if "errors" in result:
            module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
