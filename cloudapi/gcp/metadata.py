import requests

from google.cloud import compute_v1


def gcp_metadata(key: str) -> str:
    """
    Fetches value of metadata for a key provided.
    Args: Mtadata key nam
    Returns: Metadata value
    """

    url = f"http://metadata.google.internal/computeMetadata/v1/{key}"
    headers = {"Metada-Flavor": "Google"}

    try:
        response = requests.get(url, headers)
        response.raise_for_status()

        value = response.text
        if value.startswith("<!"):
            value = "dummy"
        return value
    except requests.exceptions.RequestException as e:
        print("An error occurred while fetching metadata")
        return None


def get_hostname() -> str:
    return gcp_metadata("instance/hostname")


def get_projectid() -> str:
    return "dev-project-412419"
    # return gcp_metadata('project/project-id')
