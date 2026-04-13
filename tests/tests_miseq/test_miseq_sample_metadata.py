from uploader.sample_metadata_collector.miseq_sample_metadata_collector import CollectMiseqSampleMetadata
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

FAKE_SAMPLE_DATA = os.path.join(COMPLETE_FAKE_RUN_FOR_TESTING, "Samples",
                                "mmci_predictive_00000000-0000-0000-0000-000000000001")

FAKE_CATALOGUE_INFO = os.path.join(COMPLETE_FAKE_RUN_FOR_TESTING, "catalog_info_per_pred_number")


def _copy_fake_run():
    shutil.copytree(FAKE_RUN_FOR_COPY, FAKE_RUN_FOR_TESTING)


def _remove_coppied_fake_run():
    shutil.rmtree(FAKE_RUN_FOR_TESTING)


@pytest.fixture(autouse=True)
def setup_and_teardown_organise_files(request):
    _copy_fake_run()
    request.addfinalizer(_remove_coppied_fake_run)
