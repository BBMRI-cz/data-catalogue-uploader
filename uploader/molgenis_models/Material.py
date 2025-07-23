import os
import uuid
from uploader.molgenis_models.MolgenisObject import MolgenisObject
from molgenis_emx2_pyclient import Client


class Material(MolgenisObject):

    TYPE = "fair-genomes_Material"

    def __init__(self, wsi_path, patient_dict, sample_dict):
        sample = patient_dict["samples"][0]
        self.MaterialIdentifier = sample["sample_ID"]
        self.CollectedFromPerson = patient_dict["ID"]
        self.BelongsToDiagnosis = f"mmci_clinical_{uuid.UUID(int=int(sample['biopsy_number'].replace('/', '').replace('-', '')))}"
        self.SamplingTimestamp = sample["cut_time"] if sample["material"].lower() == "tissue" else sample["taking_date"]
        self.RegistrationTimestamp = sample["freeze_time"] if sample["material"].lower() == "tissue" else sample["taking_date"]
        self.BiospecimenType = sample_dict.bioSpeciType
        self.PathologicalState = sample_dict.pathoState
        self.StorageConditions = sample_dict.storCond
        self.PercentageTumourCells = "NotAvailable (NA, nullflavor)"
        self.PhysicalLocation = "MMCI Bank of Biological Material"
        self.wholeslideimagesavailability = self._look_for_wsi(wsi_path, sample["biopsy_number"])
        self.radiotherapyimagesavailability = False

    def add_to_catalog_if_not_exist(self, session):
        analysis_ids = [val["MaterialIdentifier"] for val in session.get(self.TYPE)]
        if self.MaterialIdentifier not in analysis_ids:
            self._add_to_catalog(session)

    def _add_to_catalog(self, session):
        data_dict = self.serialize
        session.add_all(self.TYPE, [data_dict])

    def upsert_to_catalog(self, client: Client):
        data = self.serialize
        temp = [data]
        print(type(temp))           # Should be <class 'list'>
        print(len(temp))            # Should be 1
        print(type(temp[0]))        # Should be <class 'dict'>
        print(temp[0].keys())
        print(client.save_schema("material", data=temp))

    def _look_for_wsi(self, wsi_path, biopsy_number):
        wsi_folder, biopsy_start = self._make_path_from_biopsy_number(biopsy_number)

        if os.path.exists(os.path.join(wsi_path, wsi_folder)) and os.path.isdir(os.path.join(wsi_path, wsi_folder)):
            return any(str(folder).startswith(biopsy_start) for folder in os.listdir(os.path.join(wsi_path, wsi_folder)))
        return False

    def _make_path_from_biopsy_number(self, biopsy_number):
        year = biopsy_number.split("/")[0]
        remaining = biopsy_number.split("/")[1].split("-")[0].zfill(5)
        fixed_biopsy = f"{year}_{remaining}-{biopsy_number.split('/')[1].split('-')[1].zfill(2)}"

        return os.path.join(year, remaining[:2], remaining[2:]), fixed_biopsy
