import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from data import output_business, output_num, data_growth_business, data_growth_num
import numpy as np
import copy
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas as pd


pd.options.display.float_format = '{:.2f}'.format
#전처리 된 데이터 불러오기
data_original = pd.read_csv('./data/result_data.csv',encoding='cp949')
main_data = data_original.iloc[1:,:]

app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

# 사업체 수 성장률 그래프
fig_business = px.bar(data_growth_business,
                      x=data_growth_business["growth_business"],
                      y=data_growth_business.index, orientation='h'
                      , color='구분', height=500)
fig_business.add_vline(x=2.2, line_dash="dash", line_color="red")

# 사업체 수 성장률 레이아웃
fig_business.update_layout(title={'text': "사업체 수 성장률 그래프",
                                  'y': 0.99, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                           titlefont={'color': 'white','size': 20},
                           font=dict(family='sans-serif',
                           color='white',
                           size=15),
                           hovermode='closest',
                           paper_bgcolor='#607178',
                           plot_bgcolor='#607178',
                           margin=dict(t=40, r=0),
                           xaxis=dict(title='<b></b>',
                                      color='white',
                                      showline=False,
                                      showgrid=False,
                                      showticklabels=True,
                                      linecolor='white',
                                      linewidth=1,
                                      ticks='outside',
                                      tickfont=dict(family='Aerial', color='white',size=12)),
                           yaxis=dict(title='<b></b>',
                                      color='white',
                                      showline=False,
                                      showgrid=False,
                                      showticklabels=True,
                                      linecolor='white',
                                      linewidth=1,
                                      ticks='outside',
                                      tickfont=dict(family='Aerial',color='white',size=12)))


# 종사자 수 성장률 그래프
fig_num = px.bar(data_growth_num,
                 x=data_growth_num["growth_num"],
                 y=data_growth_num.index, orientation='h',
                 color='구분')
fig_num.add_vline(x=2.99, line_dash="dash", line_color="red")

# 종사자 수 그래프 레이아웃
fig_num.update_layout(title={'text': "종사자 수 성장률 그래프",
                             'y': 0.99, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                      titlefont={'color': 'white','size': 20},
                      font=dict(family='sans-serif',
                      color='white',
                      size=15),
                      hovermode='closest',
                      paper_bgcolor='#607178',
                      plot_bgcolor='#607178',
                      margin=dict(t=40, r=0),
                      xaxis=dict(title='<b></b>',
                                 color='white',
                                 showline=False,
                                 showgrid=False,
                                 showticklabels=True,
                                 linecolor='white',
                                 linewidth=1,
                                 ticks='outside',
                                 tickfont=dict(family='Aerial', color='white',size=12)),
                      yaxis=dict(title='<b></b>',
                                 color='white',
                                 showline=False,
                                 showgrid=False,
                                 showticklabels=True,
                                 linecolor='white',
                                 linewidth=1,
                                 ticks='outside',
                                 tickfont=dict(family='Aerial',color='white',size=12)))

# 전체 산업 종사자/사업체 상관 계수
cor = np.corrcoef(output_business['전체 산업'],output_num['전체 산업'])


app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div([
                # 타이틀
                html.H4(children="인천시 산업별 종사자,사업체 수 분석",
                        style={'textAlign': 'center',
                               'color': '#FFF'}),
            ], className='half column', id='title'),
        ], className='row flex display'),


        html.Div([
            html.Div([
                html.Div([
                    # 사업체/종사자 선택 라디오 박스
                    dcc.RadioItems(id="num_or_business",
                                   labelStyle={'display': 'inline-block'},
                                   options=[{'label': '사업체수', 'value': 'business'},
                                            {'label': '종사자수', 'value': 'num'}],
                                   value='business',
                                   style={'text-align': 'center', 'color': 'white'},
                                   className='radio_compon'),
                    # 종사자/사업체 수 전체 비교 그래프
                    dcc.Graph(id='total_graph', config={'displayModeBar': 'hover'},
                              style={'height': '400px'})
                ], className='create_container2 twelve columns', style={'height': '450px'}),
            ]),
        ]),

        html.Div([
            html.Div([
                html.P('산업 종류 선택', className='fix_label', style={'textAlign': 'center', 'color': 'white'}),
                # 드롭다운 메뉴
                dcc.Dropdown(
                    id='dropdown_business',
                    options=[
                        {'label': i, 'value': n} for n, i in enumerate(output_business)],
                    value=0,
                    className='dcc_compon'),

                # 산업별 상관관계 계수
                html.Div(id='text1'),

            ], className='create_container2 three columns', style={'height': '370px'}),

        ]), html.Div(id='business_con'),
        html.Div([
            html.Div([
                # 산업별 비교 그래프
                dcc.Graph(id='compare_graph', config={'displayModeBar': 'hover'},
                          style={'height': '350px'})
            ], className='create_container2 nine columns', style={'height': '370px'}),
        ]),

        html.Div([
            html.Div([
                # 사업체 수 성장률 그래프
                dcc.Graph(figure=fig_business, config={'displayModeBar': 'hover'},
                          style={'height': '450px'})
            ], className='create_container2 four columns', style={'height': '500px'}),

            html.Div([
                html.H6(children="사업체 수 성장률 상/하위",
                        style={'textAlign': 'center',
                               'color': 'white'}),
                html.H5(children="성장률 상위 3순위",
                        style={'textAlign': 'center',
                               'color': 'white'}),
                html.P('1. {}'.format(data_growth_business.index[0]),
                       style={'textAlign': 'center',
                              'color': 'orange',
                              'fontSize': 13,
                              'margin-top': '-10px'}),
                html.P('2. {}'.format(data_growth_business.index[1]),
                       style={'textAlign': 'center',
                              'color': 'orange',
                              'fontSize': 13,
                              'margin-top': '-10px'}),
                html.P('3. {}'.format(data_growth_business.index[2]),
                       style={'textAlign': 'center',
                              'color': 'orange',
                              'fontSize': 13,
                              'margin-top': '-10px'}),
                html.H5(children="성장률 하위 3순위",
                        style={'textAlign': 'center',
                               'color': 'white'}),
                html.P('1. {}'.format(data_growth_business.index[19]),
                       style={'textAlign': 'center',
                              'color': 'orange',
                              'fontSize': 13,
                              'margin-top': '-10px'}),
                html.P('2. {}'.format(data_growth_business.index[18]),
                       style={'textAlign': 'center',
                              'color': 'orange',
                              'fontSize': 13,
                              'margin-top': '-10px'}),
                html.P('3. {}'.format(data_growth_business.index[17]),
                       style={'textAlign': 'center',
                              'color': 'orange',
                              'fontSize': 13,
                              'margin-top': '-10px'})
            ], className='create_container2 two columns', style={'height': '500px'}),

            html.Div([
                # 종사자 수 성장률 그래프
                dcc.Graph(figure=fig_num, config={'displayModeBar': 'hover'},
                          style={'height': '450px'})
            ], className='create_container2 four columns', style={'height': '500px'}),

            html.Div([
                html.H6(children="종사자 수 성장률 상/하위",
                        style={'textAlign': 'center',
                               'color': 'white'}),
                html.H5(children="성장률 상위 3순위",
                        style={'textAlign': 'center',
                               'color': 'white'}),
                html.P('1. {}'.format(data_growth_num.index[0]),
                       style={'textAlign': 'center',
                              'color': 'orange',
                              'fontSize': 13,
                              'margin-top': '-10px'}),
                html.P('2. {}'.format(data_growth_num.index[1]),
                       style={'textAlign': 'center',
                              'color': 'orange',
                              'fontSize': 13,
                              'margin-top': '-10px'}),
                html.P('3. {}'.format(data_growth_num.index[2]),
                       style={'textAlign': 'center',
                              'color': 'orange',
                              'fontSize': 13,
                              'margin-top': '-10px'}),
                html.H5(children="성장률 하위 3순위",
                        style={'textAlign': 'center',
                               'color': 'white'}),
                html.P('1. {}'.format(data_growth_num.index[19]),
                       style={'textAlign': 'center',
                              'color': 'orange',
                              'fontSize': 13,
                              'margin-top': '-10px'}),
                html.P('2. {}'.format(data_growth_num.index[18]),
                       style={'textAlign': 'center',
                              'color': 'orange',
                              'fontSize': 13,
                              'margin-top': '-10px'}),
                html.P('3. {}'.format(data_growth_num.index[17]),
                       style={'textAlign': 'center',
                              'color': 'orange',
                              'fontSize': 13,
                              'margin-top': '-10px'})
            ], className='create_container2 two columns', style={'height': '500px'}),

        ]),
        html.Div([
            html.H4(children='인천시 산업별 매출액 증가율',
                    style={'textAlign': 'center',
                           'color': '#FFF'}),
        ], className='half column'),
        html.Div([
            html.P('년도 선택',className='fix_label',style={'textAlign':'center','color':'white'}),
            dcc.Dropdown(id='select_year',
                         options=[{'label':'2016','value':'2016'},
                                  {'label':'2017','value':'2017'},
                                  {'label':'2018','value':'2018'},
                                  {'label':'2019','value':'2019'},],
                         multi=False,
                         searchable=True,
                         value='2016',
                         placeholder='Select Year',
                         className='dcc_compon'),
            html.P('그래프 종류 선택',className='fix_label',style={'textAlign':'center','color':'white'}),
            dcc.Dropdown(id='select_menu',
                         options=[{'label':'사업체 수','value':'사업체수'},
                                  {'label':'종사자 수','value':'종사자수'},
                                  {'label':'매출액','value':'매출액'}],
                         multi=False,
                         searchable=True,
                         value='사업체수',
                         placeholder='Select Menu',
                         className='dcc_compon'),
            html.P('회귀 분석', className='fix_label', style={'textAlign': 'center', 'color': 'white'}),
            html.H6('(사업체 수,종사자 수)', style={'textAlign': 'center', 'color': 'white'}),
            html.P('매출액 설명률', className='fix_label', style={'textAlign': 'center', 'color': 'white'}),
            html.P(id='text_1', className='fix_label', style={'textAlign': 'center', 'color': 'orange'}),

        ],className='create_container2 two columns',style={'height':'480px'}),
        html.Div([
            dcc.Graph(id='total_bar', config={'displayModeBar': 'hover'})
        ], className='create_container2 ten columns'),
        html.Div([
            dcc.Graph(id='heat_map')
        ], className='create_container2 four columns'),
        html.Div([
            dcc.Graph(id='increase_bar', config={'displayModeBar': 'hover'})
        ], className='create_container2 eight columns'),
        html.Div([

            html.Div([
                dcc.Graph(id='predict_bar', config={'displayModeBar': 'hover'})
            ], className='create_container2 twelve columns'),\
        ], className='row flex display'),
    ], className='row flex display'),
], id='mainContainer', style={'display': 'flex', 'flex-direction': 'column'})

