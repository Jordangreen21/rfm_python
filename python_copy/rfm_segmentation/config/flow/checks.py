

def check_automation_prerequisites(project, variables):
    global_variables = variables["standard"]
    rfm_dates_filtering_strategy = global_variables["rfm_dates_filtering_strategy_app"] # choices in ["keep_dates_in_a_range_before_a_past_date", "keep_dates_in_a_range_before_today"]
    enable_flow_automation = global_variables["enable_flow_automation_app"]
    update_reference_period_rfm_scoring = global_variables["update_reference_period_rfm_scoring_app"]
    update_the_rfm_propagation_start_date = global_variables["update_the_rfm_propagation_start_date_app"]
    
    if not enable_flow_automation:
        log_message = \
        "Error : Flow automation disablled."\
        "Flow refresh over time can only work if you activate the option 'Enable flow automation ?' "\
        "in the 'Automation strategy settings'. "
        raise Exception(log_message)
        pass
    
    else:
        not_any_period_asked_for_refresh = (update_reference_period_rfm_scoring==False) and (update_the_rfm_propagation_start_date==False)
        if not_any_period_asked_for_refresh:
            log_message = \
            "Error : Not any period asked for refresh."\
            "Flow refresh over time can only work if at least one of the two options 'Refresh the reference period data ?' "\
            "or 'Refresh the larger period data ?' is activated in the 'Automation strategy settings'."
            raise Exception(log_message)
            pass
    pass