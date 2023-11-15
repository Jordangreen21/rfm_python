from rfm_segmentation.config.flow.constants import FLOW_INPUTS, FALLBACK_CONNECTIONS, FALLBACK_DATASETS
from dku_utils.connections.connection_commons import FlowConnectionsHandler
from dku_utils.core import get_current_project_and_variables
from dku_utils.datasets.dataset_commons import get_dataset_in_connection_settings

project, variables = get_current_project_and_variables()

main_connection_name = variables["standard"]["main_connection_app"]

main_connection_settings = get_dataset_in_connection_settings(
    project, main_connection_name
)
main_connection_type = main_connection_settings["type"]
managed_dataset_format = variables["standard"]["managed_dataset_format_app"]

if main_connection_type in ["Redshift", "Synapse", "BigQuery"]:
    fallback_connection_name = variables["standard"]["fallback_connection_app"]
    fallback_connection_datasets_downstream_recipes = FALLBACK_CONNECTIONS
    fallback_connection_datasets = FALLBACK_DATASETS
else:
    fallback_connection_name = None
    fallback_connection_datasets_downstream_recipes = None
    fallback_connection_datasets = None

folder_connection_name = variables["standard"]["folder_connection_name_app"]

datasets_to_tables_or_paths_mapping = {}
list_of_datasets_to_load = FLOW_INPUTS
for dataset_name in list_of_datasets_to_load:
    variable_containing_dataset_table_name = "{}_table_name_app".format(dataset_name)
    dataset_table_name = variables["standard"][variable_containing_dataset_table_name]
    datasets_to_tables_or_paths_mapping[dataset_name] = dataset_table_name

FLOW_INPUTS = ["transactions_dataset", "rf_segments_identication"]


flow_connection_handler = FlowConnectionsHandler(
    project=project,
    main_connection_name=main_connection_name,
    fallback_connection_name=fallback_connection_name,
    input_datasets=list_of_datasets_to_load,
    input_datasets_to_preserve=[],
    fallback_connection_datasets=fallback_connection_datasets,
    fallback_connection_datasets_downstream_recipes=fallback_connection_datasets_downstream_recipes,
    input_folders=["cluster_model"],
    bool_change_computed_folders_connections=True,
    folders_connection_name=folder_connection_name,
    project_folders_to_preserve=[],
)
flow_connection_handler.switch_flow_datasets_connections(
    managed_datasets_write_file_format=managed_dataset_format
)
flow_connection_handler.switch_input_datasets_to_not_managed_sate()
flow_connection_handler.switch_flow_folders_connections()

flow_connection_handler.connect_flow_input_datasets(datasets_to_tables_or_paths_mapping)

if main_connection_type in ["Redshift", "Synapse", "BigQuery"]:
    flow_connection_handler.adapt_flow_to_fast_path()

if variables["local"]["not_connected_flag"]:
    variables["local"]["not_connected_flag"] = False
    project.set_variables(variables)
