from shiny import App, render, ui
import pandas as pd

# Import modules for plot rendering
import numpy as np
import matplotlib.pyplot as plt

app_ui = ui.page_fluid(
    ui.h3("Animal Populations in Canada"),
    ui.output_plot("plot"),
    ui.output_table("table"),
)


def server(input, output, session):

    def importCattleData():
        df = pd.read_csv('http://gbadske.org:9000/GBADsLivestockPopulation/faostat?year=2017&country=Canada&species=*&format=file')
        print(df.keys)
        return df

    @output
    @render.table
    def table():
        df = importCattleData()
        file = open('cattleData.txt', 'w')
        file.write(df.to_csv(index=False))
        file.close()
        return df


    @output
    @render.plot(alt="A histogram")
    def plot():
        df = importCattleData()

        np.random.seed(1)
        x = 100 + 15 * np.random.randn(437)
        #plt.hist(x, input.n(), density=True)
        #plt.bar(df.loc[:,"species"], df.loc[:,"population"])
        plt.barh(df.loc[:,"species"], df.loc[:,"population"])


app = App(app_ui, server, debug=True)
