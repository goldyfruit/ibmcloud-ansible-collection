#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import security as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_security_group_rule
short_description: Manage VPC security group rules on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - This module creates a new security group rule from a security group rule
    prototype object. The prototype object is structured in the same way as
    a retrieved security group rule and contains the information necessary to
    create the rule.
  - As part of creating a new rule in a security group, the rule is applied
    to all the networking interfaces in the security group. Rules specify
    which IP traffic a security group should allow. Security group rules are
    stateful, such that reverse traffic in response to allowed traffic is
    automatically permitted.
  - A rule allowing inbound TCP traffic on port 80 also allows outbound TCP
    traffic on port 80 without the need for an additional rule.
requirements:
  - "ibmcloud-python-sdk"
options:
  group:
    description:
      - The user-defined name for this security group.
    type: str
    required: true
  rule:
    description:
      - Rule ID.
    type: str
    required: true
  direction:
    description:
      - The direction of traffic to enforce.
    type: str
    choices: [inbound, outbound]
  ip_version:
    description:
      - The IP version to enforce.
    type: str
    choices: [ipv4]
  protocol:
    description:
      - The protocol to enforce.
    type: str
    choices: [all, icmp, tcp, udp],
  port_min:
    description:
      - For a single port, set C(port_max) to the same value.
    type: int
  port_max:
    description:
      - For a single port, set C(port_min) to the same value.
    type: int
  code:
    description:
      - May only be specified if type is also specified. Only related if
        C(protocol=icmp) protocol.
    type: int
  type:
    description:
      - Only related with if C(protocol=icmp) protocol.
    type: int
  cidr_block:
    description:
      - The remote CIDR block.
    type: str
  address:
    description:
      - The remote IP address.
    type: str
  security_group:
    description:
      - The remote security group.
    type: str
  unique:
    description:
      - Avoid duplicate rules within the securiry group.
    type: bool
    default: true
    choices: [true, false]
  state:
    description:
      - Should the resource be present or absent.
    type: str
    default: present
    choices: [present, absent]
'''

EXAMPLES = r'''
- name: Create rule (HTTPS open for one address)
  ic_is_security_group_rule:
    group: ibmcloud-sec-group-rule-baby
    direction: inbound
    protocol: tcp
    port_min: 443
    port_max: 443
    remote:
      address: 10.243.12.23

- name: Create rule (allow ICMP for any)
  ic_is_security_group_rule:
    group: ibmcloud-sec-group-rule-baby
    direction: inbound
    protocol: icmp
    code: 0
    type: 8
    remote:
      cidr_block: 0.0.0.0/0

- name: Delete rule
  ic_is_security_group_rule:
    group: ibmcloud-sec-group-baby
    rule: r006-6cfe8f8e-1fca-4859-bd9a-ea6502e17a95
    state: absent
'''


security = sdk.Security()


def _check_rule(module):
    data = security.get_security_group_rules(module.params["group"])
    if "errors" in data:
        module.fail_json(msg=data)

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

    group = module.params["group"]
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

    if not rule:
        rule = None
    check = security.get_security_group_rule(group, rule)

    if state == "absent":
        if "id" in check:
            result = security.delete_security_group_rule(group, rule)
            if "errors" in result:
                module.fail_json(msg=result)

            payload = {"rule": rule, "security_group": group,
                       "status": "deleted"}
            module.exit_json(changed=True, msg=payload)

        payload = {"rule": rule, "security_group": group,
                   "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        if "id" in check:
            if unique:
                _check_rule(module)

            result = security.create_security_group_rule(
                sg=group,
                direction=direction,
                ip_version=ip_version,
                protocol=protocol,
                port_max=port_max,
                port_min=port_min,
                code=code,
                type=type,
                cidr_block=cidr_block,
                address=address,
                security_group=security_group
            )

            if "errors" in result:
                module.fail_json(msg=result)

            module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
