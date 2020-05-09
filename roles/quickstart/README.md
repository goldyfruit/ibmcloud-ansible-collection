Quickstart
=========

This role is a quickstart to consume resources on IBM Cloud. During the role execution the following resources will be created:

  - VPC (Virtual Private Cloud)
  - VPC address prefix
  - Public gateway
  - Subnet
  - Public gateway attached to the subnet
  - Security group
  - Rules in security group (ICMP and port 22)
  - SSH public key
  - Floating IP
  - VSI (Virtual Server Instance)
  - Security group attached to the VSI
  - Floating IP attached to the VSI

Requirements
------------

  - ibmcloud-python-sdk

Role Variables
--------------

The Virtual Private Cloud (VPC) name.

    vpc_name

The VPC address prefix name.

    vpc_address_prefix_name

Security group name.

    security_group_name

Public gateway name.

    gateway_name

SSH public key name.

    key_name

Virtual Server Instance (VSI) name.

    vsi_name

Floating IP name.

    floating_ip_name

Virtual subnet name.

    subnet_name

Virtual subnet CIDR (used by VPC address prefix).

    subnet_cidr

Ports to open in security group.

    ports_to_open

SSH public key.

    ssh_public_key

Zone where resources will be created.

    zone_name: us-south-3

Resource group where the resource should be created, `omit` if not defined.

    resource_group_name

VSI profile name to use to create the instance.

    vsi_profile_name

VSI image to use to provision the instance.

    vsi_image_name

Dependencies
------------

None

Example Playbook
----------------

    ---
    - hosts: localhost
      connection: local
      gather_facts: no
      collections:
        - ibmcloud.cloud_automation

      tasks:
        - import_role:
            name: quickstart

License
-------

MPL-2.0

Author Information
------------------

Gaëtan Trellu (@goldyfruit)