from bokeh.plotting import show,output_notebook,ColumnDataSource,figure,vplot
from bokeh.models import HoverTool
from bokeh.charts import Bar
from numpy import pi
output_notebook()


class dataPrep():

    def __init__(self,table,df):
        self.states = table.keys()
        self.stateCount = table.values()
        self.stateList = sorted(df.columns.tolist())
        self.df = df

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
        dataPrep.__init__(self,table,df) #what was mx?
        self.matrix = df.sort_index()
        self.maxVal = mx

    def stateBarPlot(self):
        # plots the number of awards for each contiguous state
        stateBarPlot = Bar(self.stateCount,cat=self.states,tools='',
            title="Number of Awards per State",
           xlabel='States',ylabel='Awards per State',
           width=800,height=400)

        show(stateBarPlot)

    def __heatmapPrep(self):
        # prepares data for use in heatmap
        self.states = self.df.columns.tolist()
        self.keywords = self.df.index.tolist()

        # tchange to heatmap plot
        state = []
        kword = []
        color = []
        value = []
        for k in self.keywords:
            for s in self.states:
                state.append(s)
                kword.append(k)
                val = self.df[s][k]
                color.append(self.colorChooser(val))
                value.append(int(val*self.maxVal))

        source = ColumnDataSource(
            data=dict(
                state=state,
                kword=kword,
                color=color,
                value=value,
            )
        )

        return(source)



    def heatmap(self,name):
        # plots heatmap
        source = self.__heatmapPrep()

        hover = HoverTool(
        tooltips = [
            ("state,term","@state,@kword"),
            ("value","@value"),
            ]
        )

        p = figure(
            tools=[hover],
            plot_width=900, plot_height=450,
            # x_axis_location="above",
            x_range=self.states, y_range=list(reversed(self.keywords)),
            title=name
        )

        p.rect('state', 'kword', 1, 1, source=source, color='color', line_color=None)


        p.grid.grid_line_color = None
        p.axis.axis_line_color = None
        p.axis.major_tick_line_color = None
        p.axis.major_label_standoff = 0
        p.legend
        p.xaxis.major_label_orientation = pi/3
        show(p)
