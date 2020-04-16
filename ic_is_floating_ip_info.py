#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.vpc import floating_ip as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_is_floating_ip_info
short_description: Retrieve VPC floating IPs on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - Floating IPs allow inbound and outbound traffic from the Internet
    to an instance.
notes:
  - The result contains a list of floating IPs.
requirements:
  - "ibmcloud-python-sdk"
options:
  fip:
    description:
      - Restrict results to floating IP with ID, name or address matching.
    type: str
'''

EXAMPLES = r'''
- name: Retrieve floating IP list
  ic_is_floating_ip_info:

- name: Retrieve specific floating
  ic_is_floating_ip_info:
    fip: 128.128.129.129
'''


def run_module():
    module_args = dict(
        fip=dict(
            type='str',
            required=False),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    floating_ip = sdk.Fip()

    fip = module.params['fip']

    if fip:
        result = floating_ip.get_floating_ip(fip)
        if "errors" in result:
            module.fail_json(msg=result["errors"])
    else:
        result = floating_ip.get_floating_ips()
        if "errors" in result:
            module.fail_json(msg=result["errors"])

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
