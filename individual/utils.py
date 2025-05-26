import base64
import logging
from os import path
from typing import Iterable

from individual.apps import IndividualConfig
import pandas as pd

from django.db.models import Q, Value, Func, F

from individual.models import IndividualDataSource

logger = logging.getLogger(__name__)


def load_dataframe(individual_sources: Iterable[IndividualDataSource]) -> pd.DataFrame:
    data_from_source = []
    for individual_source in individual_sources:
        json_ext = individual_source.json_ext
        individual_source.json_ext["id"] = individual_source.id
        data_from_source.append(json_ext)
    recreated_df = pd.DataFrame(data_from_source)

    # Ensure 'location_code' is treated as a string if it exists
    if "location_code" in recreated_df.columns:
        recreated_df["location_code"] = recreated_df["location_code"].astype("string")

    return recreated_df


def fetch_summary_of_broken_items(upload_id):
    return list(IndividualDataSource.objects.filter(
        Q(is_deleted=False) &
        Q(upload_id=upload_id) &
        ~Q(validations__validation_errors=[])
    ).values_list('uuid', flat=True))


def fetch_summary_of_valid_items(upload_id):
    return list(IndividualDataSource.objects.filter(
        Q(is_deleted=False) &
        Q(upload_id=upload_id) &
        Q(validations__validation_errors=[])
    ).values_list('uuid', flat=True))


def _photo_dir(file_dir, file_name):
    root = IndividualConfig.individual_photos_root_path
    return path.join(root, file_dir, file_name)


def load_photo_file(file_dir, file_name):
    photo_path = _photo_dir(file_dir, file_name)
    try:
        with open(photo_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except FileNotFoundError:
        logger.error(f"{photo_path} not found")
