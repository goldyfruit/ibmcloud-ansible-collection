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
module: ic_is_instance_volume
short_description: Manage VPC volume attachment to VSI on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - The prototype object is structured in the same way as a retrieved volume
    attachment, and contains the information necessary to create the new volume
    attachment. The creation of a new volume attachment connects a volume to an
    instance.
requirements:
  - "ibmcloud-python-sdk"
options:
  instance:
    description:
      - VSI (Virtual Server Instance) where to attach the volume.
    type: str
    required: true
  volume:
    description:
      - The identity of the volume to attach to the instance.
    type: str
    required: true
  attachment_name:
    description:
      - The user-defined name for this volume attachment.
    type: str
    required: true
  delete_volume_on_instance_delete:
    description:
      - If set to true, when deleting the instance the volume will
       also be deleted.
    type: bool
    choices: [true, false]
  state:
    description:
      - Should the resource be present or absent.
    type: str
    default: detach
    choices: [present, absent, attach, detach]
'''

EXAMPLES = r'''
- name: Attach volume to the VSI
  ic_is_instance_volume:
    instance: ibmcloud-vsi-baby
    volume: ibmcloud-volume-baby
    attachment_name: ibmcloud-attachment-baby

- name: Detach volume from VSI
  ic_is_instance_volume:
    instance: ibmcloud-vsi-baby
    volume: ibmcloud-volume-baby
    attachment_name: ibmcloud-attachment-baby
    state: detach
'''


vsi_instance = sdk.Instance()


def _get_attachment(instance, volume):
    data = vsi_instance.get_instance_volume_attachments(instance)
    if "errors" in data:
        return data

    for attachment in data["volume_attachments"]:
        info = attachment["volume"]
        if info["name"] == volume or info["id"] == volume:
            return attachment["id"]


def run_module():
    module_args = dict(
        instance=dict(
            type='str',
            required=True),
        volume=dict(
            type='str',
            required=True),
        attachment_name=dict(
            type='str',
            required=True),
        delete_volume_on_instance_delete=dict(
            type='bool',
            required=False,
            choices=[True, False]),
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

    instance = module.params["instance"]
    volume = module.params["volume"]
    attachment_name = module.params["attachment_name"]
    delete = module.params["delete_volume_on_instance_delete"]
    state = module.params["state"]

    check = vsi_instance.get_instance_volume_attachment(instance,
                                                        attachment_name)

    if state == "absent" or state == "detach":
        if "id" in check:
            if not attachment_name:
                attachment_name = _get_attachment(instance, volume)

            result = vsi_instance.detach_volume(instance, attachment_name)
            if "errors" in result:
                module.fail_json(msg=result)

            payload = {"volume": volume, "status": "detached"}
            module.exit_json(changed=True, msg=payload)

        payload = {"volume": volume, "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        if "id" in check:
            module.exit_json(changed=False, msg=check)

        result = vsi_instance.attach_volume(
            instance=instance,
            volume=volume,
            delete_volume_on_instance_delete=delete,
            name=attachment_name)

        if "errors" in result:
            module.fail_json(msg=result)

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
