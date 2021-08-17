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
module: ic_dns_public_record
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
    record: The full DNS record to create or delete
        description:
        required: true
    type: A, CNAME, MX, AAAA, TXT, PTR, SRV, SPF, CAA, NS, SOA
    ttl: 60 (one hour)
    value: The new value when creating a DNS recor
    state:
        description:
            - Should the resource be present or absent.
        required: false
        choices: [present, absent]
        default: present
'''

EXAMPLES = '''
# Create an A public DNS record
- ic_dns_public_record:
    zone: comegetsome.duke
    record: www.comegetsome.duke
    type: A
    ttl: 60
    value: 10.0.0.1

# Delete a public DNS
- ic_dns_public_record:
    zone: comegetsome.duke
    record: www.comegetsome.duke
    state: absent
'''

def run_module():
    module_args = dict(
        zone=dict(
            type='str',
            required=True),
        record=dict(
            type='str',
            required=True),
        type=dict(
            type='str',
            choices=["A", "CNAME", "MX", "AAAA", "TXT", "PTR", "SRV",
                     "SPF", "CAA", "NS", "SOA"],
            required=False),
        ttl=dict(
            type='int',
            required=False),
        value=dict(
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

    ttl_min = 60
    ttl_max = 604800

    zone = module.params['zone']
    record = module.params['record']
    rtype = module.params['type']
    ttl = module.params['ttl']
    value = module.params['value']
    state = module.params['state']

    if state == "absent":
        search_result = dns.get_record(record=record, zone=zone)
        if "errors" in search_result:
            for key_name in search_result["errors"]:
                if key_name["code"] == "not_found":
                    module.exit_json(changed=False, msg=(
                        "record {} doesn't exist").format(record))
        # delete record in zone
        result = dns.delete_record(record=record, zone=zone)
        if result is None:
            module.exit_json(changed=True, msg=(
                "record {} successfully deleted").format(record))
        module.fail_json(msg=result)

    else:
        if not (ttl_min <= ttl <= ttl_max):
            module.fail_json(
                msg="provide a TTL value between {} and {}".format(
                    ttl_min, ttl_max))
        result = dns.get_record(record=record, zone=zone)
        if "errors" in result:
            for key_name in result["errors"]:
                if key_name["code"] == "not_found":
                    create_result = dns.create_record(zone=zone, record=record,
                                                      record_type=rtype,
                                                      data=value, ttl=ttl)
                    if create_result is not None:
                        module.exit_json(changed=True, msg=(
                            "record {} successfully created").format(record))
        module.exit_json(changed=False, msg=(
            "record {} already exist").format(record))


def main():
    run_module()


if __name__ == '__main__':
    main()
