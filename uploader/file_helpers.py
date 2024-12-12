import os
import re

def get_all_runs_with_data_for_catalogue(organised_folder: str, wanted_run_type: str="MiSEQ") -> [str]:
    runs_to_precess_for_catalogue = []
    years = [year for year in os.listdir(organised_folder) if re.match(r'^[\d]{4}$', year)]
    for year in years:
        for run_type in [run_type for run_type in os.listdir(os.path.join(organised_folder, year)) if run_type == wanted_run_type]:
            if run_type == "MiSEQ":
                multiple_runs_path = os.path.join(organised_folder, year, run_type, "complete-runs")
            else:
                multiple_runs_path = os.path.join(organised_folder, year, run_type)
            for run in os.listdir(multiple_runs_path):
                run_catalog_info = os.path.join(multiple_runs_path, run, "catalog_info_per_pred_number")
                already_uploaded = os.path.join(multiple_runs_path, run, ".uploaded")
                if os.path.exists(run_catalog_info) and os.listdir(run_catalog_info) and not already_uploaded:
                    runs_to_precess_for_catalogue.append(os.path.join(multiple_runs_path, run))

    return runs_to_precess_for_catalogue
