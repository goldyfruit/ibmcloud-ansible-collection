# IBM Cloud Ansible Collections

This collection allows interactions with IBM Cloud VPC, Classic Infrastructure, etc... Modules will consume resources and make sure idempotency is respected as it should.

This collection leverage [IBM Cloud Python SDK](https://pypi.org/project/ibmcloud-python-sdk)

## Requirements

IBM Cloud API keys are required, to setup keys please have a look at the official [IBM Cloud documentation](https://cloud.ibm.com/docs/iam?topic=iam-manapikey).

- [IBM Cloud Access (IAM) API key](https://cloud.ibm.com/docs/iam?topic=iam-userapikey)
- [Classic Infrastructure API key](https://cloud.ibm.com/docs/iam?topic=iam-classic_keys)

To setup credential please reead the [documentation](https://github.com/goldyfruit/ibmcloud-python-sdk).

- `ibmcloud-python-sdk` >= `1.0.0`
- `ansible` >= `2.9`

```shell
$ pip install ansible ibmcloud-python-sdk
```

## Install

```shell
$ ansible-galaxy collection install goldyfruit.ibmcloud_automation
```

The collection will be automatically installed in `~/.ansible/collections/ansible_collections/goldyfruit/` directory.

## Examples

### Create VPC and VSI

```yaml
---
- hosts: localhost
  connection: local
  gather_facts: no
  collections:
    - goldyfruit.ibmcloud_automation

  vars:
    ibmcloud_file: "{{ lookup('env','HOME') }}/.ibmcloud/clouds.yaml"

  environment:
    IC_CONFIG_FILE: "{{ ibmcloud_file }}"

  tasks:
    - import_role:
        name: quickstart
```

### Upload QCOW2 image for VPC

```yaml
---
- hosts: localhost
  connection: local
  gather_facts: no
  collections:
    - goldyfruit.ibmcloud_automation

  vars:
    ibmcloud_file: "{{ lookup('env','HOME') }}/.ibmcloud/clouds.yaml"

  environment:
    IC_CONFIG_FILE: "{{ ibmcloud_file }}"

  tasks:
    - import_role:
        name: quickstart_image
```
