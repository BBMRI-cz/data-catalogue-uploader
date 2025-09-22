import uuid

from molgenis_emx2_pyclient import Client

from uploader.logging_config.logging_config import LoggingConfig
from uploader.molgenis_models.MolgenisObject import MolgenisObject
from datetime import datetime
from dateutil import relativedelta


class Clinical(MolgenisObject):


    TYPE = "fair-genomes_Clinical"

    def __init__(self, patient_dict):
        sample = patient_dict["samples"][0]
        self.ClinicalIdentifier = f"mmci_clinical_{uuid.UUID(int=int(sample['biopsy_number'].replace('/', '').replace('-', '')))}"
        self.BelongsToPerson = patient_dict["ID"]
        self.Phenotype = '"NoInformation (NI, nullflavor)"'
        self.UnobservedPhenotype = '"NoInformation (NI, nullflavor)"'
        self.ClinicalDiagnosis = self._adjust_diagnosis(sample["diagnosis"]) if sample["material"] != "genome" else None
        self.MolecularDiagnosisGene = '"NoInformation (NI, nullflavor)"'
        self.AgeAtDiagnosis = self._calculate_age_at_diagnosis(patient_dict["birth"], sample)
        self.AgeAtLastScreening = self._calculate_age_at_diagnosis(patient_dict["birth"], sample)
        self.Medication = '"NoInformation (NI, nullflavor)"'
        self.MedicalHistory = '"NoInformation (NI, nullflavor)"'

    def add_to_catalog_if_not_exist(self, session):
        analysis_ids = [val["ClinicalIdentifier"] for val in session.get(self.TYPE)]
        if self.ClinicalIdentifier not in analysis_ids:
            self._add_to_catalog(session)

    def upsert_to_catalog(self, client: Client):
        logger = LoggingConfig.get_logger()
        data = self.serialize
        logger.info(client.save_schema("clinical", data=[data]))

    def _add_to_catalog(self, session):
        data_dict = self.serialize
        session.add_all(self.TYPE, [data_dict])

    def _calculate_age_at_diagnosis(self, birth, sample):
        datetime_format = "%Y-%m-%d"
        birth = self._adjust_birth_format(birth)
        if sample["material"].lower() == "tissue":
            return relativedelta.relativedelta(datetime.strptime(sample["freeze_time"],
                                                                 f"{datetime_format}T%H:%M:%S"),
                                datetime.strptime(birth, datetime_format)).years
        else:
            return relativedelta.relativedelta(datetime.strptime(sample["taking_date"], datetime_format),
                                               datetime.strptime(birth, datetime_format)).years

    def _adjust_birth_format(self, birth):
        if birth.startswith("--"):
            month, year = birth.replace("--", "").split("/")
            return f"{year}-{month}-1"
        return birth

    def _adjust_diagnosis(self, diagnosis):
        if len(diagnosis) == 4:
            return diagnosis[:3] + "." + diagnosis[3]
        return diagnosis
