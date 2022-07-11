#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from email.policy import default
from random import choices
from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import baremetal as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_baremetal
short_description: Manage VPC Baremetal Server Instance) on IBM Cloud.
author: James Regis (@jamesregis)
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
      - The unique user-defined name for this physical server instance
        (and default system hostname).
    type: str
    required: true
  keys:
    description:
      - The public SSH keys to install on the physical server instance. Up to 10
        keys may be provided; if no keys are provided the instance will be
        inaccessible unless the image used provides a means of access.
        For Windows instances, one of the keys will be used to encrypt the
        administrator password.
    type: list
  network_interfaces:
    description:
      - Collection of additional network interfaces to create for the baremetal
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
      name:
        description:
          - The user-defined name for network interface.
        type: str
      interface_type:
        description:
          - Primary interface type (pci or vlan).
        type: str
        required: true
      security_groups:
        description:
          - Collection of security groups.
        type: list
      subnet:
        description:
          - The associated subnet.
        type: str
        required: true
      enable_infrastructure_nat:
        description:
          - When enabled, the VPC infrastructure performs any needed NAT operations.
            When disabled, the packet is passed unmodified to and from the network interface,
            allowing the workload to perform any needed NAT operations
        type: bool
        choices: [true, false]
        default: false
      vlan:
        description:
          - Collection of allowed vlans.
        type: str
        required: false
      allow_ip_spoofing:
        description:
          - To enable or disable 'Allow IP Spoofing'
        type: bool
        choices: [true, false]
  primary_network_interface:
    description:
      - Primary network interface.
    type: dict
    suboptions:
      name:
        description:
          - The user-defined name for network interface.
        type: str
      interface_type:
        description:
          - Primary interface type (pci or vlan).
        type: str
        required: true
      security_groups:
        description:
          - Collection of security groups.
        type: list
      subnet:
        description:
          - The associated subnet.
        type: str
        required: true
      allowed_vlans:
        description:
          - Collection of allowed vlans.
        type: list
      allow_ip_spoofing:
        description:
          - To enable or disable Allow IP Spoofing
        type: boolean
      enable_infrastructure_nat:
        description:
          - When enabled, the VPC infrastructure performs any needed NAT operations.
            When disabled, the packet is passed unmodified to and from the network interface,
            allowing the workload to perform any needed NAT operations
        type: boolean
        default: false
  source_template:
    description:
      - Identifies an instance template by a unique property.
    type: str
  profile:
    description:
      - The profile to use for this virtual server instance.
    type: str
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
  zone:
    description:
      - The identity of the zone to provision the virtual server instance in.
    type: str
  force:
    description:
      -  Ignore warnings and complete the actions.
      This parameter is useful while powering down a bare metal server which is powered on state.
    type: boolean
    choice: [true, false]
    default: false
  state:
    description:
      - Should the resource be present or absent.
    type: str
    default: present
    choices: [present, absent, poweredon, poweredoff, restart]
'''

EXAMPLES = r'''
- name: Create baremetal server
  ic_is_baremetal:
    instance: ibm-baremetal-baby
    keys:
      - ibmcloud-key1-baby
      - ibmcloud-key2-baby
    profile: ibmcloud-vsi-profile-baby
    vpc: ibmcloud-vpc-baby
    image: ibmcloud-image-baby
    primary_network_interface:
      name: eth0
      subnet: ibmcloud-subnet-baby
      interface_type: "pci"
      subnet: my-subnet
      security_groups:
        - my-sec-group-1
        - my-sec-group-2
        - my-sec-group-3
      allowed_vlans:
        - 118
        - 218
    network_interfaces:
      - name: eth1
        subnet: ibmcloud-subnet-baby
        interface_type: "pci"
        security_groups:
          - my-sec-group-1
          - my-sec-group-2
          - my-sec-group-3
      - name: eth2
        subnet: ibmcloud-subnet-baby
        interface_type: "pci"
        security_groups:
          - my-sec-group-1
          - my-sec-group-2
          - my-sec-group-3
    zone: ibmcloud-zone-baby

