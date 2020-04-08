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
module: ic_is_instance_volume_info
short_description: Retrieve volume attachments from a VSI.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Retrieve volume attachments from volumes attached to VSI (Virtual Server
      Instance) on IBM Cloud.
notes:
    - The result contains a list of volumes.
requirements:
    - "ibmcloud-python-sdk"
options:
    instance:
        description:
            - Instance UUID or name.
        required: true
    attachment:
        description:
            - Volume attachment name.
        required: false
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Retrieve volume attachments from a VSI
- ic_is_instance_volume_info:
    instance: ibmcloud-vsi-baby

# Retrieve specific volume attachment from a VSI and register the value
- ic_is_instance_volume_info:
    instance: ibmcloud-vsi-baby
    attachment: ibmcloud-volume-baby
  register: attachment

# Display attachment registered value
- debug:
    var: attachment
'''


def run_module():
    module_args = dict(
        instance=dict(
            type='str',
            required=True),
        attachment=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    instance = sdk.Instance()

    name = module.params['instance']
    attachment = module.params['attachment']

    if attachment:
        result = instance.get_instance_volume_attachment(name, attachment)
        if "errors" in result:
            module.fail_json(msg=result["errors"])
    else:
        result = instance.get_instance_volume_attachments(name)
        if "errors" in result:
            module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
