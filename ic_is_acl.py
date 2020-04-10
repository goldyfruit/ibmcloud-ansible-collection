#!/usr/bin/env python

# GNU General Public License v3.0+

from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import acl as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_is_acl
short_description: Create or delete network ACL.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Create or delete network ACL on IBM Cloud.
requirements:
    - "ibmcloud-python-sdk"
options:
    acl:
        description:
            -  Name that has to be given to the network ACL to create
                or delete.
                During the removal an UUID could be used.
        required: true
    resource_group:
        description:
            -  Name or UUID of the resource group where the network ACL has
                 to be created.
        required: false
    rules:
        description:
            -  Array of prototype objects for rules to create along with this
                network ACL.
        required: false
    source_network_acl:
        description:
            -  Network ACL to copy rules from.
        required: false
    vpc:
        description:
            -  The VPC the network ACL is to be a part of.
        required: false
    state:
        description:
            - Should the resource be present or absent.
        required: false
        choices: [present, absent]
        default: present
'''

EXAMPLES = '''
# Create network ACL without rules (block traffic)
- ic_is_acl:
    acl: ibmcloud-acl-baby
    vpc: ibmcloud-vpc-baby

# Create network ACL with rules (allow traffic)
- ic_is_acl:
    acl: ibmcloud-acl-baby
    vpc: ibmcloud-vpc-baby
    rules:
      - name: inbound
        action: allow
        destination: 0.0.0.0/0
        source: 0.0.0.0/0
        protocol: all
        direction: inbound
      - name: outbound
        action: allow
        destination: 0.0.0.0/0
        source: 0.0.0.0/0
        protocol: all
        direction: outbound

# Delete network ACL
- ic_is_acl:
    acl: ibmcloud-acl-baby
    state: absent
'''


def run_module():
    module_args = dict(
        acl=dict(
            type='str',
            required=True),
        resource_group=dict(
            type='str',
            required=False),
        rules=dict(
            type='list',
            options=dict(
                action=dict(
                    type='str',
                    required=True,
                    choices=['allow', 'deny']),
                destination=dict(
                    type='str',
                    required=True),
                direction=dict(
                    type='str',
                    required=True,
                    choices=['inbound', 'outbound']),
                name=dict(
                    type='str',
                    required=False),
                destination_port_min=dict(
                    type='int',
                    required=False),
                destination_port_max=dict(
                    type='int',
                    required=False),
                source_port_min=dict(
                    type='int',
                    required=False),
                source_port_max=dict(
                    type='int',
                    required=False),
                protocol=dict(
                    type='str',
                    required=True,
                    choices=['all', 'icmp', 'tcp', 'udp']),
                source=dict(
                    type='str',
                    required=True),
            ),
            required=False),
        vpc=dict(
            type='str',
            required=False),
        source_network_acl=dict(
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

    acl = sdk.Acl()

    name = module.params["acl"]
    resource_group = module.params["resource_group"]
    rules = module.params["rules"]
    source_network_acl = module.params["source_network_acl"]
    vpc = module.params["vpc"]
    state = module.params["state"]

    if state == "absent":
        result = acl.delete_network_acl(name)

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "not_found":
                    module.fail_json(msg=result["errors"])
                else:
                    module.exit_json(changed=False, msg=(
                        "network ACL {} doesn't exist")).format(name)

        module.exit_json(changed=True, msg=(
            "network ACL {} successfully deleted")).format(name)

    else:

        result = acl.create_network_acl(
            name=name,
            resource_group=resource_group,
            rules=rules,
            source_network_acl=source_network_acl,
            vpc=vpc)

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "validation_unique_failed":
                    module.fail_json(msg=result["errors"])
                else:
                    exist = acl.get_network_acl(name)
                    if "errors" in exist:
                        module.fail_json(msg=exist["errors"])
                    else:
                        module.exit_json(changed=False, msg=(exist))

        module.exit_json(changed=True, msg=(result))


def main():
    run_module()


if __name__ == '__main__':
    main()
