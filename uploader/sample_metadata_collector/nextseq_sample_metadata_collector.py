import os.path

from .miseq_sample_metadata_collector import CollectMiseqSampleMetadata


class CollectNextSeqSampleMetadata(CollectMiseqSampleMetadata):


    def collect(self):
        sample_id = os.path.basename(self.sample_path)
        self._find_sample_metadata(sample_id)
        self.sample_info.avReadDepth = None
        self.sample_info.obsReadLength = None
        return self.sample_info

    def _find_sample_metadata(self, sample_id):
        self._find_data_in_clinical_info(self.clinical_data_path, sample_id)

