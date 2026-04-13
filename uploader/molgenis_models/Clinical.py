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
        birth_dt = self._parse_datetime_to_formats(birth)
        if sample["material"].lower() == "tissue":
            freeze_dt = self._parse_datetime_to_formats(sample["freeze_time"])
            return relativedelta.relativedelta(freeze_dt, birth_dt).years
        else:
            taking_dt = self._parse_datetime_to_formats(sample["taking_date"])
            return relativedelta.relativedelta(taking_dt, birth_dt).years


    def _parse_datetime_to_formats(self, s: str) -> datetime:

        FORMATS = [
            "%Y-%m-%dT%H:%M:%S",     # 2024-01-09T09:27:00
            "%d/%m/%Y, %H:%M:%S",    # 17/05/2024, 00:00:00
            "%Y-%m-%d",   # 1944-02-01
            "%d/%m/%Y",   # 01/02/1944

        ]
        for fmt in FORMATS:
            try:
                return datetime.strptime(s, fmt)
            except ValueError:
                continue

        raise ValueError(f"Unsupported datetime format: {s}")

    def _adjust_birth_format(self, birth):
        if birth.startswith("--"):
            month, year = birth.replace("--", "").split("/")
            return f"{year}-{month}-1"
        return birth

    def _adjust_diagnosis(self, diagnosis):
        if len(diagnosis) == 4:
            return diagnosis[:3] + "." + diagnosis[3]
        return diagnosis
