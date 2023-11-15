from dku_utils.core import get_current_project_and_variables
from dku_utils.scenarios.scenario_commons import switch_scenario_triggers_state, switch_scenario_auto_trigger_state
from rfm_segmentation.config.flow.constants import FLOW_REFRESH_SCENARIO_ID
from rfm_segmentation.config.flow.checks import check_automation_prerequisites

project, variables = get_current_project_and_variables()
check_automation_prerequisites()
switch_scenario_triggers_state(project, FLOW_REFRESH_SCENARIO_ID, [True])
switch_scenario_auto_trigger_state(project, FLOW_REFRESH_SCENARIO_ID, True)