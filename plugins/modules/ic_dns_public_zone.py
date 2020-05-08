#!/usr/bin/env python

# GNU General Public License v3.0+

from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.dns import public as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_dns_public_zone
short_description: Create or delete private DNS instance.
author: James Regis (@jregis)
version_added: "2.9"
description:
    - Create or delete private DNS instamce on IBM Cloud.
requirements:
    - "ibmcloud-python-sdk"
options:
    zone:
        description:
            -  Name that has to be given to the DNS to create or delete.
                During the removal an UUID could be used.
        required: true
    check_availability:
        description:
            - Check if the domain is available or not
        required: false
        choices: [true, false]
        default: false
    state:
        description:
            - Should the resource be present or absent.
        required: false
        choices: [present, absent]
        default: present
'''

EXAMPLES = '''
# Check if the domain if available
- ic_dns_public_zone:
  check_availability: true
  zone: ibm.com

# Create private VPC with resource group, description and label
- ic_dns_public_zone:
    zone: ibmcloud.lab

# Create a private DNS
- ic_dns_public_zone:
    zone: ibmcloud.lab

# Delete a private DNS
- ic_dns_public_zone:
    zone: ibmcloud.lab
    state: absent
'''

def run_module():
    module_args = dict(
        zone=dict(
            type='str',
            required=True),
        check_availability=dict(
            type='str',
            default='false',
            choices=['true', 'false'],
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

    dns = sdk.Dns()
    
    zone = module.params['zone']
    check_availability = module.params["check_availability"]
    state = module.params['state']

    if state == "absent":
        zone_id = dns.get_zone_id(zone)
        if not isinstance(zone_id, int):
            if "errors" in zone_id:
                for key in zone_id["errors"]:
                    if key["code"] == "not_found":
                        module.exit_json(changed=False, msg=(
                            "zone {} doesn't exist").format(zone))
        result = dns.delete_zone(zone)
        if result is None:
            module.exit_json(changed=True, msg=(
                "zone {} successfully deleted").format(zone))

    else:
        zone_id = dns.get_zone_id(zone)
        if not isinstance(zone_id, int):
            if "errors" in zone_id:
                for key in zone_id["errors"]:
                    if key["code"] == "not_found":
                        result = dns.create_zone(zone)
                        if result:
                            module.exit_json(changed=True, msg=(
                                "zone {} successfully created".format(zone)))
                        module.fail_json(changed=False, msg=(
                            "errot while creating zone {}")).format(zone)
        module.exit_json(changed=False, msg=("zone {} already exists".format(zone)))


def main():
    run_module()


if __name__ == '__main__':
    main()
