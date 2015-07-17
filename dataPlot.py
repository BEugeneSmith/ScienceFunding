from bokeh.plotting import show,output_notebook,ColumnDataSource,figure
from bokeh.models import HoverTool
from bokeh.charts import Bar
output_notebook()


class dataPrep():

    def __init__(self,table,df):
        self.states = table.keys()
        self.stateCount = table.values()
        self.stateList = sorted(df.columns.tolist())

    def colorChooser(self,c):
        # selects colors to use for heatmap
        colors = [
                "#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce",
                "#ddb7b1", "#cc7878", "#933b41", "#550b1d", "#ffffff"
                ]

        if c == 0.0:
            return colors[0]
        elif c <= 0.005:
            return colors[1]
        elif c <= 0.01:
            return colors[2]
        elif c <= 0.025:
            return colors[3]
        elif c <= 0.05:
            return colors[4]
        elif c <= 0.1:
            return colors[5]
        elif c <= 0.25:
            return colors[6]
        elif c <= 0.5:
            return colors[7]
        elif c <= 0.75:
            return colors[8]
        elif c >= 1:
            return colors[9]


class dataPlots(dataPrep):

    def __init__(self,table,df,mx):
        dataPrep.__init__(self,table,df)
        self.matrix = df.sort_index()
        self.maxVal = mx

    def stateBarPlot(self):
        # plots the number of awards for each contiguous state
        stateBarPlot = Bar(self.stateCount,cat=self.states,tools='',
            title="Number of Awards per State",
           xlabel='States',ylabel='Awards per State',
           width=1000)

        show(stateBarPlot)

    def __heatmapPrep(self):
        # prepares data for use in heatmap

        plotVals = []
        plotClrs = []
        plotKwds = []
        plotStes = []

        for i in range(len(self.matrix)):
            for j in self.stateList:
                val = self.matrix.ix[i,j]
                plotClrs.append(self.colorChooser(val))
                plotVals.append(int(val*self.maxVal))
                plotKwds.append(i)
                plotStes.append(self.stateList.index(j))
        return {
            'Vals':plotVals,
            'Clrs':plotClrs,
            'Kwds':plotKwds,
            'Stes':plotStes,
            }


    def heatmap(self):
        # plots heatmap of term counts
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

        heatmap = figure(width=800,height=400,tools=[hover],outline_line_color=None)
        heatmap.rect('states','keywords', 1,1, source=source,
            x_range=self.stateList, y_range=(self.matrix.index.tolist())[::-1],
            color='colors', line_color=None,
            title="Keywords by state",tools=[hover],
            grid_line_color=None,axis_line_color = None,major_tick_line_color = None
            )
        show(heatmap)
