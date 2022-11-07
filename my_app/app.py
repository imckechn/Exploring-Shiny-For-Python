# Normally in Python, you would use urllib.request.urlopen() to fetch data from a web
# API. However, it won't work in Pyodide because sockets are not available.
#
# Instead, you can pyodide.http.pyfetch(), which is a wrapper for the JavaScript fetch()
# function. Note that when running shinylive, the endpoint MUST use https. This is
# because shinylive must be served over https (unless you are running on localhost),
# and browsers will not allow a https page to fetch data with http.
#
# One important difference between urllib.request.urlopen() and pyodide.http.pyfetch()
# is that the latter is asynchronous. In a Shiny app, this just means that the
# reactive.Calc's and outputs must have `async` in front of the function definitions,
# and when they're called, they must have `await` in front of them.
#
# If you want to write code that works in both regular Python and Pyodide, see the
# download.py file for a wrapper function that can be used to make requests in both
# regular Python and Pyodide. (Note that the function isn't actually used in this app.)

from pprint import pformat
import requests
import pandas as pd
from shiny import App, reactive, render, ui

app_ui = ui.page_fluid(
    ui.output_text_verbatim("info"),
)


def server(input, output, session):
    # Weather data API: https://github.com/robertoduessmann/weather-api
    @reactive.Calc
    def url():
        return f"http://gbadske.org:9000/GBADsLivestockPopulation/faostat?year=2017&country=Canada&species=*&format=file"

    @reactive.Calc
    async def animal_data():

        #response = requests.get(url())
        #print(type(response))

        #data = response.text
        data = pd.read_csv(url())

        return data

    @output
    @render.plot(alt="A histogram")
    def plot():
        np.random.seed(19680801)
        x = 100 + 15 * np.random.randn(437)
        plt.hist(x, input.n(), density=True)

    @output
    @render.text
    async def info():
        data = await animal_data()
        if isinstance(data, (str, bytes)):
            data_str = data
        else:
            data_str = pformat(data)
        return f"Request URL: {url()}\nResult type: {type(data)}\n{data_str}"


app = App(app_ui, server)
