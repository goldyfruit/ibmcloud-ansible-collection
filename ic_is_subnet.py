#!/usr/bin/env python

# GNU General Public License v3.0+

from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import subnet as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_is_subnet
short_description: Create or delete network subnet.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Create or delete network subnet on IBM Cloud.
requirements:
    - "ibmcloud-python-sdk"
options:
    subnet:
        description:
            -  Name that has to be given to the subnet to create or delete.
                During the removal an UUID could be used.
        required: true
    resource_group:
        description:
            -  Name or UUID of the resource group where the subnet has to
               be created.
        required: false
    ip_version:
        description:
            -  The IP version(s) supported by this subnet.
        required: false
        choices: [both, ipv4, ipv6]
    ipv4_cidr_block:
        description:
            -  The IPv4 range of the subnet, expressed in CIDR format.
        required: false
    network_acl:
        description:
            -  The network ACL to use for this subnet.
        required: false
    public_gateway:
        description:
            -  The public gateway to handle internet bound traffic for this
                subnet.
        required: false
    total_ipv4_address_count:
        description:
            -  The total number of IPv4 addresses required.
        required: false
    zone:
        description:
            -  The location of the subnet.
        required: false
    vpc:
        description:
            -  The VPC the subnet is to be a part of.
        required: false
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
# Create subnet
- ic_is_subnet:
    subnet: ibmcloud-subnet-baby
    vpc: ibmcloud-vpc-baby
    ipv4_cidr_block: 192.168.10.0/24

# Delete subnet
- ic_is_subnet:
    subnet: ibmcloud-volume-baby
    state: absent
'''


def run_module():
    module_args = dict(
        subnet=dict(
            type='str',
            required=True),
        resource_group=dict(
            type='str',
            required=False),
        ip_version=dict(
            type='str',
            choices=['both', 'ipv4', 'ipv6'],
            required=False),
        ipv4_cidr_block=dict(
            type='str',
            required=False),
        network_acl=dict(
            type='str',
            required=False),
        public_gateway=dict(
            type='str',
            required=False),
        total_ipv4_address_count=dict(
            type='int',
            required=False),
        zone=dict(
            type='str',
            required=False),
        vpc=dict(
            type='str',
            required=False),
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

    subnet = sdk.Subnet()

    name = module.params["subnet"]
    resource_group = module.params["resource_group"]
    ip_version = module.params["ip_version"]
    ipv4_cidr_block = module.params["ipv4_cidr_block"]
    network_acl = module.params["network_acl"]
    public_gateway = module.params["public_gateway"]
    total_ipv4_address_count = module.params["total_ipv4_address_count"]
    zone = module.params["zone"]
    vpc = module.params["vpc"]
    state = module.params["state"]

    if state == "absent":
        result = subnet.delete_subnet(name)

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "not_found":
                    module.fail_json(msg=result["errors"])
                else:
                    module.exit_json(changed=False, msg=(
                        "subnet {} doesn't exist")).format(name)

        module.exit_json(changed=True, msg=(
            "subnet {} successfully deleted")).format(name)

    else:

        if total_ipv4_address_count and not zone:
            module.fail_json(msg="when using total_ipv4_address_count option,"
                                 " zone option should be set too.")

        result = subnet.create_subnet(
            name=name,
            resource_group=resource_group,
            ip_version=ip_version,
            ipv4_cidr_block=ipv4_cidr_block,
            network_acl=network_acl,
            public_gateway=public_gateway,
            total_ipv4_address_count=total_ipv4_address_count,
            zone=zone,
            vpc=vpc)

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "validation_unique_failed":
                    module.fail_json(msg=result["errors"])
                else:
                    exist = subnet.get_subnet(name)
                    if "errors" in exist:
                        module.fail_json(msg=exist["errors"])
                    else:
                        module.exit_json(changed=False, msg=(exist))

        module.exit_json(changed=True, msg=(result))


def main():
    run_module()


if __name__ == '__main__':
    main()
