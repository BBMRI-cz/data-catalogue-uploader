from uploader.run_metadata_collector.miseq_run_metadata_collector import CollectMiseqRunMetadata, RunInfoMMCI
import pytest
import shutil
import os
import json

FAKE_RUN_FOR_COPY = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    "..",
    "test_destination_for_copy"
))

FAKE_RUN_FOR_TESTING = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    "..",
    "test_destination_for_testing"
))

COMPLETE_FAKE_RUN_FOR_TESTING = os.path.join(FAKE_RUN_FOR_TESTING, "2020", "MiSEQ", "complete-runs",
                                             "200101_M00000_0000_00000000-00000")


def _copy_fake_destination():
    shutil.copytree(FAKE_RUN_FOR_COPY, FAKE_RUN_FOR_TESTING)


def _remove_coppied_fake_destination():
    shutil.rmtree(FAKE_RUN_FOR_TESTING)


@pytest.fixture(autouse=True)
def setup_and_teardown_organise_files(request):
    _copy_fake_destination()
    request.addfinalizer(_remove_coppied_fake_destination)
