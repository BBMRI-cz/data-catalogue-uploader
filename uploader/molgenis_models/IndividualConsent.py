from uploader.molgenis_models.MolgenisObject import MolgenisObject
from molgenis_emx2_pyclient import Client

class IndividualConsent(MolgenisObject):

    TYPE = "fair-genomes_IndividualConsent"
    
    def __init__(self, patient_dict):
        sample = patient_dict["samples"][0]
        self.IndividualConsentIdentifier = patient_dict["ID"].replace("patient", "consent")
        self.PersonConsenting = patient_dict["ID"]
        #self.ConsentFormUsed = "mmci_consentform_1"
        #self.CollectedBy = "Masaryk Memorial Cancer Institute"
        self.SigningDate = sample["freeze_time"] if sample["material"].lower() == "tissue" else sample["taking_date"]
        self.RepresentedBy = "patient"
        self.DataUsePermissions = "general research use"

    def add_to_catalog_if_not_exist(self, session):
        analysis_ids = [val["IndividualConsentIdentifier"] for val in session.get(self.TYPE)]
        if self.IndividualConsentIdentifier not in analysis_ids:
            self._add_to_catalog(session)

    def upsert_to_catalog(self, client: Client):
        data = self.serialize
        temp = [data]
        print(type(temp))           # Should be <class 'list'>
        print(len(temp))            # Should be 1
        print(type(temp[0]))        # Should be <class 'dict'>
        print(temp[0].keys())
        print(client.save_schema("individualconsent", data=temp))

    def _add_to_catalog(self, session):
        data_dict = self.serialize
        session.add_all(self.TYPE, [data_dict])
