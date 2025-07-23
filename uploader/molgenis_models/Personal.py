from uploader.molgenis_models.MolgenisObject import MolgenisObject
from molgenis_emx2_pyclient import Client


class Personal(MolgenisObject):

    TYPE = "fair-genomes_Personal"

    def __init__(self, patient_dict):
        self.PersonalIdentifier = patient_dict["ID"]
        #self.GenderIdentity = "Not asked (NASK, nullflavor)"
        self.GenderAtBirth = self._convert_gender_at_birth(patient_dict["sex"])
        self.GenotypicSex = self._convert_genotypic_sex(patient_dict["sex"])
        self.CountryOfResidence = "Czechia"
        #self.Ancestry = ["Not asked (NASK, nullflavor)"]
        self.CountryOfBirth = "Czechia"
        self.YearOfBirth = patient_dict["birth"].split("/")[1]
        #self.InclusionStatus = "Not available (NAVU, nullflavor)"
        #uself.PrimaryAffiliatedInstitute = "Masaryk Memorial Cancer Institute"
        #self.ResourcesInOtherInstitutes = ["Not available (NAVU, nullflavor)"]

    def add_to_catalog_if_not_exist(self, session):
        analysis_ids = [val["PersonalIdentifier"] for val in session.get(self.TYPE)]
        if self.PersonalIdentifier not in analysis_ids:
            self._add_to_catalog(session)

    def upsert_to_catalog(self, client: Client):
        data = self.serialize
        temp = [data]
        print(type(temp))           # Should be <class 'list'>
        print(len(temp))            # Should be 1
        print(type(temp[0]))        # Should be <class 'dict'>
        print(temp[0].keys())
        print(client.save_schema("personal", data=temp))

    def _add_to_catalog(self, session):
        data_dict = self.serialize
        session.add_all(self.TYPE, [data_dict])

    def _convert_gender_at_birth(self, sex):
        if sex == "male":
            return "assigned male at birth"
        elif sex == "female":
            return "assigned female at birth"
        else:
            return "Asked but unkown (ASKU, nullflavor)"

    def _convert_genotypic_sex(self, sex):
        if sex == "male":
            return "XY Genotype"
        elif sex == "female":
            return "XX Genotype"
        else:
            return "Asked but unkown (ASKU, nullflavor)"
