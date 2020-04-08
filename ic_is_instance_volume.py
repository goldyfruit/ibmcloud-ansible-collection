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
module: ic_is_instance_volume
short_description: Attach or detach a volume from a VSI.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Attach or detach a volume from VSI (Virtual Server Instance)
      on IBM Cloud.
requirements:
    - "ibmcloud-python-sdk"
options:
    instance:
        description:
            - Instance name or ID where to attach the volume.
        required: true
    volume:
        description:
            -  The identity of the volume to attach to the instance.
        required: false
    attachment_name:
        description:
            - The user-defined name for this volume attachment.
        required: false
    delete_volume_on_instance_delete:
        description:
            - If set to true, when deleting the instance the volume will
              also be deleted.
        required: false
    state:
        description:
            - Should the resource be present or absent.
        required: false
        choices: [present, absent, attach, detach]
        default: present
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Attach volume with random attachment name
- ic_is_instance_volume:
    instance: ibmcloud-vsi-baby
    volume: ibmcloud-volume-baby
    delete_volume_on_instance_delete: false

# Attach volume with defined attachment name
- ic_is_instance_volume:
    instance: ibmcloud-vsi-baby
    volume: ibmcloud-volume-baby
    attachment_name: ibmcloud-attach-baby
    delete_volume_on_instance_delete: false

# Detach volume by using volume name or ID
- ic_is_instance_volume:
    instance: ibmcloud-instance-baby
    volume: ibmcloud-volume-baby
    state: absent

# Detach volume by using volume attachment name
- ic_is_instance_volume:
    instance: ibmcloud-instance-baby
    attachment_name: ibmcloud-attach-baby
    state: absent
'''

instance = sdk.Instance()


def _get_attachment(name, volume):
    data = instance.get_instance_volume_attachments(name)
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
            required=False),
        attachment_name=dict(
            type='str',
            required=False),
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

    name = module.params["instance"]
    volume = module.params["volume"]
    attachment_name = module.params["attachment_name"]
    delete = module.params["delete_volume_on_instance_delete"]
    state = module.params["state"]

    if state == "absent" or state == "detach":
        result = None
        if attachment_name:
            result = instance.detach_volume(name, attachment_name)
        else:
            attachment_id = _get_attachment(name, volume)
            result = instance.detach_volume(name, attachment_id)

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "not_found":
                    module.fail_json(msg=result["errors"])
                else:
                    module.exit_json(changed=False, msg=(
                        "volume {} is not attach to instance {}").format(
                            volume, name))

        module.exit_json(changed=True, msg=(
            "volume successfully detached from {}").format(name))
    else:
        check = instance.get_instance_volume_attachment(name, attachment_name)
        if "status" in check:
            module.exit_json(changed=False, msg=(check))

        result = instance.attach_volume(
            instance=name,
            volume=volume,
            delete_volume_on_instance_delete=delete,
            name=attachment_name)

        if "errors" in result:
            module.fail_json(msg=result["errors"])

        module.exit_json(changed=True, msg=(result))


def main():
    run_module()


if __name__ == '__main__':
    main()
