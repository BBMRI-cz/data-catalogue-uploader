from uploader.molgenis_models.MolgenisObject import MolgenisObject


class Personal(MolgenisObject):

    TYPE = "fair-genomes_Personal"

    def __init__(self, patient_dict):
        self.PersonalIdentifier = patient_dict["ID"]
        self.GenderIdentity = "Not asked (NASK, nullflavor)"
        self.GenderAtBirth = self._convert_gender_at_birth(patient_dict["sex"])
        self.GenotypicSex = self._convert_genotypic_sex(patient_dict["sex"])
        self.CountryOfResidence = "Czechia"
        self.Ancestry = ["Not asked (NASK, nullflavor)"]
        self.CountryOfBirth = "Czechia"
        self.YearOfBirth = patient_dict["birth"].split("/")[1]
        self.InclusionStatus = "Not available (NAVU, nullflavor)"
        self.PrimaryAffiliatedInstitute = "Masaryk Memorial Cancer Institute"
        self.ResourcesInOtherInstitutes = ["Not available (NAVU, nullflavor)"]

    def add_to_catalog_if_not_exist(self, session):
        analysis_ids = [val["PersonalIdentifier"] for val in session.get(self.TYPE)]
        if self.PersonalIdentifier not in analysis_ids:
            self._add_to_catalog(session)

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
