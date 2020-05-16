#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.cis.storage import bucket as sdk


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_cos_bucket
short_description: Manage COS (Cloud Object Storage) buckets on IBM Cloud.
author: James Regis (@jregis)
version_added: "2.9"
description:
  - This module create or delete COS bucket.
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
  grant_full_control:
    description:
      - Allows grantee the read, write, read ACP, and write ACP permissions
        on the bucket.
    type: str
  grant_read:
    description:
      - Allows grantee to list the objects in the bucket.
    type: str
  grant_readacp:
    description:
      - Allows grantee to read the bucket ACL.
    type: str
  grant_write:
    description:
      - Allows grantee to create, overwrite, and delete any object in the
        bucket.
    type: str
  grant_write_acp:
    description:
      - Allows grantee to write the ACL for the applicable bucket.
    type: str
  ibm_sse_kp_encryptions_algorithm:
    description:
      - The encryption algorithm that will be used for objects stored in the
        newly created bucket.
    type: str
  ibm_sse_kp_customer_root_key_crn:
    description:
      - Container for describing the KMS-KP Key CRN.
    type: str
  state:
    description:
      - Should the resource be present or absent.
    type: str
    default: present
    choices: [present, absent]
'''

EXAMPLES = r'''
- name: Create a simple bucket
  ic_cos_bucket:
    bucket: ibmcloud-bucket-baby

- name: Create a bucket in with specific location, service instance and mode
  ic_cos_bucket:
    bucket: ibmcloud-bucket-baby
    mode: regional
    location: us-south
    service_instance: ibmcloud-resource-instance-baby

- name: Delete a bucket
  ic_cos_bucket:
    bucket: ibmcloud-bucket-baby
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
        acl=dict(
            type='str',
            required=False),
        grant_full_control=dict(
            type='str',
            required=False),
        grant_read=dict(
            type='str',
            required=False),
        grant_read_acp=dict(
            type='str',
            required=False),
        grant_write=dict(
            type='str',
            required=False),
        grant_write_acp=dict(
            type='str',
            required=False),
        ibm_sse_kp_encryptions_algorithm=dict(
            type='str',
            required=False),
        ibm_sse_kp_customer_root_key_crn=dict(
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

    bucket = module.params["bucket"]
    mode = module.params["mode"]
    location = module.params["location"]
    service_instance = module.params["service_instance"]
    acl = module.params["acl"]
    grant_full_control = module.params["grant_full_control"]
    grant_read = module.params["grant_read"]
    grant_read_acp = module.params["grant_read_acp"]
    grant_write = module.params["grant_write"]
    grant_write_acp = module.params["grant_write_acp"]
    ibm_sse_kp_encryptions_algorithm = module.params[
        "ibm_sse_kp_encryptions_algorithm"]
    ibm_sse_kp_customer_root_key_crn = module.params[
        "ibm_sse_kp_customer_root_key_crn"]
    state = module.params["state"]

    sdk_bucket = sdk.Bucket(
                    mode=mode,
                    location=location,
                    service_instance=service_instance
                )

    check = sdk_bucket.get_bucket(bucket)

    if state == "absent":
        if "Name" in check:
            result = sdk_bucket.delete_bucket(bucket)
            if "errors" in result:
                module.fail_json(msg=result)

            payload = {"bucket": bucket, "status": "deleted"}
            module.exit_json(changed=True, msg=payload)

        payload = {"bucket": bucket, "status": "not_found"}
        module.exit_json(changed=False, msg=payload)
    else:
        if "Name" in check:
            module.exit_json(changed=False, msg=check)

        result = sdk_bucket.create_bucket(
            bucket=bucket,
            acl=acl,
            grant_full_control=grant_full_control,
            grant_read=grant_read,
            grant_read_acp=grant_read_acp,
            grant_write=grant_write,
            grant_write_acp=grant_write_acp,
            ibm_sse_kp_encryptions_algorithm=ibm_sse_kp_encryptions_algorithm,
            ibm_sse_kp_customer_root_key_crn=ibm_sse_kp_customer_root_key_crn
        )

        if "errors" in result:
            module.fail_json(msg=result)

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
