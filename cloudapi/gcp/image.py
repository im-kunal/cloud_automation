# https://cloud.google.com/python/docs/reference/compute/latest/google.cloud.compute_v1.services.images.ImagesClient
# https://cloud.google.com/python/docs/reference/compute/latest/google.cloud.compute_v1.services.images

from google.cloud import compute_v1


def create_image(project: str, imagename: str, family: str, source_disk: str) -> str:
    """Creates custom image of a VM
    Args:
        instance (str): Name of the instance to make image from
        zone (str): Zone where instance is running
    Returns:
        str: Image name
    """
    client = compute_v1.ImagesClient()
    image = compute_v1.Image()
    image.name = imagename
    image.family = family
    image.source_disk = source_disk
    operation = client.insert(project=project, image_resource=image)
    operation.result()
    return operation


def delete_image():
    pass


def get_image():
    pass


def get_image_with_pattern():
    pass


print(
    create_image(
        project="dev-project-412419",
        imagename="test-image-1",
        family="test-image",
        source_disk="projects/dev-project-412419/zones/us-central1-a/disks/my-temp-instance",
    )
)
