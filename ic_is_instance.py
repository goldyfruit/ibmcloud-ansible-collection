#!/usr/bin/env python

# GNU General Public License v3.0+

from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk import instance as ic


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_is_instance
short_description: Create or delete VSI (Virtual Server Instance).
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Create or delete VSI (Virtual Server Instance) on IBM Cloud.
requirements:
    - "python >= 3.6"
    - "ibmcloud-python-sdk"
options:
    instance:
        description:
            - Name or UUID that has to be given to the instance to create
               or delete.
        required: true
    keys:
        description:
            - The public SSH keys to install on the virtual server instance.
                Up to 10 keys may be provided, name or UUID could be used.
        required: false
    profile:
        description:
            - The profile name to use for this virtual server instance.
        required: true
    resource_group:
        description:
            - Name or UUID of the resource group where the instance has to
               be created.
        required: false
    user_data:
        description:
            - User data to be made available when setting up the virtual
               server instance.
        required: false
    vpc:
        description:
            - Name or UUID of the VPC the virtual server instance is to be
               a part of.
        required: false
    image:
        description:
            - Name or UUID of the image to be used when provisioning
               the virtual server instance.
        required: true
    pni_subnet:
        description:
            - Name or UUID of associated subnet where the virtual instance
               will be part of, "PNI" stands for Primary Network Instance.
        required: true
    zone:
        description:
            - Name of the zone to provision the virtual server instance in.
        required: true
    state:
        description:
            - Should the resource be present or absent.
        required: false
        choices: [present, absent]
        default: present
extends_documentation_fragment:
    - ibmcloud
'''

EXAMPLES = '''
# Create instance (VSI)
- ic_is_instance:
    instance: ibmcloud-vsi
    keys:
      - ibmcloud-ssh-key
    profile: mp2-56x448
    image: ibm-redhat-7-6-minimal-amd64-1
    pni_subnet: advisory-subnet
    zone: us-south-3

# Create instance within a specific VPC
- ic_is_instance:
    instance: ibmcloud-vsi
    keys:
      - ibmcloud-ssh-key
    profile: mp2-56x448
    resource_group: advisory
    vpc: advisory
    image: ibm-redhat-7-6-minimal-amd64-1
    pni_subnet: advisory-subnet
    zone: us-south-3

# Delete instance
- ic_is_instance:
    instance: ibmcloud-vsi
    state: absent
'''


def run_module():
    module_args = dict(
        instance=dict(
            type='str',
            required=True),
        keys=dict(
            type='list',
            required=False),
        profile=dict(
            type='str',
            required=True),
        resource_group=dict(
            type='str',
            required=False),
        user_data=dict(
            type='str',
            required=False),
        vpc=dict(
            type='str',
            required=False),
        image=dict(
            type='str',
            required=True),
        pni_subnet=dict(
            type='str',
            required=True),
        zone=dict(
            type='str',
            required=True),
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

    instance = ic.Instance()

    name = module.params['instance']
    keys = module.params['keys']
    profile = module.params['profile']
    resource_group = module.params["resource_group"]
    user_data = module.params['user_data']
    vpc = module.params['vpc']
    image = module.params['image']
    pni_subnet = module.params['pni_subnet']
    zone = module.params['zone']

    if module.params["state"] == "absent":
        result = instance.delete_instance(name)

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "not_found":
                    module.fail_json(msg=result["errors"])
                else:
                    module.exit_json(changed=False, msg=(
                        f"instance {name} doesn't exist"))

        module.exit_json(changed=True, msg=(
            f"instance {name} successfully deleted"))

    else:
        result = instance.create_instance(name=name,
                                          keys=keys,
                                          profile=profile,
                                          resource_group=resource_group,
                                          user_data=user_data,
                                          vpc=vpc,
                                          image=image,
                                          pni_subnet=pni_subnet,
                                          zone=zone)

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "validation_unique_failed":
                    module.fail_json(msg=result["errors"])
                else:
                    exist = instance.get_instance_by_name(name)
                    if "errors" in exist:
                        module.fail_json(msg=exist["errors"])
                    else:
                        module.exit_json(changed=False, msg=(exist))

        module.exit_json(changed=True, msg=(result))


def main():
    run_module()


if __name__ == '__main__':
    main()
