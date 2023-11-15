from dku_utils.core import get_current_project_and_variables
from dku_utils.datasets.dataset_commons import get_dataset_in_connection_settings
from dku_utils.recipes.recipe_commons import update_recipe_ouput_schema


def optional_build(recipe_name, dataset_name):
    project, variables = get_current_project_and_variables()

    main_connection_name = variables["standard"]["main_connection_name_app"]

    main_connection_settings = get_dataset_in_connection_settings(project, main_connection_name)
    main_connection_type = main_connection_settings["type"]
    if main_connection_type in ["Redshift", "Synapse", "BigQuery"]:
        update_recipe_ouput_schema(project, recipe_name)
        project.get_dataset(dataset_name).build()
