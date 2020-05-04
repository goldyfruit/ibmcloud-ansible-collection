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
module: ic_cos_bucket
short_description: Manage buckets and objects.
author: James Regis (@jregis)
version_added: "2.9"
description:
    - Manage buckets and cloud objects on IBM Cloud.
requirements:
    - "ibmcloud-python-sdk"
options:
    bucket: 
        description: bucket's name.
        required: true
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
  state:
    description:
      - Should the resource be present or absent.
    type: str
    default: present
    choices: [present, absent]
'''

EXAMPLES = '''
# Create a bucket
- ic_cos_bucket:
    bucket: ibm-bucket-baby
    mode: regional
    location: us-south
    service_instance: my-service-instance-baby

# Delete a bucket
- ic_cos_bucket:
    bucket: ibm-bucket-baby
    mode: regional
    location: us-south
    service_instance: my-service-instance-baby
    state: absent

'''

def run_module():
    module_args = dict(
        bucket=dict(
            type='str',
            required=True),
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

    object_storage = sdk.ObjectStorage()

    bucket = module.params['bucket']
    mode = module.params['mode']
    location = module.params['location']
    service_instance = module.params["service_instance"]
    state = module.params["state"]
    
    check = object_storage.get_bucket(
            bucket=bucket,
            mode=mode,
            location=location,
            service_instance=service_instance)

    if state == "absent":
        if "errors" in check:
            for key in check["errors"]:
                if key["code"] == "not_found":
                    module.exit_json(changed=False, msg=(
                        "bucket {} doesn't exist".format(bucket)))
                module.exit_json(changed=True, msg=(check))
            
        # delete the bucket
        delete_query = object_storage.delete_bucket(
                bucket=bucket,
                mode=mode,
                location=location,
                service_instance=service_instance)
        if "errors" in delete_query:
            module.fail_json(msg=(delete_query))
        module.exit_json(changed=True, msg=(
            "bucket {} successfully deleted").format(bucket))
        
    else:      
        if "errors" in check:
            for key in check["errors"]:
                if key["code"] != "not_found":
                    module.fail_json(msg=check["errors"])
                
                result = object_storage.create_bucket(
                    bucket=bucket,
                    mode=mode,
                    location=location,
                    service_instance=service_instance)
                
                if "errors" in result:
                    module.fail_json(msg=result["errors"])
                module.exit_json(changed=True, msg=(result))
        module.exit_json(changed=False, msg=(check))

def main():
    run_module()


if __name__ == '__main__':
    main()
