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
module: ic_is_instance
short_description: Manage VPC VSI (Virtual Server Instance) on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - The prototype object is structured in the same way as a retrieved instance,
    and contains the information necessary to provision the new instance. The
    instance is automatically started.
requirements:
  - "ibmcloud-python-sdk"
options:
  instance:
    description:
      - The unique user-defined name for this virtual server instance
        (and default system hostname).
    type: str
    required: true
  keys:
    description:
      - The public SSH keys to install on the virtual server instance. Up to 10
        keys may be provided; if no keys are provided the instance will be
        inaccessible unless the image used provides a means of access.
        For Windows instances, one of the keys will be used to encrypt the
        administrator password.
    type: list
  network_interfaces:
    description:
      - Collection of additional network interfaces to create for the virtual
        server instance.
    type: list
    suboptions:
      allow_ip_spoofing:
        description:
          - Indicates whether source IP spoofing is allowed on this interface.
            If false, source IP spoofing is prevented on this interface.
            If true,source IP spoofing is allowed on this interface.
        type: bool
        choices: [true, false]
      ips:
        description:
          - Array of additional IP addresses to bind to the network interface.
        type: list
      name:
        description:
          - The user-defined name for network interface.
        type: str
      primary_ip:
        description:
          - Primary IP address to bind to the network interface.
        type: str
      security_groups:
        description:
          - Collection of security groups.
        type: list
      subnet:
        description:
          - The associated subnet.
        type: str
        required: true
  placement_target:
    description:
      - The placement for the virtual server instance.
    type: str
  volume_attachments:
    description:
      - Collection of volume attachments
    type: list
    suboptions:
      delete_volume_on_instance_delete:
        description:
          - If set to true, when deleting the instance the volume will also
            be deleted.
        type: bool
        choices: [true, false]
      name:
        description:
          - The user-defined name for this volume attachment.
        type: str
      volume:
        description:
          - The identity of the volume to attach to the instance.
        type: str
        required: true
  boot_volume_attachment:
    description:
      - The boot volume attachment for the virtual server instance
    type: dict
    suboptions:
      delete_volume_on_instance_delete:
        description:
          - If set to true, when deleting the instance the volume will also
            be deleted.
        type: bool
        choices: [true, false]
      name:
        description:
          - The user-defined name for this volume attachment.
        type: str
      volume:
        description:
          - The identity of the volume to attach to the instance.
        type: dict
        required: true
        suboptions:
          capacity:
            description:
              - The capacity of the volume in gigabytes.
            type: int
          encryption_key:
            description:
              - The key to use for encrypting this volume. If no encryption key
                is provided, the volume's encryption will be provider-managed.
            type: str
          iops:
            description:
              - The bandwidth for the volume.
            type: int
          name:
            description:
              - The unique user-defined name for this volume
            type: str
          profile:
            description:
              - The profile name to use for this volume.
            type: str
  primary_network_interface:
    description:
      - Primary network interface.
    type: dict
    required: true
    suboptions:
      ips:
        description:
          - Array of additional IP addresses to bind to the network interface.
        type: list
      name:
        description:
          - The user-defined name for network interface.
        type: str
      primary_ip:
        description:
          - Primary IP address to bind to the network interface.
        type: str
      security_groups:
        description:
          - Collection of security groups.
        type: list
      subnet:
        description:
          - The associated subnet.
        type: str
        required: true
  source_template:
    description:
      - Identifies an instance template by a unique property.
    type: str
  profile:
    description:
      - The profile to use for this virtual server instance.
    type: str
    required: true
  resource_group:
    description:
      - The resource group to use. If unspecified, the account's default
        resource group is used.
    type: str
  user_data:
    description:
      - User data to be made available when setting up the virtual server
        instance.
    type: str
  vpc:
    description:
      - The VPC the virtual server instance is to be a part of. If provided,
        must match the VPC tied to the subnets of the instance's network
        interfaces.
    type: str
  image:
    description:
      - The identity of the image to be used when provisioning the virtual
        server instance.
    type: str
    required: true
  pni_subnet:
    description:
      - Name or UUID of associated subnet where the virtual instance
        will be part of, "PNI" stands for Primary Network Instance.
    required: true
  zone:
    description:
      - The identity of the zone to provision the virtual server instance in.
    type: str
    required: true
  state:
    description:
      - Should the resource be present or absent.
    type: str
    default: present
    choices: [present, absent]
