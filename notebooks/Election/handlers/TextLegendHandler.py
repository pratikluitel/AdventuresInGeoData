from matplotlib.legend_handler import HandlerBase
from matplotlib.text import Text


class TextHandler(HandlerBase):
    def create_artists(
        self, legend, text, xdescent, ydescent, width, height, fontsize, trans
    ):
        tx = Text(
            width / 2.0,
            height / 2,
            text,
            fontsize=fontsize,
            ha="center",
            va="center",
            fontweight="bold",
        )
        return [tx]
