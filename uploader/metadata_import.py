import molgenis.client
import json

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

    def __init__(self, wsi_path, libraries_path, login, password):
        self.session = molgenis.client.Session("https://data.bbmri.cz/api/")
        self.session.login(login, password)

        self.wsi_path = wsi_path
        self.libraries_path = libraries_path

    def upload(self, run_metadata, sample_metadata, clinical_info_path, run_type, libraries_data=None):
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
            print(json.dumps(molgenis_object.serialize, indent=2))
            molgenis_object.add_to_catalog_if_not_exist(self.session)

    def __del__(self):
        self.session.logout()