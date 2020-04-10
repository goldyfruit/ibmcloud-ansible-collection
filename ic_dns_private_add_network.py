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
module: ic_dns_private_add_network
short_description: Add or delete permitted network to a private dns zone.
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
        required: true
    vpc:
        description:
            -  Name or ID of VPC to delete or add as permitted network.
        required: true
    state:
        description:
            - Should the resource be present or absent.
        required: false
        choices: [present, absent]
        default: present
'''

EXAMPLES = '''
# Add my-vpc-oh-yeah VPC as allowed permitted network
- ic_dns_private_add_network:
    dns_zone: ibmcloud-dns-baby
    resource_instance: ibmcloud-rg-baby
    vpc: my-vpc-oh-yeah

# Create a private DNS
- ic_dns_private_add_network:
    dns_zone: ibmcloud-dns-baby
    resource_instance: ibmcloud-rg-baby

# Delete a private DNS
- ic_dns_private_add_network:
    dns_zone: ibmcloud-dns-baby
    resource_instance: ibmcloud-rg-baby
    state: absent
'''

dns = sdk.Dns()

#def _check_zone(module):
#    #module.exit_json(changed=False, msg="ceci est un message {}".format(module.params["dns_zone"]))
#    result = dns.get_dns_zone(dns_zone=module.params["dns_zone"],
#            resource_instance=module.params["resource_instance"])
#
#    msg = ("zone {} already exists in resource instance {}".format(
#        module.params["dns_zone"],
#        module.params["resource_instance"]))
#
#    if "errors" in result:
#        for key in result["errors"]:
#                if key["code"] != "not_found":
#                    module.fail_json(msg=result["errors"])
#    else:
#        module.exit_json(changed=False, msg=msg)

def run_module():
    module_args = dict(
        dns_zone=dict(
            type='str',
            required=True),
        resource_instance=dict(
            type='str',
            required=True),
        vpc=dict(
            type='str',
            default='auto',
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
    vpc = module.params['vpc']
    state = module.params['state']

    if state == "absent":
        result = dns.delete_permitted_network(dns_zone=dns_zone,
                resource_instance=resource_instance,
                vpc=vpc)

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "not_found":
                    module.fail_json(msg=result["errors"])
                else:
                    module.exit_json(changed=False, msg=(
                        "The vpc {} is not attached with zone {} ").format(vpc, dns_zone))

        module.exit_json(changed=True, msg=(
            "The vpc {} is successfully detached from zone {}").format(vpc, dns_zone))

    else:
        
        result = dns.add_permitted_network(dns_zone=dns_zone,
                                resource_instance=resource_instance,
                                vpc=vpc)

        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "resource_already_exists":
                    module.fail_json(msg=result["errors"])
                else:
                    module.exit_json(changed=False, msg=("The VPC {} is already attached to the zone {}").format(vpc, dns_zone))
        else:
            module.exit_json(changed=True, msg=(result))


def main():
    run_module()


if __name__ == '__main__':
    main()
