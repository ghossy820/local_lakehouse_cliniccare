from dagster import Definitions, load_assets_from_modules
from dagster_dbt import DbtCliResource

from .assets import data_generators, raw_ingestion, dbt_assets

all_assets = load_assets_from_modules([data_generators, raw_ingestion, dbt_assets])

defs = Definitions(
    assets=all_assets,
    resources={
        "dbt": DbtCliResource(project_dir=dbt_assets.my_dbt_project),
    },
)