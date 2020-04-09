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
module: ic_is_security_group_rule
short_description: Create or delete security group rule.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
    - Create or delete a rule within a security group on IBM Cloud.
requirements:
    - "ibmcloud-python-sdk"
options:
    group:
        description:
            -  The user-defined name for this security group.
        required: true
    rule:
        description:
            -  The rule ID (used for deletion).
        required: true
    direction:
        description:
            -  The direction of traffic to enforce.
        required: false
        choices: [inbound, outbound]
    ip_version:
        description:
            -  The IP version to enforce.
        required: false
        choices: [ipv4]
    protocol:
        description:
            -  The protocol to enforce.
        required: false
        choices: [all, icmp, tcp, udp],
    port_min:
        description:
            -  For a single port, set port_max to the same value.
        required: false
    port_max:
        description:
            -  For a single port, set port_min to the same value.
        required: false
    code:
        description:
            -  May only be specified if type is also specified. Only
               related with icmp protocol.
        required: false
    type:
        description:
            -  Only related with icmp protocol.
        required: false
    cidr_block:
        description:
            -  The remote CIDR block.
        required: false
    address:
        description:
            -  The remote IP address.
        required: false
    security_group:
        description:
            -  The remote security group.
        required: false
    unique:
        description:
            -  Avoid duplicate rules within the securiry group.
        required: false
        choices: [true, false]
        default: true
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
# Create security group with rule (HTTPS open for one address)
- ic_is_security_group_rule:
    group: ibmcloud-sec-group-baby
    vpc: ibmcloud-vpc-baby
    rules:
      - direction: inbound
        protocol: tcp
        port_min: 443
        port_max: 443
        remote:
          address: 10.243.12.23

# Create security group with rule (allow ICMP for any)
- ic_is_security_group_rule:
    group: ibmcloud-sec-group-baby
    vpc: ibmcloud-vpc-baby
    rules:
      - direction: inbound
        protocol: icmp
        code: 0
        type: 8
        remote:
          cidr_block: 0.0.0.0/0

# Delete security group rule
- ic_is_security_group_rule:
    group: ibmcloud-sec-group-baby
    rule: r006-6cfe8f8e-1fca-4859-bd9a-ea6502e17a95
    state: absent
'''

security = sdk.Security()


def _check_rule(module):
    data = security.get_security_group_rules(module.params["group"])
    if "errors" in data:
        module.fail_json(msg=data["errors"])

    msg = ("rule already exists in security group {}".format(
        module.params["group"]))

    # "Workaround" for 80 chars Pylint
    cird_block = module.params["cidr_block"]

    for i in data["rules"]:
        if (
            i["direction"] == module.params["direction"]
            and i.get("port_max", "") == module.params["port_max"]
            and i.get("port_min", "") == module.params["port_min"]
            and i.get("protocol", "") == module.params["protocol"]
        ):
            if (
                i["remote"].get("cidr_block", "") == cird_block
                or i["remote"].get("address", "") == module.params["address"]
                or i["remote"].get("id", "") == module.params["security_group"]
            ):
                module.exit_json(changed=False, msg=msg)
        elif (
            i["direction"] == module.params["direction"]
            and i.get("type", "") == module.params["type"]
            and i.get("protocol", "") == module.params["protocol"]
            and i.get("code", "") == module.params["code"]
        ):
            if (
                i["remote"].get("cidr_block", "") == cird_block
                or i["remote"].get("address", "") == module.params["address"]
                or i["remote"].get("id", "") == module.params["security_group"]
            ):
                module.exit_json(changed=False, msg=msg)


def run_module():
    module_args = dict(
        group=dict(
            type='str',
            required=True),
        rule=dict(
            type='str',
            required=False),
        direction=dict(
            type='str',
            required=False,
            choices=['inbound', 'outbound']),
        ip_version=dict(
            type='str',
            required=False,
            choices=['ipv4']),
        protocol=dict(
            type='str',
            required=False,
            choices=['all', 'icmp', 'tcp', 'udp']),
        port_min=dict(
            type='int',
            required=False),
        port_max=dict(
            type='int',
            required=False),
        code=dict(
            type='int',
            required=False),
        type=dict(
            type='int',
            required=False),
        cidr_block=dict(
            type='str',
            required=False),
        address=dict(
            type='str',
            required=False),
        security_group=dict(
            type='str',
            required=False),
        unique=dict(
            type='bool',
            default='true',
            choices=[True, False],
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

    name = module.params["group"]
    rule = module.params["rule"]
    direction = module.params["direction"]
    ip_version = module.params["ip_version"]
    protocol = module.params["protocol"]
    port_max = module.params["port_max"]
    port_min = module.params["port_min"]
    code = module.params["code"]
    type = module.params["type"]
    cidr_block = module.params["cidr_block"]
    address = module.params["address"]
    security_group = module.params["security_group"]
    unique = module.params["unique"]
    state = module.params["state"]

    if state == "absent":
        result = security.delete_security_group_rule(name, rule)

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "not_found":
                    module.fail_json(msg=result["errors"])
                else:
                    module.exit_json(changed=False, msg=(
                        "rule {} in security group {} doesn't exist".format(
                            rule, name)))

        module.exit_json(changed=True, msg=(
            "rule {} successfully deleted security group {}".format(
                rule, name)))
    else:

        if unique:
            _check_rule(module)

        result = security.create_security_group_rule(
            sg=name,
            direction=direction,
            ip_version=ip_version,
            protocol=protocol,
            port_max=port_max,
            port_min=port_min,
            code=code,
            type=type,
            cidr_block=cidr_block,
            address=address,
            security_group=security_group,)

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "validation_unique_failed":
                    module.fail_json(msg=result["errors"])
                else:
                    exist = security.get_security_group_rule(name, rule)
                    if "errors" in exist:
                        module.fail_json(msg=exist["errors"])
                    else:
                        module.exit_json(changed=False, msg=(exist))

        module.exit_json(changed=True, msg=(result))


def main():
    run_module()


if __name__ == '__main__':
    main()
