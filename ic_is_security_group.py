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
module: ic_is_security_group
short_description: Manage VPC security group on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - Create or delete security group on IBM Cloud.
requirements:
  - "ibmcloud-python-sdk"
options:
  group:
    description:
      - The user-defined name for this security group.
    type: str
    required: true
  resource_group:
    description:
      - The resource group to use. If unspecified, the account's default
        resource group is used.
    type: str
  rules:
    description:
      - Array of rule prototype objects for rules to be created for this
        security group. If unspecified, no rules will be created, resulting
        in all traffic being denied.
    type: list
    suboptions:
      direction:
        description:
          - The direction of traffic to enforce.
        type: str
        required: true
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
        choices: [all, icmp, tcp, udp]
      port_min:
        description:
          - For a single port, set C(port_max) to the same value.
          - Required if C(protocol=udp) or C(protocol=tcp).
        type: int
      port_max:
        description:
          - For a single port, set C(port_min) to the same value.
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
          - Required if C(protocol=icmp).
        type: int
      remote:
        description:
          - The IP addresses or security groups from which this rule will allow
            traffic (or to which, for outbound rules). Can be specified as an
            IP address, a CIDR block, or a security group.
          - If omitted, a CIDR block of 0.0.0.0/0 will be used to allow traffic
            from any source (or to any source, for outbound rules).
        type: dict
        required: false
        suboptions:
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
              - The remote security group ID.
            type: str
  vpc:
    description:
      -  The VPC the security group is to be a part of.
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
- name: Create security group without rules (block traffic)
  ic_is_security_group:
    group: ibmcloud-sec-group-baby
    vpc: ibmcloud-vpc-baby

- name: Create security group with rule (SSH open)
  ic_is_security_group:
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

- name: Delete security group
  ic_is_security_group:
    group: ibmcloud-sec-group-baby
    vpc: ibmcloud-vpc-baby
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
                        address=dict(
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

    security = sdk.Security()

    group = module.params["group"]
    resource_group = module.params["resource_group"]
    rules = module.params["rules"]
    vpc = module.params["vpc"]
    state = module.params["state"]

    check = security.get_security_group(group)

    if state == "absent":
        if "id" in check:
            result = security.delete_security_group(group)
            if "errors" in result:
                module.fail_json(msg=result)

            payload = {"security_group": group, "status": "deleted"}
            module.exit_json(changed=True, msg=payload)

        payload = {"security_group": group, "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        if "id" in check:
            result = security.create_security_group(
                name=group,
                resource_group=resource_group,
                rules=rules,
                vpc=vpc
            )

        if "errors" in result:
            module.fail_json(msg=result)

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
