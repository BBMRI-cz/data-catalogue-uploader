import os
import shutil
import traceback
from typing import List

from uploader.run_metadata_collector.miseq_run_metadata_collector import CollectMiseqRunMetadata
from uploader.run_metadata_collector.nextseq_run_metadata_collector import CollectNextSeqRunMetadata
from uploader.run_metadata_collector.run_metadata_collector import RunInfoMMCI
from uploader.sample_metadata_collector.miseq_sample_metadata_collector import CollectMiseqSampleMetadata
from uploader.sample_metadata_collector.nextseq_sample_metadata_collector import CollectNextSeqSampleMetadata
from uploader.metadata_import import MetadataImport
from uploader.file_helpers import get_all_runs_with_data_for_catalogue
from uploader.manage_libraries import LibrariesManager
import argparse

from uploader.sample_metadata_collector.sample_metadata_collector import SampleInfoMMCI


def process_runs(run_paths: List[str], libraries_folders: str, importer: MetadataImport, run_type: str) -> None:
    """Process and upload run data for each run."""
    for absolute_run_path in run_paths:
        try:
            print(f"Processing {absolute_run_path}...")
            run_metadata = collect_run_metadata(absolute_run_path, run_type)
            catalog_info_folder = os.path.join(absolute_run_path, "catalog_info_per_pred_number")
            lib_manager = LibrariesManager(libraries_folders, absolute_run_path)

            for sample_id in os.listdir(catalog_info_folder):
                process_and_upload_sample(sample_id, catalog_info_folder, absolute_run_path, run_metadata, lib_manager, importer, run_type)

            open(os.path.join(absolute_run_path, ".uploaded"), "w").close()

        except FileNotFoundError as e:
            print(f"Error: Missing file in run {absolute_run_path}: {e}")
            print("Full stack trace:")
            print(traceback.format_exc())
        except Exception as e:
            print(f"Unexpected error in run {absolute_run_path}: {e}")
            print("Full stack trace:")
            print(traceback.format_exc())


def process_and_upload_sample(sample_id: str, catalog_info_folder: str, absolute_run_path: str, run_metadata: RunInfoMMCI, lib_manager: LibrariesManager, importer: MetadataImport, run_type: str) -> None:
    """Process and upload sample data."""
    clinical_info_path = os.path.join(catalog_info_folder, sample_id)
    sample_id = sample_id.replace(".json", "")
    sample_path = os.path.join(absolute_run_path, "Samples", sample_id)
    lib_data = lib_manager.get_data_from_libraries(sample_id)

    sample_metadata = collect_sample_metadata(absolute_run_path, sample_path, catalog_info_folder, run_type)

    # upload sample to catalogue
    importer.upload(run_metadata, sample_metadata, clinical_info_path, run_type, lib_data)

def collect_run_metadata(absolute_run_path: str, run_type: str) -> RunInfoMMCI:
    """Collect metadata for the run based on the run type."""
    if run_type == "MiSEQ":
        return CollectMiseqRunMetadata(absolute_run_path).collect()
    elif run_type == "NextSeq":
        return CollectNextSeqRunMetadata(absolute_run_path).collect()
    else:
        raise ValueError(f"Unsupported run type: {run_type}")

def collect_sample_metadata(absolute_run_path: str, sample_path: str, catalog_info_folder: str, run_type: str) -> SampleInfoMMCI:
    """Collect metadata for the sample based on the run type."""
    if run_type == "MiSEQ":
        return CollectMiseqSampleMetadata(absolute_run_path, sample_path, catalog_info_folder).collect()
    elif run_type == "NextSeq":
        return CollectNextSeqSampleMetadata(absolute_run_path, sample_path, catalog_info_folder).collect()
    else:
        raise ValueError(f"Unsupported run type: {run_type}")

def run(organised_files_folders, wsi_folders, libraries_folders):
    molgenis_login = os.environ["CATALOG_LOGIN"]
    molgenis_password = os.environ["CATALOG_PASSWORD"]

    importer = MetadataImport(wsi_folders,
                              libraries_folders,
                              molgenis_login,
                              molgenis_password)

    miseq_run_paths_for_catalogue_upload = get_all_runs_with_data_for_catalogue(organised_files_folders, wanted_run_type="MiSEQ")
    print("MiSeq:", miseq_run_paths_for_catalogue_upload)

    nextseq_run_paths_for_catalogue_upload = get_all_runs_with_data_for_catalogue(organised_files_folders, wanted_run_type="NextSeq")
    print("NextSeq:", nextseq_run_paths_for_catalogue_upload)

    process_runs(miseq_run_paths_for_catalogue_upload, libraries_folders, importer, "MiSEQ")
    process_runs(nextseq_run_paths_for_catalogue_upload, libraries_folders, importer, "NextSeq")

    print("Upload process completed.")
    del importer

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="Uploader",
                                     description="Organise pseudonymized runs into a specifed output folder \n." +
                                                 " It is important to use full paths")
    parser.add_argument("-o", "--organised_runs", type=str, required=True, help="")
    parser.add_argument("-w", "--wsi", type=str, required=True, help="Path to a WSI folder")
    parser.add_argument("-d", "--libraries", type=str, required=True, help="Path to a libraries document")
    args = parser.parse_args()

    run(args.organised_runs, args.wsi, args.libraries)
