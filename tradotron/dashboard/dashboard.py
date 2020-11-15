import warnings
import logging
from IPython.display import display
import plotly.graph_objects as go
from ipywidgets import widgets
from ..data import data
from ..helper import helper

warnings.filterwarnings(action="ignore", category=DeprecationWarning)
logger = logging.getLogger(__name__)


logger.debug("get inital data")
FinDat = data.FinanceData(ticker_name="MSFT", ticker_period="1mo")
df = FinDat.data
df_column_list = df.columns.to_list()

logger.debug("gset up widgets - row 1")
period = widgets.Dropdown(
    value="1mo",
    options=[
        "1d", "5d", "1mo", "3mo",
        "6mo", "1y", "2y", "5y",
        "10y", "ytd", "max"
    ],
    description='Period:'
)
ticker = widgets.Dropdown(
    value="MSFT",
    options=helper.load_preferences().get("ticker_handles"),
    description="Ticker:"
)
container1 = widgets.HBox(children=[ticker, period])

logger.debug("gset up widgets - row 2")
primary_y = widgets.Dropdown(
    options=df_column_list
)
secondary_y = widgets.Dropdown(
    options=df_column_list
)
container2 = widgets.HBox([primary_y, secondary_y])

logger.debug("gset up widgets - row 3")
add_ticker_name = widgets.Text(
    description="New ticker:"
)
add_ticker_button = widgets.ToggleButton(
    value=False,
    description='Add Ticker',
    disabled=False,
    button_style='success',  # 'success', 'info', 'warning', 'danger' or ''
    tooltip='Description',
    icon='plus'
)
container3 = widgets.HBox([add_ticker_name, add_ticker_button])


# Assign an empty figure widget with two traces
trace0 = go.Scatter(
    x=df.index,
    y=df[primary_y.value],
    opacity=0.75,
    name=primary_y.value,
    line={"dash": "solid"}
)

trace1 = go.Scatter(
    x=df.index,
    y=df[secondary_y.value],
    opacity=0.75,
    name=secondary_y.value,
    line={"dash": "solid"}
)

figure_widget = go.FigureWidget(
    data=[trace0, trace1],
    layout=go.Layout(
        title=dict(
            text=f"Ticker: {ticker.value}"
        ),
        barmode='overlay'
    )
)


def add_handle(change):
    """add ticker handle to preferences.json on button press"""

    # load preferences
    pref_dict = helper.load_preferences()
    ticker_handles = pref_dict.get("ticker_handles")

    if add_ticker_name.value not in ticker_handles:

        # update preferences.json
        ticker_handles.append(add_ticker_name.value)
        pref_dict["ticker_handles"] = ticker_handles
        helper.save_preferences(preference_dict=pref_dict)

        # update widget values
        ticker.options = ticker_handles

        print("Ticker handle saved!")

    else:
        print("Ticker handle already exists!")

    # clear add_ticker_name input
    add_ticker_name.value = ""


def update_figure(change):
    """update plot on change"""

    # get data
    FinDat = data.FinanceData(
        ticker_name=ticker.value,
        ticker_period=period.value
    )

    df = FinDat.data

    with figure_widget.batch_update():
        figure_widget.data[0].x = df.index
        figure_widget.data[1].x = df.index
        figure_widget.data[0].y = df[primary_y.value]
        figure_widget.data[1].y = df[secondary_y.value]
        # following is not being updated
        figure_widget.data[0].name = primary_y.value
        figure_widget.data[1].name = secondary_y.value
        figure_widget.layout.barmode = "overlay"
        figure_widget.layout.title = dict(text=f"Ticker: {ticker.value}")
        figure_widget.layout.xaxis.title = "time"
        figure_widget.layout.yaxis.title = "price"


def run():
    """display the widgets and plot"""

    ticker.observe(update_figure, names="value")
    period.observe(update_figure, names="value")

    primary_y.observe(update_figure, names="value")
    secondary_y.observe(update_figure, names="value")

    add_ticker_button.observe(add_handle, names="value")

    display(
        widgets.VBox([
            container1,
            container2,
            container3,
            figure_widget
        ])
    )
