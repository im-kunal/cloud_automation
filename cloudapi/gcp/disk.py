from google.cloud import compute_v1


def get_disk(project: str, zone: str, disk: str) -> str:
    """Returns disk object for a disk

    Args:
        project (str): project where disk is hosted
        disk (str): Name of the disk

    Returns:
        str: disk object
    """
    client = compute_v1.DisksClient()
    disk = client.get(project=project, zone=zone, disk=disk)
    return disk


def get_source_disk(project: str, zone: str, disk: str):
    """Returns full source URL of the disk

    Args:
        project (str): project of the disk
        zone (str): zone of the disk
        disk (str): name of the disk

    Returns:
        str: Fully qualified url of the disk (e.g. projects/project/zones/zone/disks/disk)
    """
    disk_obj = get_disk(project, zone, disk)
    return disk_obj.source_disk

def create_disk():
    pass

def delete_disk():
    pass


