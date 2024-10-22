import uuid
from uploader.molgenis_models.MolgenisObject import MolgenisObject
from datetime import datetime


class Clinical(MolgenisObject):

    TYPE = "fair-genomes_Clinical"

    def __init__(self, patient_dict):
        sample = patient_dict["samples"][0]
        self.ClinicalIdentifier = f"mmci_clinical_{uuid.UUID(int=int(sample['biopsy_number'].replace('/', '').replace('-', '')))}"
        self.BelongsToPerson = patient_dict["ID"]
        self.Phenotype = ["NoInformation (NI, nullflavor)"]
        self.UnobservedPhenotype = ["NoInformation (NI, nullflavor)"]
        self.ClinicalDiagnosis = self._adjust_diagnosis(sample["diagnosis"]) if sample["material"] != "genome" else None
        self.MolecularDiagnosisGene = ["NoInformation (NI, nullflavor)"]
        self.AgeAtDiagnosis = self._calculate_age_at_diagnosis(patient_dict["birth"], sample)
        self.AgeAtLastScreening = self._calculate_age_at_diagnosis(patient_dict["birth"], sample)
        self.Medication = ["NoInformation (NI, nullflavor)"]
        self.MedicalHistory = ["NoInformation (NI, nullflavor)"]

    def add_to_catalog_if_not_exist(self, session):
        analysis_ids = [val["ClinicalIdentifier"] for val in session.get(self.TYPE)]
        if self.ClinicalIdentifier not in analysis_ids:
            self._add_to_catalog(session)

    def _add_to_catalog(self, session):
        data_dict = self.serialize
        session.add_all(self.TYPE, [data_dict])

    @staticmethod
    def _calculate_age_at_diagnosis(birth, sample):
        datetime_format = "%d/%m/%Y"
        if sample["material"] == "Tissue":
            return datetime.strptime(sample["freeze_time"],
                                     datetime_format + ", %H:%M:%S") - datetime.strptime(birth, datetime_format)
        else:
            return datetime.strptime(sample["taking_date"], datetime_format) - datetime.strptime(birth, datetime_format)

    @staticmethod
    def _adjust_diagnosis(diagnosis):
        if len(diagnosis) == 4:
            return diagnosis[:3] + "." + diagnosis[3]
        return diagnosis
