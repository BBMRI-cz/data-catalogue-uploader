import pytest
from uploader.manage_libraries import LibrariesManager
import os
import shutil

TEST_LIBRARY_FOLDER = os.path.join(os.path.dirname(__file__), "test_libraries")
TEST_DESTINATION_RUN = os.path.join(os.path.dirname(__file__), "test_destination_for_copy", "2020", "MiSEQ", "complete-runs",
                                    "2020_M00000_0000_00000000-00000")
SPECIAL_SAMPLE_SHEET = os.path.join(os.path.dirname(__file__), "SpecialSampleSheet.csv")


def _move_back_sample_sheets():
    shutil.move(os.path.join(TEST_DESTINATION_RUN, "SampleSheet.csv"), SPECIAL_SAMPLE_SHEET)
    shutil.move(os.path.join(os.path.dirname(__file__), "OriginalSampleSheet.csv"),
                os.path.join(TEST_DESTINATION_RUN, "SampleSheet.csv"))


@pytest.fixture()
def use_different_sample_sheet(request):
    shutil.move(os.path.join(TEST_DESTINATION_RUN, "SampleSheet.csv"),
                os.path.join(os.path.dirname(__file__), "OriginalSampleSheet.csv"))
    shutil.move(SPECIAL_SAMPLE_SHEET, os.path.join(TEST_DESTINATION_RUN, "SampleSheet.csv"))

    request.addfinalizer(_move_back_sample_sheets)


def test_correct_library_file_selected():
    manager = LibrariesManager(TEST_LIBRARY_FOLDER, 
                               TEST_DESTINATION_RUN) 

    assert manager.libraries_path == os.path.join(TEST_LIBRARY_FOLDER, "LibrariesV240126.csv")


def test_correct_data_extracted_from_library_with_panel_in_parameters():
    manager = LibrariesManager(TEST_LIBRARY_FOLDER,
                               TEST_DESTINATION_RUN)

    results = manager.get_data_from_libraries("mmci_predictive_00000000-0000-0000-0000-000000000001")

    assert results == {
        "library_prep_kit": "Accel-Amplicon Plus Panel by Swift Biosciences/IDT",
        "pca_free": False,
        "target_enrichment_kid": "Accel Amplicon Custom Core Kit",
        "umi_present": False,
        "genes": "ALK, APC, ARAF, BRAF, CDKN2A, EGFR, ERBB2, ERBB4, FGFR1, FGFR2, FGFR3, KIT," +
                 " KRAS, MAP2K1, MET, NOTCH1, NRAS, PDGFRA, PIK3CA, PTEN, STK11, TP53*"
    }


def test_correct_data_extracted_from_library_with_manual_panel():
    manager = LibrariesManager(TEST_LIBRARY_FOLDER,
                               TEST_DESTINATION_RUN)



    results = manager.get_data_from_libraries("mmci_predictive_00000000-0000-0000-0000-000000000002")

    assert results == {'genes': 'AKT1,ALK,APC,ARAF,BRAF,BRCA1*,BRCA2*,CDKN2A,EGFR,ERBB2,ERBB4,FGFR1,FGFR2,FGFR3,' +
                                'KIT,KRAS,MAP2K1,MET,NOTCH1,NRAS,PDGFRA,PIK3CA,POLE,PTEN,STK11,TP53*',
                       'library_prep_kit': 'Accel-Amplicon Plus Panel by Swift Biosciences',
                       'pca_free': False,
                       'target_enrichment_kid': 'Accel Amplicon Custom Core Kit',
                       'umi_present': False}


def test_correct_data_extraction_from_library_with_panel_based_on_date(use_different_sample_sheet):
    manager = LibrariesManager(TEST_LIBRARY_FOLDER,
                               TEST_DESTINATION_RUN)

    results = manager.get_data_from_libraries("mmci_predictive_00000000-0000-0000-0000-000000000002")

    assert results == {'genes': 'AKT1, ALK, APC, AR, ARAF, BAP1, BRAF, BRCA1*, BRCA2*, CDH1, CDKN2A, '
                                'CTNNB1, EGFR, ERBB2*, ESR1*, FBXW7, FGFR2, FGFR3, FOXL2, GNA11, '
                                'GNAQ, GNAS, HRAS, CHEK2, IDH1, KDR, KIT, KRAS*, MAP2K1, MAP2K4, '
                                'MET, MLH1, MTOR, NF1, NOTCH1, NRAS*, PDGFRA, PIK3CA*, POLE, PTEN, '
                                'RB1, RET, SMAD4, SMO, SRC, STK11, TP53*',
                                'library_prep_kit': 'KAPA HyperPlus Kits by Roche',
                                'pca_free': True,
                                'target_enrichment_kid': 'KAPA HyperChoice',
                                'umi_present': False}
