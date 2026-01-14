import molgenis.client
import json
import os
from molgenis_emx2_pyclient import Client


from uploader.logging_config.logging_config import LoggingConfig
from uploader.molgenis_models.Analysis import Analysis
from uploader.molgenis_models.Clinical import Clinical
from uploader.molgenis_models.IndividualConsent import IndividualConsent
from uploader.molgenis_models.Material import Material
from uploader.molgenis_models.MolgenisObject import MolgenisObject
from uploader.molgenis_models.Personal import Personal
from uploader.molgenis_models.SamplePreparation import SamplePreparation
from uploader.molgenis_models.Sequencing import Sequencing


class MetadataImport:

    FAIR_PERSONAL = "fair-genomes_Personal"
    FAIR_CLINICAL = "fair-genomes_Clinical"
    FAIR_MATERIAL = "fair-genomes_Material"
    FAIR_SAMPLE_PREP = "fair-genomes_SamplePreparation"
    FAIR_SEQUENCING = "fair-genomes_Sequencing"
    FAIR_ANALYSIS = "fair-genomes_Analysis"
    FAIR_INDI_CONSENT = "fair-genomes_IndividualConsent"

    def __init__(self, wsi_path, libraries_path):
        login = os.getenv("CATALOG_LOGIN")
        password = os.getenv("CATALOG_PASSWORD")
        token = os.getenv("MOLGENIS_TOKEN")
        url = os.getenv("MOLGENIS_URL")

        self.client = Client(url, schema="FairGenomes", token=token)

        self.wsi_path = wsi_path
        self.libraries_path = libraries_path

    def upload(self, run_metadata, sample_metadata, clinical_info_path, run_type, libraries_data=None):
        logger = LoggingConfig.get_logger()

        with open(clinical_info_path) as clinical_file:
            clinical_metadata = json.load(clinical_file)

        upload_sequence: list[MolgenisObject] = [
            Personal(clinical_metadata),
            IndividualConsent(clinical_metadata),
            Clinical(clinical_metadata),
            Material(self.wsi_path, clinical_metadata, sample_metadata),
            SamplePreparation(run_metadata, clinical_metadata, libraries_data),
            Sequencing(clinical_metadata, sample_metadata, run_metadata),
        ] # order  of the objects is important

        if run_type == "MiSEQ":
            upload_sequence.append(Analysis(clinical_metadata))


        for molgenis_object in upload_sequence:
            logger.info(json.dumps(molgenis_object.serialize, indent=2))
            # molgenis_object.add_to_catalog_if_not_exist(self.session)
            molgenis_object.upsert_to_catalog(self.client)
