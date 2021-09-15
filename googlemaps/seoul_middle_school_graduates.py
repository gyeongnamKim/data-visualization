import folium
import pandas as pd
import numpy as np
import googlemaps,json
#구글 맵스, 서울시 지오 데이터 가져오기

#api 키 입력
gmaps = googlemaps.Client(key='googlemaps API keys')
#


geo_data = json.load(open('../data/02. skorea_municipalities_geo_simple.json', encoding='utf-8'))
#파일 읽어오기
graduates_data = pd.read_excel('../data/2016_middle_shcool_graduates_report.xlsx')
del graduates_data['Unnamed: 0']

#구별 진학률 구하기
graduates_data['진학률'] = np.sum(graduates_data.iloc[:,7:16],axis=1)
graduates_data['진학률'] = graduates_data['진학률'].apply(lambda x:1 if x > 1 else x)
graduates_gu = graduates_data.groupby('지역')['진학률'].mean().to_frame()
#서울시 지도에 학교의 위치를 표시
school_map = folium.Map(location=[37.59344046685624, 126.97465047107741], tiles="OpenStreetMap", zoom_start=11)
#특수고 진학률 구하기
graduates_data['특수고진학률'] = np.sum(graduates_data.iloc[:,8:11],axis=1)
graduates_data.sort_values(by='특수고진학률',ascending=False,inplace=True)
#지도 표시
for i in range(len(graduates_data.index)):
    llmap = gmaps.geocode(graduates_data.loc[i,'지역']+' '+graduates_data.loc[i,'학교명'])
    lat =llmap[0]['geometry']['location']['lat']
    lng = llmap[0]['geometry']['location']['lng']
    #특수고 진학률 상위 10 지도에 표시
    if i < 10:
        folium.Marker(
            location=[lat, lng],
            popup=graduates_data.loc[i, '학교명'],
            icon=folium.Icon(color='blue', icon='hand-up')
        ).add_to(school_map)
    # 특수고 진학률 하위 10 지도에 표시
    elif i >= (len(graduates_data.index)-10):
        folium.Marker(
            location=[lat, lng],
            popup=graduates_data.loc[i, '학교명'],
            icon=folium.Icon(color='red', icon='hand-down')
        ).add_to(school_map)
    else:
        folium.Marker(
            location=[lat, lng],
            popup=graduates_data.loc[i, '학교명'],
            icon=folium.Icon(color='green', icon='flag')
        ).add_to(school_map)
#구별 진학률 평균 표시하기
folium.Choropleth(geo_data=geo_data,
                  data = graduates_gu,
                  columns=[graduates_gu.index,'진학률'],
                  key_on='feature.id',
                  fill_color='BuPu'
                  ).add_to(school_map)
#지도 html로 저장
school_map.save('./school_map.html')

