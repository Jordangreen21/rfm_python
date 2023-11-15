import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from collections import Counter

from rfm_segmentation.custom_charts import (
    min_max_scale_values,
    from_scaled_values_to_hex_colors,
    create_plotly_boxplot_trace,
    create_plotly_boxplot_layout,
    create_plotly_boxplot_figure,
    PLOTLY_AXES_FONT_SIZE,
    PLOTLY_AXES_LABEL_COLOR,
    PLOTLY_Y_AXIS_GRID_COLOR,
    PLOTLY_PLOT_BACKGROUND_COLOR,
    PLOTLY_PLOT_BORDERS_COLOR,
    PLOTLY_FIGURE_HEIGHT,
    PLOTLY_FIGURE_WIDTH,
)


def load_rfm_parameters(
    column_for_recency_computation, recency_policy, monetary_value_policy
):
    rfm_original_columns = load_rfm_original_columns(
        column_for_recency_computation, monetary_value_policy
    )
    original_columns_to_rfm_labels_mapping = load_mapping_between_original_and_rfm_columns(
        column_for_recency_computation, monetary_value_policy
    )
    reverse_scores_in_rfm_columns = load_score_reversing_strategy(
        rfm_original_columns, column_for_recency_computation, recency_policy
    )
    rfm_columns = [
        original_columns_to_rfm_labels_mapping[original_column]
        for original_column in rfm_original_columns
    ]
    return (
        rfm_original_columns,
        reverse_scores_in_rfm_columns,
        original_columns_to_rfm_labels_mapping,
        rfm_columns,
    )


def load_rfm_original_columns(column_for_recency_computation, monetary_value_policy):
    if monetary_value_policy == "monetary_value_is_the_baskets_sum":
        rfm_original_columns = [
            column_for_recency_computation,
            "number_of_transactions",
            "total_basket",
            "total_purchased_items",
        ]
    else:
        rfm_original_columns = [
            column_for_recency_computation,
            "number_of_transactions",
            "average_basket",
            "average_purchased_items",
        ]
    return rfm_original_columns


def load_score_reversing_strategy(
    rfm_original_columns, column_for_recency_computation, recency_policy
):
    reverse_scores_in_rfm_columns = {
        column_for_recency_computation: True,
        "number_of_transactions": False,
        "total_basket": False,
        "average_basket": False,
        "total_purchased_items": False,
        "average_purchased_items": False,
    }

    if recency_policy != "oldest_customers_must_have_a_lower_recency":
        reverse_scores_in_rfm_columns[column_for_recency_computation] = False

    reverse_scores_in_rfm_columns = {
        key: reverse_scores_in_rfm_columns[key] for key in rfm_original_columns
    }

    return reverse_scores_in_rfm_columns


def load_mapping_between_original_and_rfm_columns(
    column_for_recency_computation, monetary_value_policy
):
    if monetary_value_policy == "monetary_value_is_the_baskets_sum":
        original_columns_to_rfm_labels_mapping = {
            column_for_recency_computation: "recency",
            "number_of_transactions": "frequency",
            "total_basket": "monetary_value",
            "total_purchased_items": "density",
        }
    else:
        original_columns_to_rfm_labels_mapping = {
            column_for_recency_computation: "recency",
            "number_of_transactions": "frequency",
            "average_basket": "monetary_value",
            "average_purchased_items": "density",
        }
    return original_columns_to_rfm_labels_mapping


def compute_segmentation_quantiles_boundaries(n_segments):
    print("Starting the computation of the quantiles boundaries ...")
    quantiles_width = 1 / n_segments
    segmentation_quantiles_boundaries = []

    for segment_id in range(n_segments):
        if segment_id == 0:
            segmentation_quantiles_boundaries.append(quantiles_width)
        else:
            segmentation_quantiles_boundaries.append(
                quantiles_width + segment_id * quantiles_width
            )
    print(
        "Computed segmentation quantiles : {}".format(segmentation_quantiles_boundaries)
    )
    return segmentation_quantiles_boundaries


def from_value_to_quantile_score(value, list_of_quantiles, quantiles_scores):
    last_quantile_score = quantiles_scores[-1]
    for quantile, quantile_score in zip(list_of_quantiles, quantiles_scores):
        if value <= quantile:
            value_quantile_score = quantile_score
            break
    try:
        return value_quantile_score
    except NameError:
        return last_quantile_score

    
