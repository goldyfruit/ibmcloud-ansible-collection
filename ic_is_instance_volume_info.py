#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import instance as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_instance_volume_info
short_description: Retrieve attached volumes from a VSI on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - A volume attachment connects a volume to an instance. Each instance may
    have many volume attachments but each volume attachment connects exactly
    one instance to exactly one volume.
notes:
  - The result contains a list of volume attachements and their volumes.
requirements:
  - "ibmcloud-python-sdk"
options:
  instance:
    description:
      - VSI (Virtual Server Instance) name or ID.
    type: str
    required: true
  attachment:
    description:
      - The volume attachment identifier.
    type: str
'''

EXAMPLES = r'''
- name: Retrieve volume attachments from a VSI
  ic_is_instance_volume_info:
    instance: ibmcloud-vsi-baby

- name: Retrieve specific volume attachment from a VSI
  ic_is_instance_volume_info:
    instance: ibmcloud-vsi-baby
    attachment: ibmcloud-volume-attachment-baby
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

    vsi_instance = sdk.Instance()

    instance = module.params['instance']
    attachment = module.params['attachment']

    if attachment:
        result = vsi_instance.get_instance_volume_attachment(instance,
                                                             attachment)
        if "errors" in result:
            module.fail_json(msg=result)
    else:
        result = vsi_instance.get_instance_volume_attachments(instance)
        if "errors" in result:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
