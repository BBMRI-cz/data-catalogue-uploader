import molgenis.client
import json
import os

from uploader.molgenis_models.Analysis import Analysis
from uploader.molgenis_models.Clinical import Clinical
from uploader.molgenis_models.IndividualConsent import IndividualConsent
from uploader.molgenis_models.Material import Material
from uploader.molgenis_models.Personal import Personal
from uploader.molgenis_models.SamplePreparation import SamplePreparation
from uploader.molgenis_models.Sequencing import Sequencing


class MolgenisImporter:

    FAIR_PERSONAL = "fair-genomes_Personal"
    FAIR_CLINICAL = "fair-genomes_Clinical"
    FAIR_MATERIAL = "fair-genomes_Material"
    FAIR_SAMPLE_PREP = "fair-genomes_SamplePreparation"
    FAIR_SEQUENCING = "fair-genomes_Sequencing"
    FAIR_ANALYSIS = "fair-genomes_Analysis"
    FAIR_INDI_CONSENT = "fair-genomes_IndividualConsent"

    def __init__(self, run_path, wsi_path, libraries_path, login, password):
        # self.session = molgenis.client.Session("https://data.bbmri.cz/api/")
        # self.session.login(login, password)
        self.run_path = run_path
        self.catalog_info_folder = os.path.join(run_path, "catalog_info_per_pred_number")
        self.samples_metadata_folder = os.path.join(run_path, "sample_metadata")
        self.wsi_path = wsi_path
        self.libraries_path = libraries_path
        self.sample_sheet_path = os.path.join(run_path, "SampleSheet.csv")
        with open(os.path.join(run_path, "run_metadata.json"), "r") as f:
            self.run_metadata = json.load(f)

    def __call__(self):
        for pred_number in os.listdir(self.catalog_info_folder):
            clinical_info_file = os.path.join(self.catalog_info_folder, pred_number)

            with open(clinical_info_file, "r") as f:
                clinical_info_file = json.load(f)

            sample_metadata_file = os.path.join(self.samples_metadata_folder, pred_number)
            with open(sample_metadata_file, "r") as f:
                sample_metadata_file = json.load(f)

            upload_sequence = [
                Personal(clinical_info_file),
                IndividualConsent(clinical_info_file),
                Clinical(clinical_info_file),
                Material(self.wsi_path, clinical_info_file, sample_metadata_file),
                SamplePreparation(self.run_path, self.libraries_path, self.sample_sheet_path, clinical_info_file),
                Sequencing(clinical_info_file, sample_metadata_file, self.run_metadata),
                Analysis(clinical_info_file)
            ]

            for molgenis_object in upload_sequence:
                print(molgenis_object.serialize)
                # molgenis_object.add_to_catalog_if_not_exists(self.session)

    def __del__(self):
        pass
        # self.session.logout()