- name: Delete instance
  ic_is_baremetal:
    instance: ibmcloud-vsi-baby
    state: absent
    force: true
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
                interface_type=dict(
                    type='str',
                    required=False,
                    choices=["pci", "vlan"],
                    default="pci"),
                name=dict(
                    type='str',
                    required=False),
                allow_interface_to_float=dict(
                    type='bool',
                    choices=[True, False],
                    required=False,
                    default=True),
                security_groups=dict(
                    type='list',
                    required=False),
                subnet=dict(
                    type='str',
                    required=True),
                enable_infrastructure_nat=dict(
                    type='bool',
                    choices=[True, False],
                    required=False,
                    default=True),
                vlan=dict(
                    type='str',
                    required=False
                ),
            ),
            required=False),
        profile=dict(
            type='str',
            required=False),
        resource_group=dict(
            type='str',
            required=False),
        user_data=dict(
            type='str',
            required=False),
        source_template=dict(
            type='str',
            required=False),
        vpc=dict(
            type='str',
            required=False),
        image=dict(
            type='str',
            required=False),
        primary_network_interface=dict(
            type='dict',
            options=dict(
                allow_ip_spoofing=dict(
                    type='bool',
                    required=False,
                    choices=[True, False]),
                interface_type=dict(
                    type='str',
                    required=False,
                    choices=["pci", "vlan"],
                    default="pci"),
                name=dict(
                    type='str',
                    required=False),
                allow_interface_to_float=dict(
                    type='bool',
                    choices=[True, False],
                    required=False,
                    default=True),
                security_groups=dict(
                    type='list',
                    required=False),
                subnet=dict(
                    type='str',
                    required=True),
                enable_infrastructure_nat=dict(
                    type='bool',
                    choices=[True, False],
                    required=False,
                    default=True),
                allowed_vlans=dict(
                    type='list',
                    required=False
                ),
            ),
            required=False),
        zone=dict(
            type='str',
            required=False),
        enable_secure_boot=dict(
            type='bool',
            choices=[True, False],
            required=False,
            default=False),
        trusted_platform_module=dict(
            type='dict',
            required=False
        ),
        force=dict(
            type='bool',
            choices=[True, False],
            required=False,
            default=False),
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

    bm_instance = sdk.Baremetal()

    instance = module.params['instance']
    keys = module.params['keys']
    network_interfaces = module.params['network_interfaces']
    profile = module.params['profile']
    resource_group = module.params["resource_group"]
    user_data = module.params['user_data']
    vpc = module.params['vpc']
    image = module.params['image']
    primary_network_interface = module.params['primary_network_interface']
    trusted_platform_module = module.params['trusted_platform_module']
    enable_secure_boot = module.params['enable_secure_boot']
    zone = module.params['zone']
    force = module.params['force']
    state = module.params["state"]

    check = bm_instance.get_server(instance)

    if state == "absent":
        if "id" in check:
            if check["status"] == "running":
                stop_instance = bm_instance.create_server_action(
                    server=instance,
                    action="stop",
                    type="hard")
                if "errors" in stop_instance:
                    module.fail_json(msg=stop_instance)

            # wait until stop and after launch deletation
            result = bm_instance.delete_server(instance)
            if "errors" in result:
                module.fail_json(msg=result)

            payload = {"instance": instance, "status": "deleted"}
            module.exit_json(changed=True, msg=payload)

        payload = {"instance": instance, "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        if "id" in check and state == "poweredon":
            check_state = bm_instance.get_server(instance)[
                "status"]
            if "errors" in check_state:
                module.fail_json(msg=result)
            start_instance = bm_instance.create_server_action(
                server=instance,
                action="start")
            if "errors" in start_instance:
                module.fail_json(msg=start_instance)

        if "id" in check and state == "poweredoff":
            if force:
                action_type = "hard"
            else:
                action_type = "soft"
            check_state = bm_instance.get_server(instance)[
                "status"]
            if "errors" in check_state:
                module.fail_json(msg=result)
            stop_instance = bm_instance.create_server_action(
                server=instance,
                action=action_type)
            if "errors" in stop_instance:
                module.fail_json(msg=stop_instance)

        if "id" in check and state == "present":
            module.exit_json(changed=False, msg=check)

        if not id in check:
            result = bm_instance.create_server(
                name=instance,
                keys=keys,
                profile=profile,
                network_interfaces=network_interfaces,
                resource_group=resource_group,
                user_data=user_data,
                vpc=vpc,
                image=image,
                trusted_platform_module=trusted_platform_module,
                enable_secure_boot=enable_secure_boot,
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
