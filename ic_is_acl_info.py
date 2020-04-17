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
module: ic_is_acl_info
short_description: Retrieve VPC network ACL on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - A network ACL defines a set of packet filtering (5-tuple) rules for all
    traffic in and out of a subnet. Both allow and deny rules can be defined,
    and rules are stateless such that reverse traffic in response to allowed
    traffic is not automatically permitted.
notes:
  - The result contains a list of network ACLs.
requirements:
  - "ibmcloud-python-sdk"
options:
  acl:
    description:
      - Restrict results to network ACL with ID or name matching.
    type: str
'''

EXAMPLES = r'''
- name: Retrieve network ACL list
  ic_is_acl_info:

- name: Retrieve specific network ACL
  ic_is_acl_info:
    acl: ibmcloud-acl-baby
'''


def run_module():
    module_args = dict(
        acl=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    network_acl = sdk.Acl()

    acl = module.params['acl']

    if acl:
        result = network_acl.get_network_acl(acl)
        if "errors" in result:
            module.fail_json(msg=result)
    else:
        result = network_acl.get_network_acls()
        if "errors" in result:
            module.fail_json(msg=result)

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
