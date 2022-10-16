from math import pi
import pandas as pd

import streamlit as st

from bokeh.layouts import row
from bokeh.plotting import figure
from bokeh.palettes import Greys4, Blues8     #, Category20c
from bokeh.transform import cumsum

pathName = '/Users/thomasnemmers/Documents/GitHub Portfolio/RMDS Project/sample_dashboard_v2/inputs'
fileName = 'Median_Household_Income_(2016).csv'

demo = pd.read_csv(f"{pathName}/{fileName}" , sep = ',' , header = 0)

zips = demo.ZIP.unique()

filter = st.sidebar.selectbox('Select a Zip Code:' , zips)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DATA FOR STACKED BAR CHART OF ELDERLY
demoFiltered = demo[demo['ZIP'] == filter]
avgElderPct = demoFiltered['Elders_Pct'].mean()
data = {'Test' : [''] , 'Elders' : [avgElderPct] , 'Not_Elders' : [100 - avgElderPct]}
categories = ['Elders' , 'Not_Elders']
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# DATA FOR PIE CHART
ethnDict = {
    'White_Pct' : 'White',
    'Black_Pct' : 'Black',
    'Asian_Pct' : 'Asian',
    'Latino_Pct' : 'Latino',
    'Mltpl_Pct' : 'Multiple',
    'NatAm_Pct' : 'Native American',
    'PacIs_Pct' : 'Pacific Islander',
    'Other_Pct' : 'Other'
}

demoPieGraph_df = demoFiltered.iloc[: , 13:21].mean().to_frame(name = 'Percentage')
demoPieGraph_df = demoPieGraph_df.rename(index = ethnDict)
demoPieGraph_df['angle'] = demoPieGraph_df['Percentage'] / 100 * 2 * pi
demoPieGraph_df['color'] = Blues8
demoPieGraph_df['categories'] = list(ethnDict.values())
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TOOLTIPS = [
    ('Elders' , '@Elders{0.00}%') ,
    ('Not Elders' , '@Not_Elders{0.00}%')
]

p1 = figure(title = 'Percent Elderly', plot_height = 350, plot_width = 400 , tooltips = TOOLTIPS)
p1.xgrid.grid_line_color = None
p1.ygrid.grid_line_alpha = 0.5
p1.yaxis.axis_label = 'Percent'
p1.y_range.start = 0
p1.x_range.range_padding = 0.1

p1.vbar_stack(categories , x='Test' , width = 0.9 , color = [Greys4[0] , Greys4[2]] , source = data , legend_label = categories)

p2 = figure(title = 'Demographic Breakdown' , plot_height = 350 , plot_width = 400)

p2.wedge(x = 0 , y = 1 , radius = 0.25 , start_angle = cumsum('angle' , include_zero = True) , end_angle = cumsum('angle') , \
    line_color = 'white' , fill_color = 'color' , source = demoPieGraph_df , legend_group = 'categories')

# eldersGraph_df.plot_bokeh(kind = 'bar' , stacked = True , colormap = [Greys4[0] , Greys4[2]])

st.bokeh_chart(row(p1 , p2))
