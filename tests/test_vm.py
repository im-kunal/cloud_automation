from cloudapi.vm import get_instance


def test_get_instance():
    instance_name = "my-test-instance"
    zone = "us-central1-a"
    assert get_instance(instance_name=instance_name, zone=zone) == True
