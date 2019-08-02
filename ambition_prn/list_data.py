from ambition_prn.constants import CRYTOCOCCAL_MENINGITIS
from edc_constants.constants import OTHER, MALIGNANCY, TUBERCULOSIS, UNKNOWN
from edc_list_data import PreloadData


list_data = {
    "edc_adverse_event.causeofdeath": [
        (CRYTOCOCCAL_MENINGITIS, "Cryptococcal meningitis"),
        (
            "Cryptococcal_meningitis_relapse_IRIS",
            "Cryptococcal meningitis relapse/IRIS",
        ),
        (TUBERCULOSIS, "TB"),
        ("bacteraemia", "Bacteraemia"),
        ("bacterial_pneumonia", "Bacterial pneumonia"),
        (MALIGNANCY, "Malignancy"),
        ("art_toxicity", "ART toxicity"),
        ("IRIS_non_CM", "IRIS non-CM"),
        ("diarrhea_wasting", "Diarrhea/wasting"),
        (UNKNOWN, "Unknown"),
        (OTHER, "Other"),
    ]
}

preload_data = PreloadData(list_data=list_data, model_data={}, unique_field_data=None)
