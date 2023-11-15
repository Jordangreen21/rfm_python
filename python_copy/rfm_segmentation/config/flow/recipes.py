RECIPES_PARAMS = {
    # transactions_preprocessing
    "compute_transactions_prepared":{
        "name":"compute_transactions_prepared",
        "flow_zone": "transactions_preprocessing",
        "params":{
            "steps_indexes":{
                "date_column_copy": 0,
                "date_column_renaming": 1,
                "date_parsing": 2, 
                "other_columns_renamings": 4,
                "total_price_computation": 5
            }
        } 
    }
}