# 종사자/사업체 수 전체 비교 그래프
@app.callback(
    Output('total_graph', 'figure'),
    [Input('num_or_business', 'value')]
)
def update_graph(value):
    fig = go.Figure()
    if value == 'business':
        for i in range(0, 20):
            fig.add_trace(go.Scatter(x=output_business.index, y=output_business[output_business.columns[i]].values,
                                      name=output_num.columns[i]))

        fig.update_layout(title={'text': "종사자 수/사업체 수 전체 비교 그래프",
                                 'y': 0.99, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                          titlefont={'color': 'white',
                                     'size': 20},
                          font=dict(family='sans-serif',
                          color='white',
                          size=15),
                          hovermode='closest',
                          paper_bgcolor='#607178',
                          plot_bgcolor='#607178',
                          margin=dict(t=40, r=0),
                          xaxis=dict(title='<b></b>',
                                     color='white',
                                     showline=False,
                                     showgrid=False,
                                     showticklabels=True,
                                     linecolor='white',
                                     linewidth=1,
                                     ticks='outside',
                                     tickfont=dict(
                                         family='Aerial', color='white',size=12)),
                          yaxis=dict(title='<b></b>',
                                     color='white',
                                     showline=False,
                                     showgrid=False,
                                     showticklabels=True,
                                     linecolor='white',
                                     linewidth=1,
                                     ticks='outside',
                                     tickfont=dict(
                                         family='Aerial',color='white',size=12))
                          )

        return fig
    else:
        for i in range(0, 20):
            fig.add_trace(go.Scatter(x=output_num.index, y=output_num[output_num.columns[i]].values,
                                      name=output_num.columns[i]))

            fig.update_layout(title={'text': "종사자 수/사업체 수 비교 그래프",
                                     'y': 0.99, 'x': 0.5, 'xanchor': 'center', 'yanchor': 'top'},
                              titlefont={'color': 'white',
                                         'size': 12},
                              font=dict(family='sans-serif',
                                        color='white',
                                        size=15),
                              hovermode='closest',
                              paper_bgcolor='#607178',
                              plot_bgcolor='#607178',
                              margin=dict(t=40, r=0),
                              xaxis=dict(title='<b></b>',
                                         color='white',
                                         showline=False,
                                         showgrid=False,
                                         showticklabels=True,
                                         linecolor='white',
                                         linewidth=1,
                                         ticks='outside',
                                         tickfont=dict(
                                             family='Aerial', color='white', size=12)),
                              yaxis=dict(title='<b></b>',
                                         color='white',
                                         showline=False,
                                         showgrid=False,
                                         showticklabels=True,
                                         linecolor='white',
                                         linewidth=1,
                                         ticks='outside',
                                         tickfont=dict(
                                             family='Aerial', color='white', size=12))
                              )

        return fig

# 산업별 상관관계 계수
@app.callback(
    Output('text1', 'children'),
    [Input('dropdown_business', 'value')])
def update_text(value):
    cor_kind= np.corrcoef(output_business[output_business.columns[value]].values, output_num[output_num.columns[value]].values)
    return [
        html.P("{} 종사자/사업체 수 상관관계".format(output_business.columns[value]), style={'textAlign': 'center', 'color': 'white'}),
        html.P(round(cor_kind[1, 0], 4), style={'textAlign': 'center', 'color': 'orange',
                                                'fontSize': 15, 'margin-top': '-10px'}),
    ]

# 산업별 비교 그래프
@app.callback(
    Output('compare_graph', 'figure'),
    [Input('dropdown_business', 'value')])
def update_graph(value):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=output_business.index,
        y=output_business[output_business.columns[value]].values,
        name='사업체 수'))

    fig.add_trace(go.Scatter(
        x=output_num.index,
        y=output_num[output_num.columns[value]].values,
        name='종사자 수'))
    fig.update_layout(
        title={'text': "종사자 수/사업체 수 비교 그래프",
               'y': 0.99,
               'x': 0.5,
               'xanchor': 'center',
               'yanchor': 'top'},
        titlefont={'color': 'white',
                   'size': 12},
        font=dict(family='sans-serif',
                  color='white',
                  size=15),
        hovermode='closest',
        paper_bgcolor='#607178',
        plot_bgcolor='#607178',
        margin=dict(t=40, r=0),
        xaxis=dict(title='<b></b>',
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
        yaxis=dict(title='<b></b>',
                   color='white',
                   showline=False,
                   showgrid=False,
                   showticklabels=True,
                   linecolor='white',
                   linewidth=1,
                   ticks='outside',
                   tickfont=dict(
                       family='Aerial',
                       color='white',
                       size=12
                   )
                   )

    )

    return fig

@app.callback(Output('total_bar','figure'),
              [Input('select_year','value'),
               Input('select_menu','value')])
def update_graph(select_year,select_menu):
    x = main_data['산업별']
    y = main_data[select_year + select_menu]
    return {
        'data': [
            go.Bar(
                x=x,y=y,
                text=y,
                texttemplate='%{text:,.0f}',
                textposition='auto',
                name=select_menu,
                marker=dict(color='#AC99C1'),
                hoverinfo='text',
                hovertext=
                '<b>산업</b>: ' + x.astype(str) + '<br>' +
                '<b>'+select_menu+'</b>: ' + [f'{x:,.0f}' for x in y] + '<br>'
            ),

        ],
        'layout': go.Layout(
            plot_bgcolor='#607178',
            paper_bgcolor='#607178',
            barmode='group',
            title={'text': select_year + '년 ' + select_menu,
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 20},
            font=dict(family='sans-serif', color='white', size=12),
            margin=dict(r=0),
            hovermode='closest',
            legend={'orientation': 'h',
                    'bgcolor': 'white',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            xaxis=dict(title='<b></b>',
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
            yaxis=dict(title='<b>사업체 수, 종사자 수, 매출액</b>',
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
@app.callback(Output('increase_bar','figure'),
              [Input('select_year','value'),
               Input('select_menu','value')])
def update_graph(select_year,select_menu):
    x = main_data['산업별']
    if select_year =='2016':
        select_year = '2017'
    y = main_data[select_year + select_menu + '증가율']
    mean = y.mean()
    a = copy.deepcopy(y)
    a[:] = mean
    return {
        'data': [
            go.Line(
                x=x, y=a,name='Mean'
            ),
            go.Bar(
                x=x,y=y,
                text=y,
                texttemplate='%{text:,.0f}',
                textposition='auto',
                name=select_menu,
                marker=dict(color='#98fb98'),
                hoverinfo='text',
                hovertext=
                '<b>산업</b>: ' + x.astype(str) + '<br>' +
                '<b>'+select_menu+'</b>: ' + [f'{x:,.0f}' for x in y] + '<br>'
            ),

        ],
        'layout': go.Layout(
            plot_bgcolor='#607178',
            paper_bgcolor='#607178',
            barmode='group',
            title={'text': select_year + '년 ' + select_menu + ' 증가율',
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 20},
            font=dict(family='sans-serif', color='white', size=12),
            margin=dict(r=0),
            hovermode='closest',
            legend={'orientation': 'h',
                    'bgcolor': '#607178',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            xaxis=dict(title='<b></b>',
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
            yaxis=dict(title='<b>사업체 증가율, 종사자 증가율, 매출액 증가율</b>',
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


@app.callback(
    Output('heat_map', 'figure'),
    [Input('select_year', 'value')])
def update_graph(select_year):
    df = main_data.loc[:,[select_year+'사업체수',select_year+'종사자수',select_year+'매출액']]
    cor = df.corr(method='pearson')
    cor_z = [[cor.iloc[0,0],cor.iloc[0,1],cor.iloc[0,2]],
             [cor.iloc[1,0],cor.iloc[1,1],cor.iloc[1,2]],
             [cor.iloc[2,0],cor.iloc[2,1],cor.iloc[2,2]]]
    return {
        'data': [go.Heatmap(
            z=cor.values,
            x=cor.index.values,
            y=cor.columns.values,
            type='heatmap',
            colorscale='RdBu'
        )],
        'layout': go.Layout(
            plot_bgcolor='#607178',
            paper_bgcolor='#607178',
            title={'text': select_year + '년 ' + ' 히트맵',
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 20},
            font=dict(family='sans-serif', color='white', size=12)
        )
    }

@app.callback(
    Output('text_1', 'children'),
    [Input('select_year', 'value')])
def update_output_p(select_year):
    xxx = data_original[[select_year + '사업체수', select_year + '종사자수']]
    yyy = data_original[[select_year + '매출액']]
    x_train, x_test, y_train, y_test = train_test_split(xxx, yyy, train_size=0.8, test_size=0.2)
    mlr = LinearRegression()
    mlr.fit(x_train, y_train)
    result = mlr.score(x_train, y_train)
    result = round((result * 100),2)
    return '{}%'.format(result)

@app.callback(Output('predict_bar','figure'),
              [Input('select_year','value')])
def update_graph(select_year):
    xxx = main_data[[select_year + '사업체수', select_year + '종사자수']]
    yyy = main_data[[select_year + '매출액']]
    x_train, x_test, y_train, y_test = train_test_split(xxx, yyy, train_size=0.8, test_size=0.2)
    mlr = LinearRegression()
    mlr.fit(x_train, y_train)
    a = []
    for i in range(0, len(xxx)):
        my_slaes = [[xxx.iloc[i, :][0], xxx.iloc[i, :][1]]]
        my_predict = mlr.predict(my_slaes)
        a.append(my_predict[0][0])

    x = main_data['산업별']
    y = main_data[select_year +'매출액']
    print(a)
    print(y)
    return {
        'data': [
            go.Bar(
                x=x,y=y,
                text=y,
                texttemplate='%{text:,.0f}',
                textposition='auto',
                name='매출액',
                marker=dict(color='#E1B4D3'),
                hoverinfo='text',
                hovertext=
                '<b>산업</b>: ' + x.astype(str) + '<br>'
            ),
            go.Bar(
                x=x, y=a,
                text=a,
                texttemplate='%{text:,.0f}',
                textposition='auto',
                name='예상매출액',
                marker=dict(color='#AEDDEF'),
                hoverinfo='text',
                hovertext=
                '<b>산업</b>: ' + x.astype(str) + '<br>'
            ),

        ],
        'layout': go.Layout(
            plot_bgcolor='#607178',
            paper_bgcolor='#607178',
            barmode='group',
            title={'text': select_year + '년 ' + '사업체 수와 종사자 수로 매출액 회귀 예측',
                   'y': 0.93,
                   'x': 0.5,
                   'xanchor': 'center',
                   'yanchor': 'top'},
            titlefont={'color': 'white',
                       'size': 20},
            font=dict(family='sans-serif', color='white', size=12),
            margin=dict(r=0),
            hovermode='closest',
            legend={'orientation': 'h',
                    'bgcolor': '#607178',
                    'xanchor': 'center', 'x': 0.5, 'y': -0.7},
            xaxis=dict(title='산업 종류',
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
            yaxis=dict(title='<b>매출액, 예상매출액</b>',
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

if __name__ == '__main__':
    app.run_server(debug=False)
