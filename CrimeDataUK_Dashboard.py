#!/usr/bin/env python
# coding: utf-8

# In[64]:


import pandas as pd
import numpy as np
import panel as pn
pn.extension('tabulator')

import hvplot.pandas


# In[65]:


df = pd.read_csv("Data_Final1.csv")
df = df[df['Year_Month'] <= '2020-12']


# In[66]:


df


# In[67]:


df = df.rename({
'Crime type' : 'Crime_Type',
'LAD19CD': 'LAD_Codes', 
'LAD19NM': 'LAD_Names',
'CTYNM': 'County',
'CNTY21NM': 'Country',
'NTN21NM':'Nation',
'Population Density':'Population_Density'}, axis=1)


# In[68]:


year_slider = pn.widgets.IntSlider(name='Year slider', start=2013, end=2020, step=1, value=2014)
year_slider


# In[69]:


select_rgn = pn.widgets.Select(name='Select', options=['North East', 'North West', 'Yorkshire and The Humber',
       'East Midlands', 'West Midlands', 'South West', 'East of England',
       'South East', 'London'])


# In[70]:


idf = df.interactive()


# In[71]:


crimeyr_pipeline = (
    idf[
        (idf.Year == year_slider) &
        (idf.RGN19NM == select_rgn)
    ].groupby(['Year', 'Crime_Type'])['Frequency'].sum()
    .to_frame()
    .reset_index()
    .sort_values(by='Crime_Type') 
    .reset_index(drop=True)
)


# In[72]:


type(crimeyr_pipeline)


# In[73]:


cryr_plot = crimeyr_pipeline.pipe(pn.widgets.Tabulator, pagination='remote', page_size = 14, layout='fit_columns',show_index=False) 
cryr_plot


# In[ ]:





# In[74]:


select_typ = pn.widgets.Select(name='Select', options=['Anti-social behaviour', 'Bicycle theft', 'Burglary',
       'Criminal damage and arson', 'Drugs', 'Other crime', 'Other theft',
       'Possession of weapons', 'Public order', 'Robbery', 'Shoplifting',
       'Theft from the person', 'Vehicle crime',
       'Violence and sexual offences'])


# In[75]:


crimeyrtp_pipeline = (
    idf[
        (idf.Year == year_slider) &
        (idf.Crime_Type == select_typ)
    ].groupby(['Year', 'RGN19NM'])['Frequency'].sum()
    .to_frame()
    .reset_index()
    .sort_values(by='RGN19NM') 
    .reset_index(drop=True)
)


# In[76]:


cryrtyp_plot = crimeyrtp_pipeline.pipe(pn.widgets.Tabulator, pagination='remote', page_size = 9, layout='fit_columns',show_index=False) 
cryrtyp_plot


# In[77]:


crimergn_pipeline = (
    idf[(idf.RGN19NM == select_rgn ) & (idf.Crime_Type== select_typ) ].groupby(['Year_Month'])['Frequency'].sum()
    .to_frame()
    .reset_index()
    .sort_values(by='Year_Month') 
    .reset_index(drop=True)
)


# In[78]:


crrgn_plot = crimergn_pipeline.hvplot(x = 'Year_Month', y='Frequency',legend=False,xticks=0,line_width=2,fontsize=10, title="Total Crime Frequency plot for Region across 2013-2020")
crrgn_plot


# In[83]:


crimetyp1_pipeline = (
    idf[(idf.Crime_Type == select_typ )].groupby(['Year_Month'])['Frequency'].sum()
    .to_frame()
    .reset_index()
    .sort_values(by='Year_Month') 
    .reset_index(drop=True)
)


# In[84]:


crtyp1_plot = crimetyp1_pipeline.hvplot(x = 'Year_Month', y='Frequency',legend=False,line_width=2, title="Total Crime Frequency plot for crime type across 2013-2020")
crtyp1_plot


# In[79]:


crimetyp_pipeline = (
    idf[(idf.Crime_Type == select_typ )].groupby(['Year_Month','RGN19NM'])['Frequency'].sum()
    .to_frame()
    .reset_index()
    .sort_values(by='Year_Month') 
    .reset_index(drop=True)
)


# In[80]:


crtyp_plot = crimetyp_pipeline.hvplot(x = 'Year_Month', y='Frequency',by='RGN19NM',legend=False,line_width=2, title="Crime Frequency plot for crime type and region across 2013-2020")
crtyp_plot


# In[95]:


template = pn.template.FastListTemplate(
    title='Crime frequency:England dashboard', 
    sidebar=[pn.pane.Markdown("# Crime frequency England dashboard"), 
             pn.pane.Markdown("#### Choose from the options below"), 
             pn.pane.Markdown("## Settings"),   
             year_slider,select_rgn,select_typ],
    main=[pn.Row(pn.Column(cryr_plot.panel(width=260), margin=(0,25)), 
                 pn.Column(crrgn_plot.panel(width=700))), 
          pn.Row(pn.Column(cryrtyp_plot.panel(width=260), margin=(0,25)),
              pn.Column(crtyp1_plot.panel(width=700))),
          pn.Row(
              pn.Column(crtyp_plot.panel(width=700),margin=(20,100)))],
    accent_base_color="#88d8b0",
    header_background="#88d8b0",
)
template.show()
template.servable();


# In[ ]:


pn.Column(cryrtyp_plot.panel(width=260), margin=(0,25))


# In[ ]:





# In[ ]:





# In[ ]:




