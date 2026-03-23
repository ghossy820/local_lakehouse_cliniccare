import os
from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets, DbtProject

DBT_PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../dbt_clinic"))

my_dbt_project = DbtProject(project_dir=DBT_PROJECT_PATH)
my_dbt_project.prepare_if_dev()

@dbt_assets(manifest=my_dbt_project.manifest_path)
def clinic_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    """Asset: Đại diện cho toàn bộ các models trong dbt (Staging & Marts)."""
    yield from dbt.cli(["build"], context=context).stream()