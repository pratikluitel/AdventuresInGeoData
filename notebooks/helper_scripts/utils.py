from typing import Callable
import matplotlib.pyplot as plt
import matplotlib.figure as figure

def annotate_polygons(ax: plt.Axes, **kwarg_dict) -> Callable:
    """
    inputs: 
    ax - The axes to plot the annotation
    annotation_field - The text field to use for the annotation
    annotation_value_field - The value field to use for the annotation

    output:
    annotate_polygons - A function that can be used to annotate a polygon

    returns a function that generates an annotation
    for a polygon on the given axes
    """
    annotation_field, annotation_value_field = kwarg_dict['annotation_field'] , kwarg_dict['annotation_value_field']
    threshold = kwarg_dict['threshold']
    try:
        color, highlight_color = kwarg_dict['color'], kwarg_dict['highlight_color']
    except KeyError:
        color, highlight_color = 'black','white'

    def annotate_polygon(x):
        text = x[annotation_field]+f'\n{x[annotation_value_field]}'
        polygon = x.geometry
        print(polygon)
        min_bounding_rect_width = abs(polygon.envelope.exterior.coords.xy[0][1] - polygon.envelope.exterior.coords.xy[0][0])

        annotation_text = ax.text(polygon.centroid.coords[0][0], polygon.centroid.coords[0][1],text,fontsize=9)
        annotation_text_width = annotation_text.get_window_extent(renderer=ax.figure.canvas.get_renderer()).width

        del ax.texts[-1]

        print(min_bounding_rect_width, annotation_text_width)

        polygon_center_coords = polygon.centroid.coords[0]
        applied_color = highlight_color if x[annotation_value_field] > threshold else color
        return ax.annotate(text=text, xy=polygon_center_coords, xytext=polygon_center_coords,
            color=applied_color, ha='center', fontsize=9)
    return annotate_polygon