import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input,Output
import plotly.graph_objs as go
import pandas as pd
#대시보드 라이브러리

#데이터 읽어오기
data = pd.read_csv('./data/globalterror.csv')


cont_data=None
#대시 보드 시작
app = dash.Dash(__name__,meta_tags=[{'name':'viewport','content':'width=device-width'}])
app.layout = html.Div([
    html.Div([
        html.Div([
            html.H4(children='전세계 테러 분석 현황',
                style={'textAlign':'center',
                       'color':'white'}),
            html.H5(id='years_result',style={'textAlign':'center',
                       'color':'white'})
        ],className='half column',id='title'),
    ],className='row flex display'),
    html.Div([
        html.Div([
            dcc.Graph(id='map_chart', config={'displayModeBar': 'hover'})
        ],className='create_container1 twelve columns')
    ],className='row flex display'),
    html.Div([

        html.Div([
            html.P('대륙 선택',className='fix_label',style={'color':'white'}),
            dcc.Dropdown(id='select_continent',
                         multi=False,
                         searchable=True,
                         value='East Asia',
                         placeholder='Select Continent',
                         options=[{'label':c,'value':c} for c in (data['region_txt'].unique())],
                         className='dcc_compon'),
            html.P('국가 선택',className='fix_label',style={'color':'white'}),
            dcc.Dropdown(id='select_country',
                         multi=False,
                         searchable=True,
                         value='South Korea',
                         placeholder='Select Country',
                         className='dcc_compon'),
            html.P('년도 선택',className='fix_label',style={'color':'white'}),
            dcc.RangeSlider(id='range_years',
                            min=1970,
                            max=2017,
                            step=1,
                            value=[1970,2017])
        ],className='create_container2 three columns',style={'height':'500px'}),
        html.Div([
            dcc.Graph(id='bar_chart',config={'displayModeBar':'hover'})
        ],className='create_container2 six columns'),
        html.Div([
            dcc.Graph(id='pie_chart',config={'displayModeBar':'hover'})
        ],className='create_container2 three columns')


    ],className='row flex display')

],id='mainContainer',style={'display':'flex','flex-direction':'column'})

@app.callback(Output('select_country','options'),
              [Input('select_continent','value')])
def update(select_continent):
    cont_data = data[data['region_txt']==select_continent]
    return [{'label': c, 'value': c} for c in (cont_data['country_txt'].unique())]

@app.callback(Output('years_result','children'),
              [Input('range_years','value')])
def update(range_years):
    return '{}  -  {}'.format(range_years[0],range_years[1])

@app.callback(Output('bar_chart','figure'),
              [Input('select_continent','value'),
               Input('select_country','value'),
               Input('range_years','value')])
