from typing import Callable, Tuple
import matplotlib.pyplot as plt


def offset(coord: Tuple, xoff: float = 0, yoff: float = 0) -> Tuple:
    return (coord[0] + xoff, coord[1] + yoff)


def transform_nepal(polygon_center_coords: Tuple, district: str) -> Tuple:
    """
    STATIC TRANSFORMATION LOGIC - TO DELETE AFTER DYNAMIC LOGIC IS IMPLEMENTED
    """
    coords = polygon_center_coords
    if district in (
        "SINDHULI",
        "KAILALI",
        "DAILEKH",
        "SALYAN",
        "KASKI",
        "TANAHUN",
        "MANANG",
        "SIRAHA",
        "ILAM",
        "LAMJUNG",
        "BARDIYA",
        "BANKE",
        "DANG",
        "KAPILBASTU",
        "ROLPA",
        "MUSTANG",
        "SARLAHI",
    ):
        coords = offset(coords, yoff=-0.04)
    elif district in (
        "DARCHULA",
        "KAVRE",
        "JHAPA",
        "BHOJPUR",
        "DADELDHURA",
        "SAPTARI",
        "BAJURA",
        "JAJARKOT",
        "RUKUM",
        "MUGU",
        "GULMI",
        "PYUTHAN",
        "PALPA",
        "NAWALPARASI",
        "SAPTARI",
    ):
        coords = offset(coords, yoff=-0.05)
    elif district in ("NUWAKOT", "DOLAKHA", "TAPLEJUNG"):
        coords = offset(coords, yoff=-0.08)
    elif district in ("SURKHET", "KALIKOT", "SINDHUPALCHOK"):
        coords = offset(coords, yoff=-0.1)
    elif district in ("BHAKTAPUR"):
        coords = offset(coords, yoff=-0.01)
    elif district in ("KANCHANPUR", "MAKWANPUR"):
        coords = offset(coords, xoff=-0.03)
    elif district in ("PARBAT", "ARGHAKHANCHI"):
        coords = offset(coords, xoff=0.04)
    elif district in ("SOLUKHUMBU"):
        coords = offset(coords, yoff=-0.1, xoff=0.03)
    elif district in ("KHOTANG", "JUMLA", "BAITADI", "RASUWA", "MYAGDI"):
        coords = offset(coords, xoff=-0.02, yoff=-0.05)
    elif district in ("BAGLUNG"):
        coords = offset(coords, xoff=-0.1, yoff=-0.02)
    elif district in ("UDAYAPUR"):
        coords = offset(coords, xoff=-0.12, yoff=0.01)
    elif district in ("DHADING"):
        coords = offset(coords, yoff=-0.14, xoff=-0.08)
    elif district in ("RAMECHHAP"):
        coords = offset(coords, yoff=-0.14, xoff=-0.09)
    elif district in ("SYANGJA"):
        coords = offset(coords, xoff=0.02, yoff=-0.06)
    elif district in ("BAJHANG", "GORKHA", "CHITWAN"):
        coords = offset(coords, xoff=0.04, yoff=-0.05)
    elif district in ("RUPANDEHI"):
        coords = offset(coords, xoff=0.03, yoff=-0.04)
    elif district in ("OKHALDHUNGA"):
        coords = offset(coords, xoff=0.02, yoff=-0.09)

    return coords


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

    annotation_field, annotation_value_field, threshold = (
        kwarg_dict["annotation_field"],
        kwarg_dict["annotation_value_field"],
        kwarg_dict["threshold"],
    )

    small_polygon_map = kwarg_dict["small_polygon_map"]

    try:
        color, highlight_color = kwarg_dict["color"], kwarg_dict["highlight_color"]
    except KeyError:
        color, highlight_color = "black", "white"

    def annotate_polygon(x):
        """
        Someday, this will be fully dynamic,
        handle all form of text and line intersections,
        and work for all forms of polygon combinations,
        not just maps.

        Someday.
        """
        small_polygons_map = small_polygon_map.copy()

        # need these for dynamic text size and other stuff
        apparant_width = plt.gcf().get_size_inches()[0] * ax.figure.dpi
        width = 1200 if apparant_width <= 1200 else apparant_width

        fontsize = (
            width / 192
            if x[annotation_field] in small_polygons_map.keys()
            else width / 236
        )

        # Generate labels from A-Z if small districts are encountered
        if x[annotation_field] in small_polygons_map.keys():
            text = small_polygons_map[x[annotation_field]]
        else:
            text = f"{x[annotation_field].title()}\n{x[annotation_value_field]}"

        applied_color = (
            highlight_color if x[annotation_value_field] > threshold else color
        )

        polygon = x.geometry
        polygon_center_coords = polygon.centroid.coords[0]

        ################################## DYNAMIC TRANSFORMATION LOGIC ##################################################################
        # # The width of the rectangle bounding polygon
        # min_bounding_rect_width = abs(polygon.envelope.exterior.coords.xy[0][1] - polygon.envelope.exterior.coords.xy[0][0])
        # annotation_text = ax.text(polygon.centroid.coords[0][0], polygon.centroid.coords[0][1],text,fontsize=9)
        # # The width of the annotation text
        # annotation_text_width = annotation_text.get_window_extent(renderer=ax.figure.canvas.get_renderer()).width
        # del ax.texts[-1]
        # # Currently, the above two widths are not in the same coordinate system, need to fix it before comparing
        # # logic to be used:
        # # - if annotation width> polygon width, shift the text to an appropriate area outside the map bounds and draw a annotation line
        ##################################################################################################################################

        ################# STATIC TRANSFORMATION LOGIC - TO DELETE AFTER DYNAMIC LOGIC IS IMPLEMENTED #####################################

        transformed_center = transform_nepal(polygon_center_coords, x[annotation_field])

        ##################################################################################################################################

        # To fix while adjusting for projections
        # polygon_center_coords = transform.transform_point(transformed_center[0], transformed_center[1], gcrs.ccrs.PlateCarree())

        return ax.annotate(
            text=text,
            xy=transformed_center,
            color=applied_color,
            ha="center",
            fontsize=fontsize,
            weight="bold",
        )

    return annotate_polygon


def transform_to_capitalized_case(string: str, separator: str) -> str:
    """
    Returns a "Capitalized Case" output value from a
     input value where words are in a separator-separated-case

    Args:
        string (str): input value, where words are separated by the separator
        separator (str): separator

    Returns:
        str: Regular Case output value
    """
    split_string = string.split(separator)
    op_string = ""
    for idx, substr in enumerate(split_string):
        op_string += ("" if idx == 0 else " ") + substr.capitalize()

    return op_string