'''

EXAMPLES = r'''
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
        network_interfaces=dict(
            type='list',
            options=dict(
                allow_ip_spoofing=dict(
                    type='bool',
                    required=False,
                    choices=[True, False]),
                ips=dict(
                    type='list',
                    required=False),
                name=dict(
                    type='str',
                    required=False),
                primary_ip=dict(
                    type='list',
                    required=False),
                security_groups=dict(
                    type='list',
                    required=False),
                subnet=dict(
                    type='str',
                    required=True),
            ),
            required=False),
        placement_target=dict(
            type='str',
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
        volume_attachments=dict(
            type='list',
            options=dict(
                delete_volume_on_instance_delete=dict(
                    type='bool',
                    required=False,
                    choices=[True, False]),
                name=dict(
                    type='str',
                    required=False),
                volume=dict(
                    type='str',
                    required=True),
            ),
            required=False),
        boot_volume_attachment=dict(
            type='dict',
            options=dict(
                delete_volume_on_instance_delete=dict(
                    type='bool',
                    required=False,
                    choices=[True, False]),
                name=dict(
                    type='str',
                    required=False),
                volume=dict(
                    type='dict',
                    options=dict(
                        capacity=dict(
                            type='int',
                            required=False),
                        encryption_key=dict(
                            type='str',
                            required=False),
                        iops=dict(
                            type='int',
                            required=False),
                        name=dict(
                            type='str',
                            required=False),
                        profile=dict(
                            type='str',
                            required=True),
                    ),
                    required=False),
            ),
            required=False),
        source_template=dict(
            type='str',
            required=False),
        vpc=dict(
            type='str',
            required=False),
        image=dict(
            type='str',
            required=True),
        primary_network_interface=dict(
            type='dict',
            options=dict(
                ips=dict(
                    type='list',
                    required=False),
                name=dict(
                    type='str',
                    required=False),
                primary_ip=dict(
                    type='list',
                    required=False),
                security_groups=dict(
                    type='list',
                    required=False),
                subnet=dict(
                    type='str',
                    required=True),
            ),
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

    vsi_instance = sdk.Instance()

    instance = module.params['instance']
    keys = module.params['keys']
    network_interfaces = module.params['network_interfaces']
    placement_target = module.params['placement_target']
    volume_attachments = module.params['volume_attachments']
    boot_volume_attachment = module.params['boot_volume_attachment']
    source_template = module.params['source_template']
    profile = module.params['profile']
    resource_group = module.params["resource_group"]
    user_data = module.params['user_data']
    vpc = module.params['vpc']
    image = module.params['image']
    primary_network_interface = module.params['primary_network_interface']
    zone = module.params['zone']
    state = module.params["state"]

    check = vsi_instance.get_instance(instance)

    if state == "absent":
        if "id" in check:
            result = vsi_instance.delete_instance(instance)
            if "errors" in result:
                module.fail_json(msg=result)

            payload = {"instance": instance, "status": "deleted"}
            module.exit_json(changed=True, msg=payload)

        payload = {"instance": instance, "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        if "id" in check:
            module.exit_json(changed=False, msg=check)

        result = vsi_instance.create_instance(
            name=instance,
            keys=keys,
            profile=profile,
            network_interfaces=network_interfaces,
            placement_target=placement_target,
            volume_attachments=volume_attachments,
            boot_volume_attachment=boot_volume_attachment,
            source_template=source_template,
            resource_group=resource_group,
            user_data=user_data,
            vpc=vpc,
            image=image,
            primary_network_interface=primary_network_interface,
            zone=zone
        )

        if "errors" in result:
            module.fail_json(msg=result)

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
