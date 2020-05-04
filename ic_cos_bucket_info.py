#!/usr/bin/env python

# GNU General Public License v3.0+

from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.cis.storage import object_storage as sdk

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: ic_cos_info
short_description: Get a list of buckets.
author: James Regis (@jregis)
version_added: "2.9"
description:
    - Get a list of buckets hosted on IBM Cloud.
requirements:
    - "ibmcloud-python-sdk"
options:
    mode:
        description: replication mode of the buckets.
        required: true
    location:
        description:
            -  Geographic bucket location.
        required: true        
    service_instance:
        description:
            -  Name or UUID of the service_instance associated with the cloud 
               object storage.
        required: true
'''

EXAMPLES = '''
# Get all buckets in the zone
- ic_cos_info:
    mode: regional
    location: us-south
    service_instance: my-service-instance-baby 
'''

def run_module():
    module_args = dict(
        mode=dict(
            type='str',
            choices=['regional', 'direct_regional', 'cross_region', 
            'direct_us_cross_region', 'direct_eu_cross_region', 
            'direct_ap_cross_region', 'single_data_center', 
            'direct_single_data_center'],
            required=True),
        location=dict(
            type='str',
            choices=['us-south', 'us-east', 'eu-united-kingdom', 'eu-germany',
            'ap-autralia', 'ap-japan', 'us-cross-region', 'eu-cross-region',
            'ap-cross-region', 'us', 'dallas', 'san-jose', 'eu', 'amsterdam',
            'frankfurt', 'milan', 'ap', 'tokyo', 'seoul', 'hong-kong',
            'chennai', 'melbourne', 'mexico', 'montreal', 'oslo', 'paris', 
            'sao-paulo', 'seoul', 'singapore', 'toronto'],
            required=False),
        service_instance=dict(
            type='str',
            required=True),
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )

    object_storage = sdk.ObjectStorage()

    mode = module.params['mode']
    location = module.params['location']
    service_instance = module.params["service_instance"]

    check = object_storage.get_buckets(mode=mode, location=location,
        service_instance=service_instance)

    if "errors" in check:
        for key in check["errors"]:
            if key["code"] != "not_found":
                module.fail_json(msg=check["errors"])
            else:
                module.exit_json(changed=False, msg=(
                    "The service instance {} doesn't exist".format(
                        service_instance)))

    module.exit_json(changed=True, msg=(check))

def main():
    run_module()


if __name__ == '__main__':
    main()
