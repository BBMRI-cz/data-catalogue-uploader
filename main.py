import logging
import os
from uploader.metadata_managers.miseq_run_metadata import CollectRunMetadata
from uploader.metadata_managers.miseq_sample_metadata import CollectSampleMetadata
from uploader.import_metadata import MolgenisImporter
from uploader.file_helpers import get_all_runs_with_data_for_catalogue
import argparse


def run(organised_files_foldes, wsi_folders, libraries_folders):
    molgenis_login = None  # os.environ["CATALOG_LOGIN"]
    molgenis_password = None  # os.environ["CATALOG_PASSWORD"]

    run_paths_for_catalogue_upload = get_all_runs_with_data_for_catalogue(organised_files_foldes)

    for absolute_run_path in run_paths_for_catalogue_upload:
        print(absolute_run_path)
        logging.info("Collecting metadata...")
        upload_to_catalog = CollectRunMetadata(absolute_run_path)()

        catalog_info_folder = os.path.join(absolute_run_path, "catalog_info_per_pred_number")
        for sample_id in os.listdir(catalog_info_folder):
            sample_id = sample_id.replace(".json", "")
            sample_path = os.path.join(absolute_run_path, "Samples", sample_id)
            CollectSampleMetadata(absolute_run_path, sample_path, catalog_info_folder)()

        logging.info("Uploading data to catalog...")
        importer = MolgenisImporter(absolute_run_path,
                                    wsi_folders,
                                    libraries_folders,
                                    molgenis_login,
                                    molgenis_password)
        importer()
        # del importer


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog="Uploader",
                                     description="Organise pseudonymized runs into a specifed output folder \n." +
                                                 " It is important to use full paths")
    parser.add_argument("-o", "--organised_runs", type=str, required=True, help="")
    parser.add_argument("-w", "--wsi", type=str, required=True, help="Path to a WSI folder")
    parser.add_argument("-d", "--libraries", type=str, required=True, help="Path to a libraries document")
    args = parser.parse_args()

    run(args.organised_runs, args.wsi, args.libraries)


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
