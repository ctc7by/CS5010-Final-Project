#!/usr/bin/env python
# coding: utf-8

# In[197]:


from os.path import dirname, join

import numpy as np
import pandas as pd


from bokeh.plotting import figure
from bokeh.layouts import layout, column, widgetbox
from bokeh.models import ColumnDataSource, Div, Slider, Select, TextInput, RangeSlider, MultiSelect, CheckboxGroup
from bokeh.io import curdoc, output_file, show
from bokeh.sampledata.movies_data import movie_path


# In[194]:


fifa = pd.read_csv('FIFA Player Info.csv')
fifa = fifa.drop(columns='Unnamed: 0')

axis_map = dict(zip(fifa.select_dtypes(include='int').columns.values, fifa.select_dtypes(include='int').columns.values))

fifa["color"] = np.where(fifa['Overall Rating'] > 50, "orange", "grey")


# In[229]:


fifa
#axis_map


# In[233]:


overall_rating = RangeSlider(title="Overall Rating", start=fifa['Overall Rating'].min(), end=fifa['Overall Rating'].max(), value=(fifa['Overall Rating'].min(), fifa['Overall Rating'].max()), step=1)
skill = RangeSlider(title="Skill", start=fifa['Skill'].min(), end=fifa['Skill'].max(), value=(fifa['Skill'].min(), fifa['Skill'].max()), step=1)
club = MultiSelect(title="Club", options=fifa.sort_values('Club').Club.unique().tolist())
league = Select(title="League", value="All", options=fifa.sort_values('League').League.unique().tolist())
country = MultiSelect(title="Country", options=fifa.sort_values('Country').Country.unique().tolist())
continent = MultiSelect(title="Continent", options=fifa.sort_values('Continent').Continent.dropna().unique().tolist())
position = CheckboxGroup(name="Position", labels=['CF', 'ST', 'RW', 'RF', 'LW', 'LF', 'RM', 'LM', 'CAM', 'CM', 'CDM', 'LB', 'LWB', 'RB', 'RWB', 'CB', 'GK'])
position_group = CheckboxGroup(name="Position Group", labels=fifa.sort_values('Position Group')['Position Group'].unique().tolist())
player = TextInput(title="Player Name")
show(overall_rating)


update()  # initial load of the data
layout = column(widgetbox(overall_rating))
curdoc().add_root(layout)
curdoc().title = "FIFA Players"


# In[ ]:




