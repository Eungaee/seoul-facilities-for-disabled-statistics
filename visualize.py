import folium
import numpy as np
import pandas as pd
import json
import re


geo_json = "https://raw.githubusercontent.com/southkorea/seoul-maps/master/kostat/2013/json/seoul_municipalities_geo_simple.json"


def getMap(statsData, legend, color):
    map = folium.Map(
        location=[37.5642135, 127.0016985],
        zoom_start=11,
        min_zoom=10,
        max_zoom=12,
        zoom_control=False,
        tiles="cartodbpositron",
    )

    folium.Choropleth(
        geo_data=geo_json,
        name="choropleth",
        data=statsData,
        columns=statsData.columns,
        key_on='feature.properties.name',
        fill_color=color,
        fill_opacity=0.75,
        line_opacity=0.25,
        nan_fill_color="grey",
        nan_fill_opacity=0.75,
        legend_name=legend
    ).add_to(map)

    return map


disabledPersons = pd.read_csv("./data/disabledPopularity.csv", encoding="utf-8", skiprows=1)
pers = disabledPersons.drop(columns=["자치구별(1)"])
pers.rename(columns={"자치구별(2)" : "자치구", "계" : "거주자 수"}, inplace=True)
pers1 = pers[["자치구", "거주자 수"]]
pers2 = pers1.drop(index=0)
""" persons = persons.sort_values(by="자치구")
persons["자치구"] = persons["자치구"].apply(lambda x: re.compile("[가-힣]+").findall(x)[0]) """

conv = pd.read_csv(r"./data/disabledConv.csv", encoding="utf-8", skiprows=1)
conv1 = conv.drop(columns=["자치구별(1)"]);
conv2 = conv1[["자치구별(2)",
                "전체 (개)", "전체 (%)", 
                "매개시설 (개)", "매개시설 (%)", 
                "내부시설 (개)" , "내부시설 (%)", 
                "위생시설 (개)", "위생시설 (%)", 
                "안내시설 (개)", "안내시설 (%)", 
                "기타시설 (개)", "기타시설 (%)"]]
conv3 = conv2.rename(columns={"자치구별(2)" : "자치구"}, inplace=False)
convAmount = conv3[["자치구", "전체 (개)"]]
convPer = conv3[["자치구", "전체 (%)"]]
acsConvAmount = conv3[["자치구", "매개시설 (개)"]]
acsConvPer = conv3[["자치구", "매개시설 (%)"]]
mobiConvAmount = conv3[["자치구", "내부시설 (개)"]]
mobiConvPer = conv3[["자치구", "내부시설 (%)"]]
tConvAmount = conv3[["자치구", "위생시설 (개)"]]
tConvPer = conv3[["자치구", "위생시설 (%)"]]
infoConvAmount = conv3[["자치구", "안내시설 (개)"]]
infoConvPer = conv3[["자치구", "안내시설 (%)"]]
convAmount = convAmount.drop(index=0)
convPer = convPer.drop(index=0)
acsConvAmount = acsConvAmount.drop(index=0)
acsConvPer = acsConvPer.drop(index=0)
mobiConvAmount = mobiConvAmount.drop(index=0)
mobiConvPer = mobiConvPer.drop(index=0)
tConvAmount = tConvAmount.drop(index=0)
tConvPer = tConvPer.drop(index=0)
infoConvAmount = infoConvAmount.drop(index=0)
infoConcPer = infoConvPer.drop(index=0)

popularityMap = getMap(pers2, "장애인 거주자 수", "Blues")
popularityMap.save("./maps/popularityMap.html")

convAmountMap = getMap(convAmount, "장애인 이용시설 전체 (개)", "YlGn")
convAmountMap.save("./maps/convAmountMap.html")

convPercentageMap = getMap(convPer, "장애인 이용시설 전체 (설치율 %)", "RdYlGn")
convPercentageMap.save("./maps/convPercentageMap.html")

acsConvAmountMap = getMap(acsConvAmount, "장애인 매개시설 (개)", "YlGn")
acsConvAmountMap.save("./maps/acsConvAmountMap.html")

acsConvPerMap = getMap(acsConvPer, "장애인 매객시설 (설치율 %)", "RdYlGn")
acsConvPerMap.save("./maps/acsConvPerMap.html")

mobiConvAmountMap = getMap(mobiConvAmount, "장애인 내부시설 (개)", "YlGn")
mobiConvAmountMap.save("./maps/mobiConvAmountMap.html")

mobiconvPerMap = getMap(mobiConvPer, "장애인 내부시설 (설치율 %)", "RdYlGn")
mobiconvPerMap.save("./maps/mobiconvPerMap.html")

tConvAmountMap = getMap(tConvAmount, "장애인 위생시설 (개)", "YlGn")
tConvAmountMap.save("./maps/tConvAmountMap.html")

tConvPerMap = getMap(tConvPer, "장애인 위생시설 (설치율 %)", "RdYlGn")
tConvPerMap.save("./maps/tConvPerMap.html")

infoConvAmountMap = getMap(infoConvAmount, "장애인 안내시설 (개)", "YlGn")  #광진구: NaN
infoConvAmountMap.save("./maps/infoConvAmountMap.html")

infoConvPerMap = getMap(infoConvPer, "장애인 안내시설 (설치율 %)", "Spectral")  #광진구: NaN
infoConvPerMap.save("./maps/infoConvPerMap.html")