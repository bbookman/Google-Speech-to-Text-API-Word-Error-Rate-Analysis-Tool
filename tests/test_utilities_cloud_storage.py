import pytest

def test_get_bucket_from_uri():
    from utilities.cloud_storage import GCS
    gcs = GCS()
    uri = "gs://foo/bar"
    expected_bucket = "foo"
    expected_folder = "bar"
    bucket, folder = gcs._parse_uri(uri)
    assert bucket == expected_bucket
    assert folder == expected_folder

def test_get_file_list():
    from utilities.cloud_storage import GCS
    gcs = GCS()
    uri = "gs://cloud-samples-data/speech"
    expected = "brooklyn_bridge"
    result = gcs.get_file_list(uri)
    success = False
    for item in result:
        if expected in item:
            success = True
    assert success

def test_read_ref():
    from utilities.cloud_storage import GCS
    gcs = GCS()
    uri = "gs://brb/test_audio_n_truth/"
    text_file = "test.txt"
    expected = "hello world"
    result = gcs.read_ref(uri, text_file)
    assert result == expected



