#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.cis.storage import object as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_cos_object
short_description: Manage COS (Cloud Object Storage) objects on IBM Cloud.
author: James Regis (@jregis)
version_added: "2.9"
description:
  - This module create or delete COS objects.
  - By default the module will look for an existing service instance associated
    to the Cloud Object Storage.
requirements:
  - "ibmcloud-python-sdk"
options:
  bucket:
    description:
      - Bucket name.
    type: str
    required: true
  body:
    description:
      - Content to store into the object.
      - Mutually exclusive with C(path) argument.
    type: str
  path:
    description:
      - Path to the file to upload.
      - Mutually exclusive with C(body) argument.
    type: str
  object:
    description:
      - Name to set once the object is uploaded.
    type: str
    required: true
  mode:
    description:
      - Replication mode of the buckets.
    type: str
  location:
    description:
      - Geographic bucket location.
    type: str
  service_instance:
    description:
      - Name or GUID of the service instance.
    type: str
  state:
    description:
      - Should the resource be present or absent.
    type: str
    default: present
    choices: [present, absent]
'''

EXAMPLES = r'''
- name: Upload a file with a custom content.
  ic_cos_object:
    bucket: ibmcloud-bucket-baby
    object: ibmcloud-object-baby
    body: "This is my IBM Cloud content, baby!"

- name: Upload an object with a custom content with specific information
  ic_cos_object:
    bucket: ibmcloud-bucket-baby
    object: ibmcloud-object-baby
    body: "This is my IBM Cloud content, baby!"
    mode: regional
    location: us-south
    service_instance: ibmcloud-resource-instance-baby

- name: Upload an existing file
  ic_cos_object:
    bucket: ibmcloud-bucket-baby
    object: ibmcloud-object-baby
    path: /home/ibmcloud/download/watson.png

- name: Delete object from a bucket
  ic_cos_object:
    bucket: ibmcloud-bucket-baby
    object: ibmcloud-object-baby
'''


def run_module():
    module_args = dict(
        body=dict(
            type='str',
            required=False),
        object=dict(
            type='str',
            required=False),
        path=dict(
            type='str',
            required=False),
        bucket=dict(
            type='str',
            required=True),
        acl=dict(
            type='str',
            choices=['private', 'public-read', 'public-read-write',
                     'authenticated-read', 'aws-exec-read',
                     'bucket-owner-read', 'bucket-owner-full-control'],
            required=False),
        mode=dict(
            type='str',
            choices=['regional', 'direct_regional', 'cross_region',
                     'direct_us_cross_region', 'direct_eu_cross_region',
                     'direct_ap_cross_region', 'single_data_center',
                     'direct_single_data_center'],
            default='regional',
            required=False),
        location=dict(
            type='str',
            choices=['us-south', 'us-east', 'eu-united-kingdom', 'eu-germany',
                     'ap-autralia', 'ap-japan', 'us-cross-region',
                     'eu-cross-region', 'ap-cross-region', 'us', 'dallas',
                     'san-jose', 'eu', 'amsterdam', 'frankfurt', 'milan', 'ap',
                     'tokyo', 'seoul', 'hong-kong', 'chennai', 'melbourne',
                     'mexico', 'montreal', 'oslo', 'paris', 'sao-paulo',
                     'seoul', 'singapore', 'toronto'],
            default='us-south',
            required=False),
        service_instance=dict(
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

    object = module.params['object']
    path = module.params['path']
    body = module.params['body']
    acl = module.params['acl']
    bucket = module.params['bucket']
    mode = module.params['mode']
    location = module.params['location']
    service_instance = module.params["service_instance"]
    state = module.params["state"]

    sdk_object = sdk.Object(
                    mode=mode,
                    location=location,
                    service_instance=service_instance
                )

    if path and body:
        msg = "path and body are mutually exclusive"
        module.fail_json(changed=False, msg=msg)

    if state == "absent":
        check = sdk_object.get_object(bucket, object)
        if "Key" in check:
            result = sdk_object.delete_object(bucket, object)
            if "errors" in result:
                module.fail_json(msg=result)

            payload = {"object": object, "bucket": bucket, "status": "deleted"}
            module.exit_json(changed=True, msg=payload)

        payload = {"object": object, "bucket": bucket, "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        result = None
        if path:
            result = sdk_object.upload_file(
                key=object,
                bucket=bucket,
                path=path,
                acl=acl
            )

            if "errors" in result:
                module.fail_json(msg=result)
        elif body:
            result = sdk_object.put_object(
                key=object,
                bucket=bucket,
                body=body,
                acl=acl
            )
            if "errors" in result:
                module.fail_json(msg=result)

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
