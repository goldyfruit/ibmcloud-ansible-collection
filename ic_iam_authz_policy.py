#!/usr/bin/env python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)


from ansible.module_utils.basic import AnsibleModule
from ibmcloud_python_sdk.iam import policy as sdk
from ibmcloud_python_sdk.auth import decode_token


ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: ic_iam_authz_policy
short_description: Manage IAM authorization policies on IBM Cloud.
author: Gaëtan Trellu (@goldyfruit)
version_added: "2.9"
description:
  - An IAM policy enables a subject to access a resource. These policies are
    used in access decisions when calling APIs for IAM-enabled services.
requirements:
  - "ibmcloud-python-sdk"
options:
  policy:
    description:
      - The policy ID.
      - Only required for policy deletion.
    type: str
  subjects:
    description:
      - The subject attribute values that must match in order for this policy
        to apply in a permission decision.
    type: dict
    suboptions:
      source_service_name:
        description:
          - The source service name.
        type: str
      source_resource_type:
        description:
          - Resource type of source service
        type: str
      source_service_instance:
        description:
          - The source resource instance name or ID.
        type: str
  resources:
    description:
      - The attributes of the resource. Note that only one resource is allowed
        in a policy.
    type: dict
    suboptions:
      target_service_name:
        description:
          - The target service name.
        type: str
      target_resource_type:
        description:
          - Resource type of target service.
        type: str
      target_service_instance:
        description:
          - The target resource instance name or ID.
        type: str
  roles:
    description:
      - A set of role cloud resource names granted by the policy.
    type: list
  state:
    description:
      - Should the resource be present or absent.
    type: str
    default: present
    choices: [present, absent]
'''

EXAMPLES = r'''
- name: Allow Infrastructure Image to communicate with Cloud Object Storage
  ic_iam_authz_policy:
    subjects:
      source_service_name: is
      source_resource_type: image
    resources:
      target_service_name: cloud-object-storage
      target_service_instance: ibmcloud-resource-instance-baby
    roles:
      - Reader
      - Writer

- name: Delete authorization policy
  ic_iam_authz_policy:
    policy: a0a03ee9-48c7-4c58-be49-6f473a98ae16
    state: absent
'''


# Retrieve account ID
account_id = decode_token()['account']['bss']

# CRN roles
crn = "crn:v1:bluemix:public:iam::::serviceRole:"


# Subjects payload
def _set_subjets(data):
    subject_attributes = [
      {"name": "accountId", "value": account_id},
      {"name": "serviceName", "value": data['source_service_name']}
    ]
    if data['source_resource_type']:
        source_resource_type = {
            "name": "resourceType",
            "value": data['source_resource_type'],
        }
        subject_attributes.append(source_resource_type)
    elif data['source_service_instance']:
        source_resource_instance = {
            "name": "serviceInstance",
            "value": data['source_service_instance'],
        }
        subject_attributes.append(source_resource_instance)

    sa = {}
    sa['attributes'] = subject_attributes

    return [sa]


# Resource payload
def _set_resources(data):
    resource_attributes = [
      {"name": "accountId", "value": account_id},
      {"name": "serviceName", "value": data['target_service_name']}
    ]
    if data['target_resource_type']:
        target_resource_type = {
            "name": "resourceType",
            "value": data['target_resource_type'],
        }
        resource_attributes.append(target_resource_type)
    elif data['target_service_instance']:
        target_resource_instance = {
            "name": "serviceInstance",
            "value": data['target_service_instance'],
        }
        resource_attributes.append(target_resource_instance)

    ra = {}
    ra['attributes'] = resource_attributes

    return [ra]


def _check_policy(data):
    for key in data["errors"]:
        if key["code"] == "policy_conflict_error":
            return True
        elif key["code"] == "policy_not_found":
            return True
    return False


def run_module():
    module_args = dict(
        policy=dict(
            type='str',
            required=False),
        subjects=dict(
            type='dict',
            options=dict(
                source_service_name=dict(
                    type='str',
                    required=False),
                source_resource_type=dict(
                    type='str',
                    required=False),
                source_service_instance=dict(
                    type='str',
                    required=False),
                ),
            required=False),
        roles=dict(
            type='list',
            required=False),
        resources=dict(
            type='dict',
            options=dict(
                target_service_name=dict(
                    type='str',
                    required=False),
                target_resource_type=dict(
                    type='str',
                    required=False),
                target_service_instance=dict(
                    type='str',
                    required=False),
                ),
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

    iam_policy = sdk.Policy()

    policy = module.params['policy']
    subjects = module.params['subjects']
    roles = module.params['roles']
    resources = module.params['resources']
    state = module.params['state']

    roles_crn = []
    # Check if roles is defined before running the loop
    for role in [role for role in (roles or [])]:
        roles_crn.append("{}{}".format(crn, role))

    if state == "absent":
        if not policy:
            module.fail_json(changed=False, msg="policy parameter is required")

        result = iam_policy.delete_policy(policy)
        if "errors" in result:
            if _check_policy(result):
                payload = {"policy": policy, "status": "not_found"}
                module.exit_json(changed=False, msg=payload)
            module.fail_json(msg=result)

        module.exit_json(changed=True, msg=result)
    else:
        result = iam_policy.create_policy(
          type="authorization",
          subjects=_set_subjets(subjects),
          resources=_set_resources(resources),
          roles=roles_crn
        )

        if "errors" in result:
            if _check_policy(result):
                info = result["errors"][0]["details"]["conflicts_with"]
                payload = {"policy": info["policy"],
                           "status": "already_exists"}
                module.exit_json(changed=False, msg=payload)
            module.fail_json(msg=result)

        module.exit_json(changed=True, msg=result)


def main():
    run_module()


if __name__ == '__main__':
    main()
