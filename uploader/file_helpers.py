import os


def get_all_runs_with_data_for_catalogue(organised_folder: str) -> [str]:
    runs_to_precess_for_catalogue = []
    for year in os.listdir(organised_folder):
        for run_type in os.listdir(os.path.join(organised_folder, year)):
            multiple_runs_path = os.path.join(organised_folder, year, run_type)
            for run in os.listdir(multiple_runs_path):
                run_catalog_info = os.path.join(multiple_runs_path, run, "catalog_info_per_pred_number")
                if os.path.exists(run_catalog_info) and os.listdir(run_catalog_info):
                    runs_to_precess_for_catalogue.append(os.path.join(multiple_runs_path, run))

    return runs_to_precess_for_catalogue