def update(select_continent,select_country,range_years):
    terr_data = data.groupby(['region_txt','country_txt','iyear'])[['nkill','nwound','attacktype1']].sum().reset_index()
    terr_data1 = terr_data[(terr_data['region_txt'] == select_continent)&\
                           (terr_data['country_txt'] == select_country) & \
                           (terr_data['iyear'] >= range_years[0])&(terr_data['iyear'] <= range_years[1])]
    return {
        'data': [go.Scatter(
            x=terr_data1['iyear'], y=terr_data1['nkill'],
            mode='markers+lines',
            name='사망',
            line=dict(shape='spline',smoothing=1.3,width=3,color='#FF00FF'),
            marker=dict(color='white',size=10,symbol='circle',
                        line=dict(color='#FF00FF',width=2)),

            hoverinfo='text',
            hovertext=
            '<b>대륙</b>: ' + terr_data1['region_txt'].astype(str) + '<br>' +
            '<b>나라</b>: ' + terr_data1['country_txt'].astype(str) + '<br>' +
            '<b>년도</b>: ' + terr_data1['iyear'].astype(str) + '<br>' +
            '<b>사망</b>: ' + [f'{x:,.0f}' for x in terr_data1['nkill']] + '<br>'
        ),
        go.Bar(
            x=terr_data1['iyear'], y=terr_data1['nwound'],
            text=terr_data1['nwound'],
            texttemplate='%{text:,.0f}',
            textposition='auto',
            name='부상',
            marker=dict(color='#9C0C38'),
            hoverinfo='text',
            hovertext=
            '<b>대륙</b>: ' + terr_data1['region_txt'].astype(str) + '<br>' +
            '<b>나라</b>: ' + terr_data1['country_txt'].astype(str) + '<br>' +
            '<b>년도</b>: ' + terr_data1['iyear'].astype(str) + '<br>' +
            '<b>부상</b>: ' + [f'{x:,.0f}' for x in terr_data1['nwound']] + '<br>'
        ),
            go.Bar(
                x=terr_data1['iyear'], y=terr_data1['attacktype1'],
                text=terr_data1['attacktype1'],
                texttemplate='%{text:,.0f}',
                textposition='auto',
                name='공격',
                marker=dict(color='orange'),
                hoverinfo='text',
                hovertext=
                '<b>대륙</b>: ' + terr_data1['region_txt'].astype(str) + '<br>' +
                '<b>나라</b>: ' + terr_data1['country_txt'].astype(str) + '<br>' +
                '<b>년도</b>: ' + terr_data1['iyear'].astype(str) + '<br>' +
                '<b>공격</b>: ' + [f'{x:,.0f}' for x in terr_data1['attacktype1']] + '<br>'
            )
        ],
        'layout': go.Layout(
            plot_bgcolor='black',
            paper_bgcolor='black',
            barmode='stack',
            title={'text': '사망, 부상, 공격 : '+(select_country)+' '+'<br>'
                    +' - ' .join([str(y) for y in range_years]),
                   'y':0.93,
                   'x':0.5,
                   'xanchor':'center',
                   'yanchor':'top'},
            titlefont={'color': 'white',
                       'size':20},
            font=dict(family='sans-serif', color='white', size=12),
            margin=dict(r=0),
            hovermode='closest',
            legend={'orientation': 'h',
                    'bgcolor': '#010915',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            xaxis= dict(title='<b>년도</b>',
                        tick0=0,
                        dtick=1,
                        color='white',
                        showline=True,
                        showgrid=True,
                        showticklabels=True,
                        linecolor='white',
                        linewidth=1,
                        ticks='outside',
                        tickfont=dict(
                            family='Aerial',
                            color='white',
                            size=12
                       )),
            yaxis=dict(title='<b>사망, 부상, 공격 </b>',
                       color='white',
                       showline=True,
                       showgrid=True,
                       showticklabels=True,
                       linecolor='white',
                       linewidth=1,
                       ticks='outside',
                       tickfont=dict(
                           family='Aerial',
                           color='white',
                           size=12
                       )),
        )
    }

@app.callback(Output('pie_chart','figure'),
              [Input('select_continent','value'),
               Input('select_country','value'),
               Input('range_years','value')])
def update_graph(select_continent,select_country,range_years):
    terr_data1 = data[(data['region_txt'] == select_continent) & \
                      (data['country_txt'] == select_country) & \
                      (data['iyear'] >= range_years[0]) & (data['iyear'] <= range_years[1])]
    terr_data = terr_data1.groupby(['country_txt'])[
        ['nkill', 'nwound', 'attacktype1']].sum().reset_index()
    a = float(terr_data.iloc[0,1])
    b = float(terr_data.iloc[0,2])
    c = float(terr_data.iloc[0,3])
    colors = ['pink','#9C0C38', 'orange']
    return {
        'data': [go.Pie(
            labels=['사망 총계', '부상 총계', '공격 총계'],
            values=[a,b,c],
            marker=dict(colors=colors),
            hoverinfo='label+value+percent',
            textinfo='label+value',
            texttemplate='%{label}<br>%{value}',
            textposition='auto',
            hole=.7,
            rotation=160
        )],
        'layout': go.Layout(
            paper_bgcolor='black',
            title={'text': '사망, 부상, 공격 : '+(select_country)+' '+'<br>'
                    +' - ' .join([str(y) for y in range_years]),
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 15},
            font=dict(family='sans-serif',
                      color='white',
                      size=12),
            plot_bgcolor='#1f2c56',
            legend={'orientation':'h',
                    'bgcolor':'black',
                    'xanchor':'center','x':0.5,'y':-0.7}
        )
    }
@app.callback(Output('map_chart','figure'),
              [Input('select_continent', 'value'),
               Input('select_country', 'value'),
               Input('range_years', 'value')])
def update_graph(select_continent, select_country, range_years):
    terr_data1 = data[(data['region_txt'] == select_continent) & \
                           (data['country_txt'] == select_country) & \
                           (data['iyear'] >= range_years[0]) & (data['iyear'] <= range_years[1])]
    terr_data = terr_data1.groupby(['latitude','longitude','country_txt'])[['nkill','nwound','attacktype1']].max().reset_index()
    terr_data['total'] = terr_data['nkill'] + terr_data['nwound'] + terr_data['attacktype1']
    zoom = 5
    zoom_lat = terr_data['latitude'][0]
    zoom_long = terr_data['longitude'][1]
    return {
        'data': [go.Scattermapbox(
            lon=terr_data['longitude'],
            lat=terr_data['latitude'],
            mode='markers',
            marker=go.scattermapbox.Marker(size=terr_data['total'] *50,
                                           color=terr_data['total'],
                                           colorscale='HSV',
                                           showscale=False,
                                           sizemode='area',
                                           opacity=0.3),
            hoverinfo='text',
            hovertext=
            '<b>경도</b>: ' + terr_data['longitude'].astype(str) + '<br>' +
            '<b>위도</b>: ' + terr_data['latitude'].astype(str) + '<br>' +
            '<b>사망</b>: ' + [f'{x:,.0f}' for x in terr_data['nkill']] + '<br>'+
            '<b>부상</b>: ' + [f'{x:,.0f}' for x in terr_data['nwound']] + '<br>'+
            '<b>공격</b>: ' + [f'{x:,.0f}' for x in terr_data['attacktype1']] + '<br>'
        )
        ],
        'layout': go.Layout(
            hovermode='x',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            margin=dict(r=0,l=0,b=0,t=0),
            mapbox=dict(
                accesstoken='pk.eyJ1IjoicXM2MjcyNTI3IiwiYSI6ImNraGRuYTF1azAxZmIycWs0cDB1NmY1ZjYifQ.I1VJ3KjeM-S613FLv3mtkw',
                center= go.layout.mapbox.Center(lat=zoom_lat,lon=zoom_long),
                style='dark',
                zoom=zoom
            ),
            autosize=True

        )
    }
if __name__ == '__main__':
    app.run_server(debug=False,port=8080,host='127.0.0.1')