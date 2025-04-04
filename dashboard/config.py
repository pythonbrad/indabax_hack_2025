import pathlib
import os

BASE_DIR = pathlib.Path(__file__).parent

USER_MANUAL_FILE = BASE_DIR / "USER-MANUAL.md"
RAW_DATASET_FILE = BASE_DIR / "data/raw/dataset.xlsx"
PREPROCESSED_DATASET_FILE = BASE_DIR / "data/preprocessed/dataset.xlsx"
RAW_GEO_DATASET_FILE = BASE_DIR / "data/geo/cmr_admbnda_adm3_inc_20180104.shp"
PREPROCESSED_GEO_DATASET_FILE = (
    BASE_DIR / "data/preprocessed/cmr_admbnda_adm3_inc_20180104.json"
)

ELIGIBILITY_PREDICTION_API = os.getenv("ELIGIBILITY_PREDICTION_API")
