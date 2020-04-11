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
module: ic_dns_private_record
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
            -  Name or UUID of the resource instance that hosts thw DNS.
        required: false
    record:
        description:
            -  JSON structure representing the record to add in the DNS.
            {
              "name": "testA",
              "type": "A",
              "rdata": {
                  "ip": "1.2.3.4"
              }
            }
        required: true
    record_name:
        description:
            -  Record name to delete (fqdn). 
        required: true
    record_id:
        description:
            -  Record id to delete.
        required: true
    state:
        description:
            - Should the resource be present or absent.
        required: false
        choices: [present, absent]
        default: present
'''

EXAMPLES = '''
# Create an A DNS record 
- ic_dns_private_record:
    dns_zone: ibmcloud-dns-baby
    resource_instance: ibmcloud-rg-baby
    description: Hail to the king baby
    label: dev

# Create a private DNS
- ic_dns_private_record:
    dns_zone: ibmcloud-dns-baby
    resource_instance: ibmcloud-rg-baby

# Delete a private DNS
- ic_dns_private_record:
    dns_zone: ibmcloud-dns-baby
    resource_instance: ibmcloud-rg-baby
    state: absent
'''

def run_module():
    module_args = dict(
        dns_zone=dict(
            type='str',
            required=True),
        resource_instance=dict(
            type='str',
            required=True),
        record=dict(
            type='dict',
            required=False),
        record_name=dict(
            type='str',
            required=False),
        record_id=dict(
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


    dns = sdk.Dns()
    
    dns_zone = module.params['dns_zone']
    resource_instance = module.params["resource_instance"]
    record = module.params['record']
    record_name = module.params['record_name']
    record_id = module.params['record_id']
    state = module.params['state']

    if state == "absent":
#        module.exit_json(changed=True, msg=(record))
        if record_name:
            result = dns.delete_resource_record(dns_zone=dns_zone,
                    resource_instance=resource_instance,
                    record=record_name)
    
            if "errors" in result:
                for key in result["errors"]:
                    if key["code"] != "not_found":
                        module.fail_json(msg=result["errors"])
                    else:
                        module.exit_json(changed=False, msg=(
                            "record {} doesn't exist").format(record_name))
    
        module.exit_json(changed=True, msg=(
            "record {} successfully deleted").format(record_name))

    else:
        if record == None:
            module.fail_json(msg="You must provide records data")

        record["rdata"] = record["rdata"][0]
        result = dns.create_resource_record(dns_zone=dns_zone,
                                resource_instance=resource_instance,
                                record=record)
        if "errors" in result:
            for key in result["errors"]:
                if key["code"] != "resource_already_exists":
                    module.fail_json(msg=result["errors"])
                else:
                    module.exit_json(changed=False, msg=(
                        "The record already exists."))
        module.exit_json(changed=True, msg=(result))


def main():
    run_module()


if __name__ == '__main__':
    main()
