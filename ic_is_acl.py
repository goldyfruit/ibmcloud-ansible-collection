#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import acl as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_acl
short_description: Manage VPC network ACL on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - A network ACL defines a set of packet filtering (5-tuple) rules for all
    traffic in and out of a subnet. Both allow and deny rules can be defined,
    and rules are stateless such that reverse traffic in response to allowed
    traffic is not automatically permitted.
options:
  acl:
    description:
      - The user-defined name for this network ACL. Names must be unique
        within the VPC the Network ACL resides in.
    required: true
    type: str
  resource_group:
    description:
      - The resource group to use. If unspecified, the account's default
        resource group is used.
    type: str
  rules:
    description:
      - Array of prototype objects for rules to create along with this
        network ACL. If unspecified, no rules will be created, resulting
        in all traffic being denied.
    type: list
    suboptions:
      action:
        description:
          - Whether to allow or deny matching traffic.
        type: str
        required: true
        choices: [allow, deny]
      destination:
        description:
          - The destination IP address or CIDR block. The CIDR block 0.0.0.0/0
            applies to all addresses.
        type: str
      direction:
        description:
          - Whether the traffic to be matched is inbound or outbound.
        type: str
        required: true
        choices: [inbound, outbound]
      name:
        description:
          - The user-defined name for this rule. Names must be unique within
            the network ACL the rule resides in.
        type: str
      protocol:
        description:
          - The protocol to enforce.
        type: str
        choices: [all, icmp, tcp, udp]
      source:
        description:
          - The source IP address or CIDR block. The CIDR block 0.0.0.0/0
            applies to all addresses.
        type: str
        required: true
      destination_port_max:
        description:
          - The inclusive upper bound of TCP/UDP destination port range.
          - Required if C(protocol=udp) or C(protocol=tcp).
        type: int
      destination_port_min:
        description:
          - The inclusive lower bound of TCP/UDP destination port range.
          - Required if C(protocol=udp) or C(protocol=tcp).
        type: int
      source_port_max:
        description:
          - The inclusive upper bound of TCP/UDP source port range.
          - Required if C(protocol=udp) or C(protocol=tcp).
        type: int
      source_port_min:
        description:
          - The inclusive lower bound of TCP/UDP source port range.
          - Required if C(protocol=udp) or C(protocol=tcp).
        type: int
      code:
        description:
          - The ICMP traffic code to allow. If unspecified, all codes are
            allowed. This can only be specified if type is also specified.
          - Required if C(protocol=icmp).
        type: int
      type:
        description:
          - The ICMP traffic type to allow. If unspecified, all types are
            allowed by this rule.
        type: int
  source_network_acl:
    description:
      - Network ACL to copy rules from.
    type: str
  vpc:
    description:
      - The VPC this network ACL is to be a part of.
    type: str
    required: true
  state:
    description:
      - Should the resource be present or absent.
    default: present
    choices: [present, absent]
'''

EXAMPLES = r'''
- name: Create network ACL without any rules (deny traffic)
  ic_is_acl:
    acl: ibmcloud-acl-baby
    vpc: ibmcloud-vpc-baby

- name: Create network ACL with rules (allow traffic)
  ic_is_acl:
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

- name: Delete network ACL
  ic_is_acl:
    acl: ibmcloud-acl-baby
    vpc: ibmcloud-vpc-baby
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
            required=True),
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

    network_acl = sdk.Acl()

    acl = module.params["acl"]
    resource_group = module.params["resource_group"]
    rules = module.params["rules"]
    source_network_acl = module.params["source_network_acl"]
    vpc = module.params["vpc"]
    state = module.params["state"]

    check = network_acl.get_network_acl(acl)

    if state == "absent":
        if "id" in check:
            result = network_acl.delete_network_acl(acl)
            if "errors" in result:
                module.fail_json(msg=result["errors"])

            payload = {"network_acl": acl, "status": "deleted"}
            module.exit_json(changed=True, msg=payload)

        payload = {"network_acl": acl, "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        if "id" in check:
            module.exit_json(changed=False, msg=check)

        result = network_acl.create_network_acl(
            name=acl,
            resource_group=resource_group,
            rules=rules,
            source_network_acl=source_network_acl,
            vpc=vpc
        )

        if "errors" in result:
            module.fail_json(msg=result["errors"])

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