def score_rfm_with_quantiles(
    axes_labels,
    axes_data,
    axes_quantiles,
    n_segments_per_axis,
    reverse_axes_resulting_scores,
):
    rfm_scores = [id_ for id_ in range(1, n_segments_per_axis + 1)]

    axes_rfm_scoring = {}
    for axis_label in axes_labels:
        axis_scores = rfm_scores.copy()
        reverse_axis_possible_scores = reverse_axes_resulting_scores[axis_label]

        if reverse_axis_possible_scores:
            axis_scores = [(n_segments_per_axis + 1) - score for score in axis_scores]

        axis_quantiles = axes_quantiles[axis_label]
        axis_data = axes_data[axis_label]
        axes_rfm_scoring[axis_label] = [
            from_value_to_quantile_score(value, axis_quantiles, axis_scores)
            for value in axis_data
        ]
    return axes_rfm_scoring


def order_predicted_clusters_by_column_values(column_values, cluster_labels, ascending):
    df_data = pd.DataFrame(
        {"column_value": column_values, "cluster_label": cluster_labels},
        index=range(len(column_values)),
    )
    df_agg = df_data.groupby("cluster_label")["column_value"].mean().reset_index()
    df_agg = df_agg.sort_values(by="column_value", ascending=ascending).reset_index(
        drop=True
    )

    df_agg["new_cluster_label"] = df_agg.index + 1
    cluster_labels_mapping = {
        old_label: new_label
        for old_label, new_label in zip(
            df_agg["cluster_label"], df_agg["new_cluster_label"]
        )
    }

    ordered_predicted_clusters = [
        cluster_labels_mapping[old_cluster_label]
        for old_cluster_label in cluster_labels
    ]
    return ordered_predicted_clusters


"""def train_kmeans_models_for_rfm(axes_labels, axes_data, n_segments_per_axis):
    axes_kmeans_clustering_model = {}

    for axis_label in axes_labels:
        axis_data = axes_data[axis_label]
        axis_data = [np.log(1 + value) for value in axis_data]
        axis_data_counts = Counter(axis_data)
        axis_data_unique_values = list(axis_data_counts.keys())
        axis_data_unique_values_weights = np.array(
            [axis_data_counts[value] for value in axis_data_unique_values]
        )
        print(
            "Applying Kmeans clustering (n_clusters={}) on axis '{}'".format(
                n_segments_per_axis, axis_label
            )
        )
        k_means_clustering_model = KMeans(n_clusters=n_segments_per_axis)
        k_means_data = np.array(axis_data_unique_values).reshape(-1, 1)
        k_means_clustering_model.fit(
            k_means_data, sample_weight=axis_data_unique_values_weights
        )
        axes_kmeans_clustering_model[axis_label] = k_means_clustering_model

    return axes_kmeans_clustering_model"""

def train_kmeans_models_for_rfm(axes_labels, axes_data, n_segments_per_axis):
    axes_kmeans_clustering_model = {}

    for axis_label in axes_labels:
        axis_data = axes_data[axis_label]
        axis_data = [np.log(1 + value) for value in axis_data]
        
        k_means_clustering_model = KMeans(n_clusters=n_segments_per_axis)
        k_means_data = np.array(axis_data).reshape(-1, 1)
        k_means_clustering_model.fit(
            k_means_data
        )
        axes_kmeans_clustering_model[axis_label] = k_means_clustering_model

    return axes_kmeans_clustering_model


def score_rfm_with_k_means(
    axes_labels, axes_data, axes_kmeans_clustering_model, reverse_axes_resulting_scores
):
    axes_kmeans_scoring = {}

    for axis_label in axes_labels:
        axis_data = axes_data[axis_label]
        axis_data = [np.log(1 + value) for value in axis_data]
        k_means_data = np.array(axis_data).reshape(-1, 1)
        k_means_clustering_model = axes_kmeans_clustering_model[axis_label]
        cluster_predictions = k_means_clustering_model.predict(k_means_data)
        cluster_predictions = [cluster_id + 1 for cluster_id in cluster_predictions]

        reverse_axis_possible_scores = reverse_axes_resulting_scores[axis_label]

        if reverse_axis_possible_scores:
            reorder_cluster_by_ascending_data_values = False
        else:
            reorder_cluster_by_ascending_data_values = True
        cluster_predictions = order_predicted_clusters_by_column_values(
            axis_data, cluster_predictions, reorder_cluster_by_ascending_data_values
        )

        axes_kmeans_scoring[axis_label] = cluster_predictions

    return axes_kmeans_scoring


