# IBM Cloud Ansible Collections

This collection allows interactions with IBM Cloud VPC, Classic Infrastructure, etc... Modules will consume resources and make sure idempotency is respected as it should.

This collection leverage IBM Cloud Python SDK(https://pypi.org/project/ibmcloud-python-sdk)

## Requirements

IBM Cloud API keys are required, to setup keys please have a look at the official [IBM Cloud documentation](https://cloud.ibm.com/docs/iam?topic=iam-manapikey).

- [IBM Cloud Access (IAM) API key](https://cloud.ibm.com/docs/iam?topic=iam-userapikey)
- [Classic Infrastructure API key](https://cloud.ibm.com/docs/iam?topic=iam-classic_keys)

To setup credential please reead the [documentation](https://github.com/goldyfruit/ibmcloud-python-sdk).

- ibmcloud-python-sdk >= 1.0.0
- ansible >= 2.9

## Install

```shell
$ ansible-galaxy collection install goldyfruit.ibmcloud_automation
```

The collection will be automatically installed in `~/.ansible/collections/ansible_collections/goldyfruit/` directory.
