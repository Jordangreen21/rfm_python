FLOW_INPUTS = ["transactions_dataset"]
FLOW_INPUTS_EDITABLES = ["rf_segments_identication"]
FLOW_INPUTS_FOR_DYNAMIC_DATA_INGESTION = ["transactions_dataset"]

COLUMN_FOR_RECENCY_COMPUTATION = "days_since_last_transaction"  # Could be "days_between_first_and_last_transaction" depending on the way we want to define the recency

COLUMNS_FOR_ARRAYS_AVERAGE_COMPUTATION = {
    "basket_total_amount_concat": "average_basket",
    "purchased_items_concat": "average_purchased_items",
}

COLUMNS_FOR_ARRAYS_SUM_COMPUTATION = {
    "basket_total_amount_concat": "total_basket",
    "purchased_items_concat": "total_purchased_items",
}

BUILD_RFM_SCENARIOS = [
    "PREPROCESS_TRANSACTIONS",
    "PREPROCESS_DATA_FOR_RFM_COMPUTATION",
    "COMPUTE_RFM_SEGMENTS",
]
BUILD_RFM_PROPAGATION_SCENARIOS = [
    "PREPROCESS_DATA_FOR_RFM_PROPAGATION",
    "PROPAGATE_RFM_SEGMENTS",
    "EXTRACT_INFORMATION_FROM_RFM_PROPAGATION",
]
BUILD_ALL_FLOW_SCENARIOS = BUILD_RFM_SCENARIOS + BUILD_RFM_PROPAGATION_SCENARIOS

FLOW_REFRESH_SCENARIO_ID = "REFRESH_FLOW_OVER_TIME"

TIME_TRIGGER_FREQUENCY_TO_UNITS = {
    "Monthly": "months",
    "Weekly": "weeks",
    "Daily": "days",
    "Hourly": "hours",
}

LOWER_OUTLIERS_QUANTILE_TRESHOLD = 0
HIGHER_OUTLIERS_QUANTILE_TRESHOLD = 0.99


FLOW_ZONES_RFM_PROPAGATION_SHARED_DATASETS = {
    "rfm_propagation_preprocessing": ["transactions_prepared"],
    "rfm_propagation": [
        "customer_rfm_segments",
        "propagation_customer_purchasing_actions",
        "rf_segments_identication_synced",
    ],
    "webapp_zone": ["last_customer_rfm_segments"],
}

FLOW_ZONES_RFM_PROPAGATION_DATASETS = {
    "rfm_propagation_preprocessing": [
        "transactions_for_rfm_propagation",
        "propagation_months",
        "propagation_customer_baskets",
        "customer_first_and_last_transactions",
        "propagation_distinct_customers",
        "propagation_customer_monthly_baskets",
        "propagation_possible_customer_montly_interactions",
        "propagation_customer_montly_interactions",
        "propagation_customer_purchasing_actions"
    ],
    "rfm_propagation": [
        "propagation_customer_rfm_scores",
        "propagation_customer_rfm_segments"
    ],
    "rfm_propagation_last_dates": [
        "last_customer_rfm_segments",
        "inactive_customers",
    ],
    "rfm_propagation_transitions": [
        "all_customer_rfm_transitions",
        "all_customer_rfm_transitions_prepared",
        "segment_label_transitions",
        "recency_transitions",
        "frequency_transitions",
        "monetary_value_transitions",
        "density_transitions",
        "segment_label_transitions_active_periods",
        "recency_transitions_active_periods",
        "frequency_transitions_active_periods",
        "monetary_value_transitions_active_periods",
        "density_transitions_active_periods"
    ],
    "rfm_propagation_scores": ["rfm_score_over_time",
                               "rfm_score_over_time_windows",
                               "rfm_score_over_time_prepared"
                              ],
}

FLOW_ZONES_RFM_PROPAGATION = [
    "rfm_propagation_preprocessing",
    "rfm_propagation",
    "rfm_propagation_transitions",
    "rfm_propagation_last_dates",
    "rfm_propagation_scores",
]
FLOW_ZONES_RFM_PROPAGATION_COLORS = {
    "rfm_propagation_preprocessing": "#8C2DA7",
    "rfm_propagation": "#F9BE40",
    "rfm_propagation_transitions": "#F9BE40",
    "rfm_propagation_last_dates": "#F9BE40",
    "rfm_propagation_scores": "#F9BE40",
}

FALLBACK_CONNECTIONS = {
    "customer_rfm_segments": [
        "compute_customer_rfm_segments_analysis",
        "compute_customer_rfm_segments_labels_analysis",
        "compute_customer_rfm_segments_scores_analysis",
        "compute_density_analysis",
        "compute_frequency_analysis",
        "compute_monetary_value_analysis",
        "compute_recency_analysis"
    ], 
    "propagation_months": [
        "compute_propagation_possible_customer_montly_interactions",
    ],    
    "rf_segments_identication_synced": [
        "compute_customer_rfm_segments",
        "compute_propagation_customer_rfm_segments",
    ]
}

FALLBACK_DATASETS = list(FALLBACK_CONNECTIONS.keys())