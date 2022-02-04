from typing import Callable
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

def offset(coord, xoff=0, yoff=0):
    return (coord[0]+xoff, coord[1]+yoff)

def transform_nepal(polygon_center_coords, district):
    """
    STATIC TRANSFORMATION LOGIC - TO DELETE AFTER DYNAMIC LOGIC IS IMPLEMENTED
    """
    coords = polygon_center_coords
    if district in ('DARCHULA','KAVRE','JHAPA','BHOJPUR',
                    'SAPTARI','BAJURA','RASUWA','JAJARKOT','RUKUM','MUGU',
                    'GULMI','PYUTHAN','PALPA','NAWALPARASI','CHITWAN'):
        coords = offset(coords, yoff=-0.05)
    elif district in ('SINDHULI'):
        coords = offset(coords, yoff=-0.04)
    elif district in ('KHOTANG'):
        coords = offset(coords, xoff=-0.02, yoff=-0.05)
    elif district in ('SYANGJA'):
        coords = offset(coords, xoff=0.02,yoff=-0.06)
    elif district in ('DADELDHURA','BAJHANG','GORKHA'):
        coords = offset(coords, xoff=0.04, yoff=-0.01)
    elif district in ('KANCHANPUR', 'MAKWANPUR'):
        coords = offset(coords, xoff=-0.03)
    elif district in ('SURKHET', 'KALIKOT','NUWAKOT','SINDHUPALCHOK','SOLUKHUMBU'):
        coords = offset(coords, yoff=-0.1)
    elif district in ('DHADING', 'RAMECHHAP'):
        coords = offset(coords, yoff=-0.14, xoff=-0.08)
    elif district in ('BAGLUNG','MYAGDI'):
        coords = offset(coords, xoff=-0.1, yoff=-0.02)
    elif district in ('UDAYAPUR'):
        coords = offset(coords, xoff=-0.12)
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
    annotation_field, annotation_value_field = kwarg_dict['annotation_field'] , kwarg_dict['annotation_value_field']
    threshold = kwarg_dict['threshold']
    try:
        color, highlight_color = kwarg_dict['color'], kwarg_dict['highlight_color']
    except KeyError:
        color, highlight_color = 'black','white'

    def annotate_polygon(x):
        """
        Someday, this will be fully dynamic, 
        handle all form of text and line intersections,
        and work for all forms of polygon combinations, 
        not just maps.

        Someday.
        """

        text = f'{x[annotation_field]}\n{x[annotation_value_field]}'
        polygon = x.geometry

        polygon_center_coords = polygon.centroid.coords[0]
        applied_color = highlight_color if x[annotation_value_field] > threshold else color
        
        # # The width of the rectangle bounding polygon
        # min_bounding_rect_width = abs(polygon.envelope.exterior.coords.xy[0][1] - polygon.envelope.exterior.coords.xy[0][0])
        # annotation_text = ax.text(polygon.centroid.coords[0][0], polygon.centroid.coords[0][1],text,fontsize=9)
        # # The width of the annotation text
        # annotation_text_width = annotation_text.get_window_extent(renderer=ax.figure.canvas.get_renderer()).width
        # del ax.texts[-1]
        # # Currently, the above two widths are not in the same coordinate system, need to fix it before comparing
        # # logic to be used:
        # # - if annotation width> polygon width, shift the text to an appropriate area outside the map bounds and draw a annotation line

        ################# STATIC TRANSFORMATION LOGIC - TO DELETE AFTER DYNAMIC LOGIC IS IMPLEMENTED ###################

        # line needed for: 
        polygon_center_coords = transform_nepal(polygon_center_coords, x[annotation_field])
        if x[annotation_field] in ('ARGHAKHANCHI', 'PARBAT', 'KATHMANDU', 'BHAKTAPUR', 'LALITPUR', 'RAUTAHAT', 'MAHOTTARI', 'DHANUSHA', 'OKHALDHUNGA', 'DHANKUTA', 'TEHRATHUM', 'PANCHTHAR'):
            return

        ################################################################################################################

        return ax.annotate(text=text, xy=polygon_center_coords, xytext=polygon_center_coords,
            color=applied_color, ha='center', fontsize=8,weight='bold')
    return annotate_polygon