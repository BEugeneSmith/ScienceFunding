from bokeh.plotting import show,output_notebook,ColumnDataSource,figure
from bokeh.models import HoverTool
from bokeh.charts import Bar
output_notebook()


class dataPrep():

    def __init__(self,table,df):
        self.states = table.keys()
        self.stateCount = table.values()
        self.stateList = df.columns.tolist()

    def colorChooser(self,c):
        colors = [
                "#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce",
                "#ddb7b1", "#cc7878", "#933b41", "#550b1d", "#ffffff"
                ]

        c = int(c)
        if c == 0:
            return colors[0]
        elif c in range(1,6):
            return colors[1]
        elif c in range(6,11):
            return colors[2]
        elif c in range(11,25):
            return colors[3]
        elif c in range(25,50):
            return colors[4]
        elif c in range(50,100):
            return colors[5]
        elif c in range(100, 250):
            return colors[6]
        elif c in range(250,500):
            return colors[7]
        elif c in range(500,1000):
            return colors[8]
        elif c >= 1000:
            return colors[9]


class dataPlots(dataPrep):

    def __init__(self,table,df):
        dataPrep.__init__(self,table,df)
        self.matrix = df

    def stateBarPlot(self):
        stateBarPlot = Bar(self.stateCount,cat=self.states,tools='',
            title="Number of Awards per State",
           xlabel='States',ylabel='Awards per State',
           width=1000)

        show(stateBarPlot)

    def __heatmapPrep(self):
        plotVals = []
        plotClrs = []
        plotKwds = []
        plotStes = []

        for i in range(len(self.matrix.index.tolist())): #odd line
            for j in self.stateList:
                plotVals.append(self.matrix.ix[i,j])
                val = self.matrix.ix[i,j]
                plotClrs.append(self.colorChooser(val))
                plotKwds.append(i)
                plotStes.append(self.stateList.index(j))
        return {
            'Vals':plotVals,
            'Clrs':plotClrs,
            'Kwds':plotKwds,
            'Stes':plotStes,
            }


    def heatmap(self):
        plotData = self.__heatmapPrep()
        source = ColumnDataSource(
        data=dict(
            states=plotData['Stes'],
            keywords=plotData['Kwds'],
            colors=plotData['Clrs'],
            values=plotData['Vals'],
            hStates=map(lambda x: self.stateList[x],plotData['Stes']),
            hKwords=map(lambda x: self.matrix.index.tolist()[x],plotData['Kwds'])
            )
        )

        hover = HoverTool(
            tooltips = [
                ("awards","@values"),
                ("state,term","@hStates,@hKwords")
            ]
        )

        p1 = figure(width=800,height=400,tools=[hover],outline_line_color=None)
        p1.rect('states','keywords', 1,1, source=source,
            x_range=self.stateList, y_range=(self.matrix.index.tolist())[::-1],
            color='colors', line_color=None,
            title="Keywords by state",tools=[hover],
            grid_line_color=None,axis_line_color = None,major_tick_line_color = None
            )
        show(p1)
