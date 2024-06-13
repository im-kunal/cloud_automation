from __future__ import annotations
from typing import Optional
from collections.abc import Iterable
from google.cloud import compute_v1
from google.api_core.exceptions import NotFound, Conflict

import json
from cloudapi import metadata


def list_instances():
    project = metadata.get_projectid()
    client = compute_v1.InstancesClient()
    instances = client.aggregated_list(project=project)

    vm_list = {}
    for key, value in instances:
        if bool(value.instances):
            zone = key.split("/")[-1]
            zonal_instances = value.instances
            for instance in zonal_instances:
                vm_list[instance.name] = zone
    return vm_list


def get_instance(instance_name: str, zone: str):
    project = metadata.get_projectid()
    client = compute_v1.InstancesClient()
    request = compute_v1.GetInstanceRequest(
        instance=instance_name, zone=zone, project=project
    )
    try:
        instance = client.get(
            request=request
        )  # returns object of type compute.Instance
        print(instance)
        return instance
    except NotFound as e:
        print(f"No resource found. Exception: {e}")
        return None
    except Exception as e:
        print(f"Unknown Exception: {e}")
        return None


def get_instance_name(instance_name: str, zone: str):
    project = metadata.get_projectid()
    client = compute_v1.InstancesClient()
    request = compute_v1.GetInstanceRequest(
        instance=instance_name, zone=zone, project=project
    )
    try:
        instance = client.get(
            request=request
        )  # returns object of type compute.Instance
        print(instance)
        return instance.name
    except NotFound as e:
        print(f"No resource found. Exception: {e}")
        return None
    except Exception as e:
        print(f"Unknown Exception: {e}")
        return None


# https://cloud.google.com/compute/docs/instance-templates
# https://cloud.google.com/compute/docs/instance-templates/create-instance-templates#terraform
def create_instance(instance_template: dict = {}, wait: bool = True):
    """
    #https://cloud.google.com/python/docs/reference/compute/latest/google.cloud.compute_v1.types.Instance
    {
        "zone": "us-central1-a",
        "instance_resource": {
            "name": "my-sample-instance",
            "machine_type": "zones/us-central1-b/machineTypes/e2-medium",
            "network_interfaces": [
                {"subnetwork": "projects/dev-project-412419/regions/us-central1-subnetworks/vpc-us-central1"},
                {"subnetwork": "projects/dev-project-412419/regions/us-central2-subnetworks/vpc-us-central2"},
            ],
            "service_accounts": [
                {
                    "email": "450766211446-compute@developer.gserviceaccount.com",
                    "scopes": [
                        "https://www.googleapis.com/auth/cloud-platform"
                    ],
                },
            ],
            "disks": [
                {
                    "boot": True,
                    "auto_delete": True,
                    "disk_size_gb": 10,
                    "initialize_params": {"source_image": "projects/debian-cloud/global/images/debian-11-bullseye-v20240110"},
                },
            ],
            "tags": {
                "items": [

                ]
            },

            "metadata": {
                "items": [
                    {"key": "service_type", "value": "server"},
                    {"key": "env_type", "value": "dev"}
                ]
            },
        },
    }
    """
    client = compute_v1.InstancesClient()
    project = metadata.get_projectid()
    zone = instance_template.get("zone", "us-central1-a")
    instance_resource = instance_template.get("instance_resource", {})
    instance_name = instance_resource.get("name", "unknown")

    request = compute_v1.InsertInstanceRequest(
        project=project, zone=zone, instance_resource=instance_resource
    )

    # request: Optional[google.cloud.compute_v1.types.compute.InsertInstanceRequest, dict]
    # If using "request" other parameters are not required as they become part of request
    try:
        operation = client.insert(request=request)
    except Conflict as e:
        operation = None
        print(f"Conflict occurred while creating resource: {e}")

    if bool(operation):
        if wait:
            result = operation.result()

            # here we have used other parameters instead of request. Either method is okay.
            instance = client.get(project=project, zone=zone, instance=instance_name)
            nics = instance.network_interfaces
            ip_address = []
            for nic in nics:
                ip_address.append(nic.network_i_p)
            print(f"instance: {instance.name}, ip: {ip_address}")
            return {"instance": instance.name, "ip": ip_address}
    else:
        return None


def delete_instances(instance_list: str) -> {}:
    deleted_instances = []
    project = metadata.get_projectid()
    client = compute_v1.InstancesClient()
    vm_list = list_instances()
    print(vm_list)
    for instance, zone in vm_list.items():
        if instance in instance_list:
            operation = client.delete(project=project, zone=zone, instance=instance)
            deleted_instances.append({"name": instance, "zone": zone})
    return {"stoplist": deleted_instances}


def start_instances(instance_list: str) -> bool:
    started_instances = []
    project = metadata.get_projectid()
    client = compute_v1.InstancesClient()
    vm_list = list_instances()
    for instance, zone in vm_list.items():
        if instance in instance_list:
            status = client.get(project=project, zone=zone, instance=instance).status
            if status == "TERMINATED":
                client.start(project=project, zone=zone, instance=instance)
                started_instances.append({"name": instance, "zone": zone})
    return {"startlist": started_instances}


def stop_instances(instance_list: str) -> {}:
    stopped_instances = []

    project = metadata.get_projectid()
    client = compute_v1.InstancesClient()
    vm_list = list_instances()
    print(vm_list)
    for instance, zone in vm_list.items():
        if instance in instance_list:
            operation = client.stop(project=project, zone=zone, instance=instance)
            stopped_instances.append({"name": instance, "zone": zone})
    return {"stoplist": stopped_instances}


instance_template = {
    "zone": "us-central1-a",
    "instance_resource": {
        "name": "my-temp-instance",
        "machine_type": "zones/us-central1-a/machineTypes/e2-medium",
        "network_interfaces": [
            {
                "subnetwork": "projects/dev-project-412419/regions/us-central1/subnetworks/us-central1-subnet",
                "access_configs": [
                    {
                        "name": "External NAT",
                        "type_": "ONE_TO_ONE_NAT",
                        "kind": "compute#accessConfig",
                        "network_tier": "PREMIUM",
                    }
                ],
            }
        ],
        "service_accounts": [
            {
                "email": "450766211446-compute@developer.gserviceaccount.com",
                "scopes": ["https://www.googleapis.com/auth/cloud-platform"],
            }
        ],
        "disks": [
            {
                "boot": true,
                "auto_delete": true,
                "disk_size_gb": 10,
                "initialize_params": {
                    "source_image": "projects/debian-cloud/global/images/debian-11-bullseye-v20240110"
                },
            }
        ],
        "tags": {"items": ["ssh", "internet-gateway"]},
        "metadata": {
            "items": [
                {"key": "service_type", "value": "server"},
                {"key": "env_type", "value": "dev"},
            ]
        },
    },
}


def update_vm_metadata():
    pass


def apply_schedule():
    pass
