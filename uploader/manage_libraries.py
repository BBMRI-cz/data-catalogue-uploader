import pandas as pd
import os

from uploader.logging_config.logging_config import LoggingConfig


class LibrariesManager:

    sample_sheet_to_panel = {
        "SeqCapH": "HyperCap",
        "EG": "EliGene",
        "TSO500": "TruSight"
        }

    def __init__(self, libraries_path, run_path):
        all_files = [os.path.join(libraries_path, file) for file in os.listdir(libraries_path)
                     if not os.path.isdir(file) and file.endswith(".csv")]
        latest_file = max(all_files, key=os.path.getmtime)
        self.run_path = run_path
        self.libraries_path = latest_file
        self.sample_sheet_path = os.path.join(run_path, "SampleSheet.csv")

    def get_data_from_libraries(self, predictive_number):
        logger = LoggingConfig.get_logger()
        parameters_path = self._get_parameteres_path(predictive_number)

        df = pd.read_csv(self.libraries_path, delimiter=";", encoding="CP1250")
        df.dropna(inplace=True, subset=["Panel"])
        df.replace(to_replace="NEPRAVDA", value=False, inplace=True)
        df.replace(to_replace="PRAVDA", value=True, inplace=True)
        df["Panel"] = df["Panel"].str.lower()
        df["Text in parameters"] = df["Text in parameters"].str.lower()

        # Try {pseudo}_Parameters.txt file
        if os.path.exists(parameters_path):
            possible_params = df["Text in parameters"].tolist()
            library_name = self._look_for_lib_in_parameters(possible_params, parameters_path)

            if library_name:
                match = df[
                    df["Text in parameters"].apply(lambda x: x in library_name.lower())
                ]
                if not match.empty:
                    return self._extract_library_info_from_row(match.iloc[0])
        else:
            logger.info(f"Parameters file does not exist for predictive number: {predictive_number}")

        # No library name in the parameters file, so we need to extract data from run_path
        run_folder_name = os.path.basename(self.run_path)
        experiment_date_str = run_folder_name[:6]
        reference_date = self._fix_reference_date(experiment_date_str)

        if "_N" in run_folder_name:
            return self._get_nextseq_library(df, reference_date)
        elif "_M" in run_folder_name:
            return self._get_miseq_library(df, reference_date)
        else:
            logger.warning(f"Unknown run type for run folder: {run_folder_name}")
            return None

    def _get_miseq_library(self, df, reference_date):
        # Extract experiment name from sample sheet
        samplesheet_df = pd.read_csv(
            self.sample_sheet_path, delimiter=",",
            names=["[Header]", "Unnamed: 1", "Unnamed: 2", "Unnamed: 3", "Unnamed: 4",
                   "Unnamed: 5", "Unnamed: 6", "Unnamed: 7", "Unnamed: 8", "Unnamed: 9"]
        )

        experiment_row = samplesheet_df[samplesheet_df["[Header]"] == "Experiment Name"]
        if experiment_row.empty:
            return None

        experiment = experiment_row["Unnamed: 1"].values[0]
        
        experiment_name = experiment.split("_")[0]

        if experiment_name in self.sample_sheet_to_panel:
            experiment_name = self.sample_sheet_to_panel[experiment_name]

        experiment_name = experiment_name.lower()

        base_match = df[
            df["Panel"].str.contains(experiment_name) &
            df["Availability Date Range"].apply(
                lambda x: self._date_in_date_range(x, reference_date)
            )
        ]

        if base_match.empty:
            return None
        if len(base_match) == 1:
            return self._extract_library_info_from_row(base_match.iloc[0])

        manual_match = df[
            df["Panel"].str.contains(experiment_name) &
            (df["Text in parameters"] == "manual")
        ]
        if not manual_match.empty:
            row = manual_match.iloc[0]
        else:
            # fallback if no manual row exists
            row = base_match.iloc[0]
        return self._extract_library_info_from_row(row)

    def _get_nextseq_library(self, df, reference_date):
        no_param_rows = df[df["Text in parameters"] == "no_parameters"]

        match = no_param_rows[
            no_param_rows["Availability Date Range"].apply(
                lambda x: self._date_in_date_range(x, reference_date)
            )
        ]

        if match.empty:
            return None

        row = match.iloc[0] # pick the first row
        return self._extract_library_info_from_row(row)


    def _get_parameteres_path(self, predictive_number):
        analysis_part = os.path.join(self.run_path, "Samples", predictive_number, "Analysis")
        if os.path.exists(os.path.join(analysis_part, "Reports", f"{predictive_number}_Parameters.txt")):
            return os.path.join(analysis_part, "Reports", f"{predictive_number}_Parameters.txt")
        else:
            return os.path.join(analysis_part, f"{predictive_number}_Parameters.txt")

    def _look_for_lib_in_parameters(self, possible_parameters, parameters_path):
        with open(parameters_path, "r") as f:
            text = f.readlines()
        for parameter in possible_parameters:
            if parameter in text[-1].lower():
                return parameter
        return None
        
    def _fix_reference_date(self, date):
        year, month, day = date[:2], date[2:4], date[4:]
        return f"20{year}-{month}-{day}"

    def _date_in_date_range(self, dates, reference_date):
        if isinstance(dates, str) and "-" in dates:
            start, end = dates.split("-")
            start = pd.to_datetime(start, dayfirst=True)
            end = pd.to_datetime(end, dayfirst=True)
            return pd.to_datetime(reference_date) in pd.date_range(start, end)
        else:
            return False

    def _extract_library_info_from_row(self, row):
        return {
            "library_prep_kit": row["code in the molgenis catalogue"].split(":")[0],
            "pca_free": row["PCR Free"],
            "target_enrichment_kid": row["Target Enrichment Kit"],
            "umi_present": row["UMIs Present"],
            "genes": row["Genes (*all coding regions covered)"]
        }
