#!/usr/bin/env python

# GNU General Public License v3.0+

from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.cis.storage import object_storage as sdk

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_cos_object
short_description: Manage buckets and objects.
author: James Regis (@jregis)
version_added: "2.9"
description:
    - Manage buckets and cloud objects on IBM Cloud.
requirements:
    - "ibmcloud-python-sdk"
options:
    bucket: 
        description: Bucket's name.
        required: true
    body: 
        description: Object's content. Mutually exclusive with **path**.
        required: false
    path:
        description: File's path to upload in the bucket.Mutually exclusive 
        with **body**
        required: false.
    key:
        description: Object key for which the PUT operation was initiated.
        Typically, the object's name.
    mode:
        description: Replication mode of the buckets.
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

EXAMPLES = r'''
# Put a object with "this is a content" as content in a bucket
- ic_cos_object:
    body: 'this is a content' 
    key: it-s-an-object-baby
    bucket: ibm-bucket-baby
    mode: regional
    location: us-south
    service_instance: my-service-instance-baby

# Upload a file to a bucket
- ic_cos_object:
    path: '/home/duke/berserk.avi' 
    key: it-s-a-video-baby
    bucket: ibm-bucket-baby
    mode: regional
    location: us-south
    service_instance: my-service-instance-baby

# Delete an object in a bucket
- ic_cos_object:
    key: it-s-an-object-baby
    bucket: ibm-bucket-baby
    mode: regional
    location: us-south
    service_instance: my-service-instance-baby

'''

def run_module():
    module_args = dict(
        body=dict(
            type='str',
            required=False),
        key=dict(
            type='str',
            required=True),
        path=dict(
            type='str',
            required=False),    
        bucket=dict(
            type='str',
            required=True),
        acl=dict(
            type='str',
            choices=['private','public-read','public-read-write',
            'authenticated-read','aws-exec-read','bucket-owner-read',
            'bucket-owner-full-control'],
            required=False),
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
            required=True),
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

    obj_key = module.params['key']
    path = module.params['path']
    body = module.params['body']
    acl = module.params['acl']
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

    if "errors" in check:
        for key in check["errors"]:
            if key["code"] == "not_found":
                module.exit_json(changed=False, msg=(
                    "bucket {} should exist before any operation.".format(
                                bucket)))
    if state == "absent":
        
        search = object_storage.get_object(
            key=obj_key,
            bucket=bucket,
            mode=mode,
            location=location,
            service_instance=service_instance,
        )
        if "errors" in search:
            module.exit_json(changed=False, msg=(
                "object {} doesn't exist".format(obj_key)))

        delete_result = object_storage.delete_object(
            key=obj_key,
            bucket=bucket,
            mode=mode,
            location=location,
            service_instance=service_instance
        )     

        if "status" in delete_result:
            if delete_result["status"] == "deleted":
                payload = {"msg": "object {} successfully deleted".format(obj_key)}
                module.exit_json(changed=True, msg=(payload))
        module.fail_json(msg=delete_result)

    else: 
        if path is not None and body is not None:
            module.fail_json(changed=False, msg=(
                "path and body are mutually exclusive"))

        if path is not None:
            result = object_storage.upload_file(
                key=obj_key,
                bucket=bucket,
                path=path,
                acl=acl,
                mode=mode,
                location=location,
                service_instance=service_instance)

            if "errors" in result:
                module.fail_json(msg=result["errors"])
            module.exit_json(changed=True, msg=(result))

        if body is not None:
            result = object_storage.put_object(
                key=obj_key,
                bucket=bucket,
                body=body,
                acl=acl,
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