def enrich_dataframe_with_rfm_global_scores_and_segments(
    rfm_dataframe, n_segments_per_axis, rfm_columns, columns_prefix
):
    rfm_score_column = "{}_score".format(columns_prefix)
    rfm_score_scaled_column = "{}_score_scaled".format(columns_prefix)
    rfm_segment_column = "{}_segment".format(columns_prefix)
    n_rfm_columns = len(rfm_columns)
    rfm_dataframe[rfm_score_column] = rfm_dataframe[rfm_columns].sum(axis=1)
    rfm_dataframe[rfm_score_scaled_column] = rfm_dataframe[rfm_score_column] / (
        n_rfm_columns * n_segments_per_axis
    )

    rfm_segments_data = list(rfm_dataframe[rfm_columns].apply(tuple, axis=1))
    rfm_segments = []

    for segment_data in rfm_segments_data:
        rfm_segment = "_".join(str(score) for score in segment_data)
        rfm_segments.append(rfm_segment)

    rfm_dataframe[rfm_segment_column] = rfm_segments

    return rfm_dataframe


def remove_dataframe_outliers_based_on_quantiles(
    dataframe, lower_quantile_threshold, higher_quantile_threshold, list_of_columns
):
    original_datafrem_length = len(dataframe)
    for column in list_of_columns:
        column_data = list(dataframe[column])
        lower_quantile = np.quantile(column_data, q=lower_quantile_threshold)
        higher_quantile = np.quantile(column_data, q=higher_quantile_threshold)
        dataframe = dataframe[
            (dataframe[column] >= lower_quantile)
            & (dataframe[column] <= higher_quantile)
        ]
    final_datafrem_length = len(dataframe)
    print(
        "After outliers removal, {}% ({}/{}) of the dataset initial rows remains".format(
            float(final_datafrem_length) / original_datafrem_length,
            final_datafrem_length,
            original_datafrem_length,
        )
    )
    return dataframe


def generate_rfm_box_plots(
    rfm_original_columns,
    original_columns_to_rfm_labels_mapping,
    final_rfm_dataframe,
    n_segments_per_axis,
):
    rfm_box_plots = {}
    rfm_scores = list(range(1, n_segments_per_axis + 1))
    rfm_scores.append(
        n_segments_per_axis + 1
    )  # We add a value to the RFM scores to make the higher score color more visible
    rfm_scores_scaled = min_max_scale_values(rfm_scores, False)
    COLORMAP_ID = "magma"
    rfm_scores_colors = from_scaled_values_to_hex_colors(
        rfm_scores_scaled, COLORMAP_ID, False
    )
    # rfm_scores_colors.reverse()
    scores_to_colors = {
        score: color for score, color in zip(rfm_scores, rfm_scores_colors)
    }

    for column in rfm_original_columns:
        rfm_axis_label = original_columns_to_rfm_labels_mapping[column]
        rfm_axis_color = "{}_color".format(rfm_axis_label)
        rfm_scores_labels = {
            score: "{} {}".format(rfm_axis_label, score) for score in rfm_scores
        }
        rfm_axis_scores_data = {}

        for rfm_score in rfm_scores:
            rfm_axis_scores_data[rfm_score] = list(
                final_rfm_dataframe[column][
                    final_rfm_dataframe[rfm_axis_label] == rfm_score
                ]
            )
            pass

        boxplot_data = [
            create_plotly_boxplot_trace(
                rfm_axis_scores_data[rfm_score],
                scores_to_colors[rfm_score],
                rfm_scores_labels[rfm_score],
            )
            for rfm_score in rfm_scores
        ]
        boxplot_layout = create_plotly_boxplot_layout(
            rfm_axis_label,
            PLOTLY_AXES_LABEL_COLOR,
            PLOTLY_AXES_FONT_SIZE,
            column,
            PLOTLY_AXES_LABEL_COLOR,
            PLOTLY_AXES_FONT_SIZE,
            PLOTLY_Y_AXIS_GRID_COLOR,
            PLOTLY_PLOT_BACKGROUND_COLOR,
            PLOTLY_PLOT_BORDERS_COLOR,
            PLOTLY_FIGURE_HEIGHT,
            PLOTLY_FIGURE_WIDTH,
        )
        figure = create_plotly_boxplot_figure(boxplot_data, boxplot_layout)
        rfm_box_plots["{}_box_plot".format(rfm_axis_label)] = figure
    return rfm_box_plots