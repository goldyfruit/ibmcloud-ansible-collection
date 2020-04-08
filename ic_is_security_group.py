#!/usr/bin/env python

# GNU General Public License v3.0+

from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import security as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_is_security_group
short_description: Create or delete security group.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Create or delete security group on IBM Cloud.
requirements:
    - "ibmcloud-python-sdk"
options:
    group:
        description:
            -  The user-defined name for this security group.
        required: true
    resource_group:
        description:
            -  Name or UUID of the resource group where the security group has
               to be created.
        required: false
    rules:
        description:
            -  Array of rule prototype objects for rules to be created for this
               security group.
        required: false
    vpc:
        description:
            -  The VPC the security group is to be a part of.
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
# Create security group without rules (block traffic)
- ic_is_security_group:
    group: ibmcloud-sec-group-baby
    vpc: ibmcloud-vpc-baby

# Create security group with rule (SSH open)
- ic_is_security_group:
    group: ibmcloud-sec-group-baby
    vpc: ibmcloud-vpc-baby
    rules:
      - name: ssh
        direction: inbound
        protocol: tcp
        port_min: 22
        port_max: 22
        remote:
          cidr_block: 0.0.0.0/0

# Delete security group
- ic_is_security_group:
    group: ibmcloud-sec-group-baby
    state: absent
'''


def run_module():
    module_args = dict(
        group=dict(
            type='str',
            required=True),
        resource_group=dict(
            type='str',
            required=False),
        rules=dict(
            type='list',
            options=dict(
                direction=dict(
                    type='str',
                    required=True,
                    choices=['inbound', 'outbound']),
                ip_version=dict(
                    type='str',
                    required=False,
                    choices=['ipv4']),
                protocol=dict(
                    type='str',
                    required=True,
                    choices=['all', 'icmp', 'tcp', 'udp']),
                port_max=dict(
                    type='int',
                    required=False),
                port_min=dict(
                    type='int',
                    required=False),
                code=dict(
                    type='int',
                    required=False),
                type=dict(
                    type='int',
                    required=False),
                remote=dict(
                    type='dict',
                    options=dict(
                        cidr_block=dict(
                            type='str',
                            required=False),
                        ip=dict(
                            type='str',
                            required=False),
                        id=dict(
                            type='str',
                            required=False),
                    ),
                    required=False),
            ),
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

    security = sdk.Security()

    name = module.params["group"]
    resource_group = module.params["resource_group"]
    rules = module.params["rules"]
    vpc = module.params["vpc"]
    state = module.params["state"]

    if state == "absent":
        result = security.delete_security_group(name)

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "not_found":
                    module.fail_json(msg=result["errors"])
                else:
                    module.exit_json(changed=False, msg=(
                        "security group {} doesn't exist".format(name)))

        module.exit_json(changed=True, msg=(
            "security group {} successfully deleted".format(name)))
    else:
        result = security.create_security_group(
            name=name,
            resource_group=resource_group,
            rules=rules,
            vpc=vpc)

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "validation_unique_failed":
                    module.fail_json(msg=result["errors"])
                else:
                    exist = security.get_security_group(name)
                    if "errors" in exist:
                        module.fail_json(msg=exist["errors"])
                    else:
                        module.exit_json(changed=False, msg=(exist))

        module.exit_json(changed=True, msg=(result))


def main():
    run_module()


if __name__ == '__main__':
    main()
