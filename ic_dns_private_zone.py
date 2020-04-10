#!/usr/bin/env python

# GNU General Public License v3.0+

from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.dns import private as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_dns_private_zone
short_description: Create or delete private DNS instance.
author: James Regis (@jregis)
version_added: "2.9"
description:
    - Create or delete private DNS instamce on IBM Cloud.
requirements:
    - "ibmcloud-python-sdk"
options:
    dns_zone:
        description:
            -  Name that has to be given to the DNS to create or delete.
                During the removal an UUID could be used.
        required: true
    resource_instance:
        description:
            -  Name or UUID of the resource group where the VPC has to
               be created.
        required: false
    description:
        description:
            -  A short description of the DNS.
        required: false
    label:
        description:
            -  A label for the DNS.
        required: false
    state:
        description:
            - Should the resource be present or absent.
        required: false
        choices: [present, absent]
        default: present
'''

EXAMPLES = '''
# Create private VPC with resource group, description and label
- ic_dns_private_zone:
    dns_zone: ibmcloud-dns-baby
    resource_instance: ibmcloud-rg-baby
    description: Hail to the king baby
    label: dev

# Create a private DNS
- ic_dns_private_zone:
    dns_zone: ibmcloud-dns-baby
    resource_instance: ibmcloud-rg-baby

# Delete a private DNS
- ic_dns_private_zone:
    dns_zone: ibmcloud-dns-baby
    resource_instance: ibmcloud-rg-baby
    state: absent
'''

dns = sdk.Dns()

def _check_zone(module):
    result = dns.get_dns_zone(dns_zone=module.params["dns_zone"],
            resource_instance=module.params["resource_instance"])

    msg = ("The zone {} already exists in resource instance {}".format(
        module.params["dns_zone"],
        module.params["resource_instance"]))

    if "errors" in result:
        for key in result["errors"]:
                if key["code"] != "not_found":
                    module.fail_json(msg=result["errors"])
    else:
        module.exit_json(changed=False, msg=msg)

def run_module():
    module_args = dict(
        dns_zone=dict(
            type='str',
            required=True),
        resource_instance=dict(
            type='str',
            required=True),
        description=dict(
            type='str',
            default='false',
            required=False),
        label=dict(
            type='str',
            default='auto',
            required=False),
        unique=dict(
            type='bool',
            default=True,
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


    
    dns_zone = module.params['dns_zone']
    resource_instance = module.params["resource_instance"]
    description = module.params['description']
    label = module.params['label']
    state = module.params['state']
    unique = module.params['unique']

    if state == "absent":
        result = dns.delete_zone(dns_zone=dns_zone,
                resource_instance=resource_instance)

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "not_found":
                    module.fail_json(msg=result["errors"])
                else:
                    module.exit_json(changed=False, msg=(
                        "zone {} doesn't exist")).format(dns_zone)

        module.exit_json(changed=True, msg=(
            "zone {} successfully deleted").format(dns_zone))

    else:
        if unique: 
            _check_zone(module)
    
        result = dns.create_zone(dns_zone=dns_zone,
                                resource_instance=resource_instance,
                                description=description,
                                label=label)

        if "errors" in result:
            module.fail_json(msg=esult["errors"])
        else:
            module.exit_json(changed=True, msg=(result))


def main():
    run_module()


if __name__ == '__main__':
    main()
