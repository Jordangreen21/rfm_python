import pandas as pd
import numpy as np


TREEMAP_ROOT_COLOR = "#000000"
MONETARY_VALUE_COLORS = {
    1: "#555555",
    2: "#777777",
    3: "#999999",
    4: "#bbbbbb",
    5: "#dddddd",
}
# {1: "#202020", 2: "#723506", 3: "#B3814E", 4: "#BEAB9E",  5: "#DBDAD5"}


def aggregate_rfm_dataframes_by_segments(rfm_dataframe):
    rfm_dataframe["count"] = 1
    result = (
        rfm_dataframe[["segment_label", "segment_color", "count"]]
        .groupby(["segment_label", "segment_color"])
        .sum()
        .reset_index()
    )
    return result


def aggregate_rfm_dataframes_by_monetary_value_and_segment(rfm_dataframe):
    rfm_dataframe["count"] = 1
    result = (
        rfm_dataframe[["monetary_value", "segment_label", "segment_color", "count"]]
        .groupby(["monetary_value", "segment_label", "segment_color"])
        .sum()
        .reset_index()
    )
    return result


def root_treemap_data(
    treemap_root_label,
    treemap_root_color,
    list_of_segment_labels,
    list_of_segment_values,
    list_of_segment_colors,
):
    treemap_labels = [treemap_root_label] + list_of_segment_labels
    treemap_parents = [""] + [
        treemap_root_label for __ in range(len(list_of_segment_labels))
    ]
    treemap_values = [int(np.sum(list_of_segment_values))] + list_of_segment_values
    treemap_values = convert_list_values_to_int(treemap_values)
    treemap_colors = [treemap_root_color] + list_of_segment_colors
    return treemap_labels, treemap_parents, treemap_values, treemap_colors


def convert_list_values_to_int(list_of_numerical_values):
    return [int(value) for value in list_of_numerical_values]


def bold_string_for_html(string):
    return "<b>{}</b>".format(string)


def match_segment_labels_and_values(segment_labels, segment_values):
    return [
        "{} : {}".format(segment_label, segment_value)
        for segment_label, segment_value in zip(segment_labels, segment_values)
    ]
