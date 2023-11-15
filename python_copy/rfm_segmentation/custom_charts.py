import plotly.graph_objects as go
from plotly.graph_objs import Layout
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

PLOTLY_AXES_FONT_SIZE = 10
PLOTLY_AXES_LABEL_COLOR = "rgb(0, 0, 0)"
PLOTLY_Y_AXIS_GRID_COLOR = "grey"
PLOTLY_PLOT_BACKGROUND_COLOR = "rgb(255, 255, 255)"
PLOTLY_PLOT_BORDERS_COLOR = "rgb(255, 255, 255)"
PLOTLY_FIGURE_HEIGHT = 400
PLOTLY_FIGURE_WIDTH = 800


def log_transform_for_min_max_scaling(list_or_array):
    list_or_array_min = min(list_or_array)
    list_or_array = [np.log(1 + value - list_or_array_min) for value in list_or_array]
    return list_or_array


def min_max_scale_values(list_or_array, smooth_scaling_with_log):
    if smooth_scaling_with_log:
        list_or_array = log_transform_for_min_max_scaling(list_or_array)
        pass

    list_or_array_min = min(list_or_array)
    list_or_array_max = max(list_or_array)
    return [
        (value - list_or_array_min) / (list_or_array_max - list_or_array_min)
        for value in list_or_array
    ]


def from_scaled_values_to_hex_colors(scaled_values, cmap_id, bool_keep_alpha_in_rgba):
    """
    values : should be scaled 
    cmap_id : look at https://matplotlib.org/stable/gallery/color/colormap_reference.html
    """
    color_mapper = plt.get_cmap(cmap_id)
    rgba_colors = color_mapper(scaled_values, bytes=False)
    hex_colors = [
        matplotlib.colors.to_hex(color, keep_alpha=bool_keep_alpha_in_rgba)
        for color in rgba_colors
    ]
    return hex_colors


def create_plotly_boxplot_trace(y_data, trace_color, trace_name):
    trace = go.Box(y=y_data, marker_color=trace_color, name=trace_name)
    return trace


def create_plotly_boxplot_layout(
    x_axis_label,
    x_axis_label_color,
    x_axis_font_size,
    y_axis_label,
    y_axis_label_color,
    y_axis_font_size,
    y_axis_grid_color,
    plot_background_color,
    plot_borders_color,
    figure_height,
    figure_width,
):
    layout = Layout(
        plot_bgcolor=plot_background_color,
        paper_bgcolor=plot_borders_color,
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            title=x_axis_label,
            titlefont=dict(size=x_axis_font_size, color=x_axis_label_color),
        ),
        yaxis=dict(
            zeroline=False,
            gridcolor=y_axis_grid_color,
            title=y_axis_label,
            titlefont=dict(size=y_axis_font_size, color=y_axis_label_color),
        ),
        height=figure_height,
        width=figure_width,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5),
    )
    return layout


def create_plotly_boxplot_figure(boxplot_data, boxplot_layout):
    figure = go.Figure(data=boxplot_data, layout=boxplot_layout)
    return figure
