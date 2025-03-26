import os
from uploader.run_metadata_collector.miseq_run_metadata_collector import CollectMiseqRunMetadata
from uploader.run_metadata_collector.nextseq_run_metadata_collector import CollectNextSeqRunMetadata
from uploader.sample_metadata_collector.miseq_sample_metadata_collector import CollectMiseqSampleMetadata
from uploader.sample_metadata_collector.nextseq_sample_metadata_collector import CollectNextSeqSampleMetadata
from uploader.metadata_import import MetadataImport
from uploader.file_helpers import get_all_runs_with_data_for_catalogue
from uploader.manage_libraries import LibrariesManager
import argparse


def run(organised_files_foldes, wsi_folders, libraries_folders):
    molgenis_login = os.environ["CATALOG_LOGIN"]
    molgenis_password = os.environ["CATALOG_PASSWORD"]

    importer = MetadataImport(wsi_folders,
                              libraries_folders,
                              molgenis_login,
                              molgenis_password)

    miseq_run_paths_for_catalogue_upload = get_all_runs_with_data_for_catalogue(organised_files_foldes,
                                                                                wanted_run_type="MiSEQ")
    print("MiSeq:", miseq_run_paths_for_catalogue_upload)

    nextseq_run_paths_for_catalogue_upload = get_all_runs_with_data_for_catalogue(organised_files_foldes,
                                                                                  wanted_run_type="NextSeq")
    print("NextSeq:", nextseq_run_paths_for_catalogue_upload)

    # miseq upload
    for absolute_run_path in miseq_run_paths_for_catalogue_upload:
        print(absolute_run_path)
        lib_manager = LibrariesManager(libraries_folders, absolute_run_path)
        run_metadata = CollectMiseqRunMetadata(absolute_run_path).collect()
        catalog_info_folder = os.path.join(absolute_run_path, "catalog_info_per_pred_number")

        for sample_id in os.listdir(catalog_info_folder):
            clinical_info_path = os.path.join(catalog_info_folder, sample_id)
            sample_id = sample_id.replace(".json", "")
            sample_path = os.path.join(absolute_run_path, "Samples", sample_id)
            lib_data = lib_manager.get_data_from_libraries(sample_id)
            sample_metadata = CollectMiseqSampleMetadata(absolute_run_path, sample_path, catalog_info_folder).collect()

            importer.upload(run_metadata, sample_metadata, clinical_info_path, "MiSEQ", lib_data)
        open(os.path.join(absolute_run_path, ".uploaded"), "w").close()


    # nextseq upload
    for absolute_run_path in nextseq_run_paths_for_catalogue_upload:
        print(absolute_run_path)
        run_metadata = CollectNextSeqRunMetadata(absolute_run_path).collect()
        catalog_info_folder = os.path.join(absolute_run_path, "catalog_info_per_pred_number")

        for sample_id in os.listdir(catalog_info_folder):
            clinical_info_path = os.path.join(catalog_info_folder, sample_id)
            sample_id = sample_id.replace(".json", "")
            sample_path = os.path.join(absolute_run_path, "Samples", sample_id)
            sample_metadata = CollectNextSeqSampleMetadata(absolute_run_path, sample_path, catalog_info_folder).collect()
            importer.upload(run_metadata, sample_metadata, clinical_info_path, "NextSeq")
        open(os.path.join(absolute_run_path, ".uploaded"), "w").close()

    print("Done")

    del importer


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
