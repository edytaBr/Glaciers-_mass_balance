#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 16 22:16:45 2020

@author: edyta
"""
import os
import pandas as pd
import folium
from bs4 import BeautifulSoup
import requests
import altair as alt
from folium import CircleMarker
 
url="http://glacier.nve.no/Glacier/viewer/CI/en/nve/ClimateIndicatorInfo/"


names= ["Svartfjelljøkelen", "Langfjordjøkelen", "Blåisen", "Storsteinsfjellbreen", "Cainhavarre", "Rundvassbreen", "Glombreen", "Tretten-null-to-breen ", "Storglombreen nord", "Kjølbreen", "Engabreen", "Svartisheibreen", "Høgtuvbreen", "Trollbergdalsbreen", "Charles Rabot-breen", "Austre Okstindbreen", "Ålfotbreen", "Hansebreen", "Vetlefjordbreen", "Nigardsbreen", "Tunsbergdalsbreen", "Supphellebreen", "Vesledalsbreen", "Austdalsbreen", "Harbardsbreen", 
"Spørteggbreen", "Juvfonne", "Tverråbrean", "Storbreen", "Gråsubreen", "Hellstugubreen", "Austre Memurubre", "Blåbrean", "Vestre Memurubre", "Omnsbreen", "Midtdalsbreen", "Rembesdalskåka", "Midtre Folgefonna", "Blåbreen", "Gråfjellsbrea", "Breidablikkbrea", "Ruklebreen", "Bondhusbrea", 
"Svelgjabreen", "Møsevassbrea", "Blomstølskardsbreen"]

names_url = ["26?name=Svartfjelljøkelen", "54?name=Langfjordjøkelen", "596?name=Blåisen", "675?name=Storsteinsfjellbreen", "703?name=Cainhavarre", "941?name=Rundvassbreen", "1052?name=Glombreen", "1084?name=Tretten-null-to-breen", "1092?name=Storglombreen%20nord", "1093?name=Kjølbreen", "1094?name=Engabreen", "1135?name=Svartisheibreen", "1144?name=Høgtuvbreen", "1280?name=Trollbergdalsbreen", "1434?name=Charles%20Rabot-breen", "1438?name=Austre%20Okstindbreen", "2078?name=Ålfotbreen", "2085?name=Hansebreen", "2148?name=Vetlefjordbreen", "2297?name=Nigardsbreen", "2320?name=Tunsbergdalsbreen", "2352?name=Supphellebreen", "2474?name=Vesledalsbreen", "2478?name=Austdalsbreen", "2514?name=Harbardsbreen", 
"2527?name=Spørteggbreen", "2597?name=Juvfonne", "2632?name=Tverråbrean", "2636?name=Storbreen", "2743?name=Gråsubreen", "2768?name=Hellstugubreen", "2769?name=Austre%20Memurubre", "2770?name=Blåbrean", "2772?name=Vestre%20Memurubre", "2919?name=Omnsbreen", "2964?name=Midtdalsbreen", "2968?name=Rembesdalskåka", "3119?name=Midtre%20Folgefonna", "3126?name=Blåbreen", "3127?name=Gråfjellsbrea", "3128?name=Breidablikkbrea", "3129?name=Ruklebreen", "3133?name=Bondhusbrea", 
"3137?name=Svelgjabreen", "3138?name=Møsevassbrea", "3141?name=Blomstølskardsbreen"]

urlss = []
for name in names_url:
   url += name
   urlss.append(url)
   url="http://glacier.nve.no/Glacier/viewer/CI/en/nve/ClimateIndicatorInfo/"
    
html_contents = []
for elem in urlss:
    ge =  requests.get(elem).text
    html_contents.append(ge)

soups = []
for elem in html_contents:
    data = BeautifulSoup(elem, "lxml")
    soups.append(data)

text1 =[]
for i in range(len(soups)): 
    for link in (soups[i]).find_all("table", attrs={"class": "table table-bordered", "id": "massbalanceTable"}):
       text1.append("Inner Text: {}".format(link.text)) 
       i+=1
       
out = []
for elem in text1:
    out.append(elem.split())
    
source = []
opis =[]
for elem in out:
    year = elem [12::4]
    winter = elem[13::4]
    opis.append("Winter")
    source.append(pd.DataFrame(list(zip(year, winter, opis)), columns =[ 'Year', 'Value', "Balance"]))

source2 = []
opis2 =[]

for elem in out:
    year = elem [12::4]
    summer = elem[14::4]
    opis2.append("Summer")
    source2.append(pd.DataFrame(list(zip(year, summer, opis2)), columns =[ 'Year', 'Value', "Balance"]))

source3 = []
opis3 =[]
for elem in out:
    year = elem [12::4]
    summer = elem[15::4]
    opis3.append("Annual")
    source3.append(pd.DataFrame(list(zip(year, summer, opis3)), columns =[ 'Year', 'Value', "Balance"]))


for elem in source:
    elem['Value'] = pd.to_numeric(elem['Value'], errors='coerce').fillna(0).astype(float)

for elem in source2:
    elem['Value'] = pd.to_numeric(elem['Value'], errors='coerce').fillna(0).astype(float)

for elem in source3:
    elem['Value'] = pd.to_numeric(elem['Value'], errors='coerce').fillna(0).astype(float)

result = []
for i,j,k in zip(source, source2, source3):
    result.append(pd.concat([i, j, k], ignore_index = True))
    

for elem in result:
    elem['Year'] = pd.to_numeric(elem['Year'], errors='coerce').fillna(0).astype(int)


isbre = os.path.join('/home/edyta/glacier/','glacier_mass.json')
data = pd.read_csv('glacier_point.csv')


m = folium.Map(location=[60.3935, 5.325], zoom_start=4,  tiles='cartodbpositron') 
m.choropleth(
 geo_data=isbre,
 fill_opacity=0.4, line_opacity=0.9, 
 color="black"
 )


plots = []
for dane in result:
    chart = alt.Chart(dane).mark_bar(size=20, cornerRadiusTopLeft=5,
    cornerRadiusTopRight=10, opacity=0.8).encode(
         alt.X("Year:Q", bin=alt.Bin(extent=[min(dane['Year']-1), max(dane['Year']+1)], step=1), axis=alt.Axis(format='.0f')),
        y='Value:Q', color=alt.Color('Balance', scale=alt.Scale(range=['black', 'red', "blue"]))).configure_axisX(
    labelAngle=90)
    vis1 = chart.to_json()
    plots.append(vis1)



#ADD MARKER
data = pd.read_csv('glacier_point.csv')
for i in range(0,len(data)):
     for plot in plots:
        m.add_child(CircleMarker(
        location = [data['x'][i], data['y'][i]],
        popup= (folium.Popup(max_width=1000).add_child(folium.VegaLite(plots[i]))),
        fill_opacity = 0.3, 
        color="darkblue",
        fill_color = ('white'),
        marker="o", markersize=16, 
        markeredgewidth=1)

        )


m.save('isbre.html')
