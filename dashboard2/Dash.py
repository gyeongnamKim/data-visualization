import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input,Output
import plotly.graph_objs as go
import pandas as pd
url_confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
url_deaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
url_recovered = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
confirmed = pd.read_csv(url_confirmed)
deaths = pd.read_csv(url_deaths)
recovered = pd.read_csv(url_recovered)
total_confirmed = pd.melt(confirmed,id_vars=['Province/State','Country/Region','Lat','Long'],
                          var_name='date',value_name='confirmed')
total_deaths = pd.melt(deaths,id_vars=['Province/State','Country/Region','Lat','Long'],
                          var_name='date',value_name='deaths')
total_recovered = recovered.melt(id_vars=['Province/State','Country/Region','Lat','Long'],
                          value_vars=recovered.columns[4:],var_name='date',value_name='recovered')
data = pd.merge(total_confirmed,total_deaths,how='left',on=['Province/State','Country/Region','Lat','Long','date'])
data = data.merge(right=total_recovered,how='left',on=['Province/State','Country/Region','Lat','Long','date'])
data['date'] = pd.to_datetime(data['date'])
data['recovered'].fillna(0,inplace=True)
data['active'] = data['confirmed'] - data['deaths'] - data['recovered']
data1 = data.groupby('date')[['confirmed','deaths','recovered','active']].sum().reset_index()
data_list = data[['Country/Region','Lat','Long']]
dict_of_location = data_list.set_index('Country/Region')[['Lat','Long']].T.to_dict('dict')
app = dash.Dash(__name__,meta_tags=[{'name':'viewport','content':'width=device-width'}])
app.layout = html.Div([
    html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('corona-logo-1.jpg'),
                     id = 'corona-image',
                     style={'height':'60px',
                            'width':'auto',
                            'margin-bottom':'25px'})
        ],className='one-third column'),

        html.Div([
            html.Div([
                html.H3('코로나-19',style={'margin-bottom':'0px','color':'white'}),
                html.H5('코로나-19 추적현황',style={'margin-bottom':'0px','color':'white'})
            ])
        ],className='one-half column',id='title'),
        html.Div([
            html.H6('Last Updated: '+str(data['date'].iloc[-1].strftime('%B %d %Y'))+' 00:01 (UTC)',
                    style={'color':'orange'})

        ],className='one-third column', id='title1')
    ],id='header',className='row flex-display',style={'margin-bottom':'25px'}),
    html.Div([
        html.Div([
            html.H6(
                children='Global Cases',
                style={'textAlign':'center',
                       'color':'white'}
            ),
            html.P(f"{data1['confirmed'].iloc[-1]:,.0f}",
                   style={"textAlign":'center',
                          'color':'orange',
                          'fontSize':40}),
            html.P('new: '+f"{data1['confirmed'].iloc[-1] - data1['confirmed'].iloc[-2]:,.0f}"
                   + ' (' + str(round(((data1['confirmed'].iloc[-1] - data1['confirmed'].iloc[-2])/
                                       data1['confirmed'].iloc[-1])*100, 2))+'%)',
                   style={"textAlign":'center',
                          'color':'orange',
                          'fontSize':15,
                          'margin-top':'-18px'})
        ],className='card_container three columns'),

        html.Div([
            html.H6(
                children='Global Death',
                style={'textAlign':'center',
                       'color':'white'}
            ),
            html.P(f"{data1['deaths'].iloc[-1]:,.0f}",
                   style={"textAlign":'center',
                          'color':'#dd1e35',
                          'fontSize':40}),
            html.P('new: '+f"{data1['deaths'].iloc[-1] - data1['deaths'].iloc[-2]:,.0f}"
                   + ' (' + str(round(((data1['deaths'].iloc[-1] - data1['deaths'].iloc[-2])/
                                       data1['deaths'].iloc[-1])*100, 2))+'%)',
                   style={"textAlign":'center',
                          'color':'#dd1e35',
                          'fontSize':15,
                          'margin-top':'-18px'})
        ],className='card_container three columns'),

        html.Div([
            html.H6(
                children='Global Recovered',
                style={'textAlign':'center',
                       'color':'white'}
            ),
            html.P(f"{data1['recovered'].iloc[-1]:,.0f}",
                   style={"textAlign":'center',
                          'color':'green',
                          'fontSize':40}),
            html.P('new: '+f"{data1['recovered'].iloc[-1] - data1['recovered'].iloc[-2]:,.0f}"
                   + ' (' + str(round(((data1['recovered'].iloc[-1] - data1['recovered'].iloc[-2])/
                                       data1['recovered'].iloc[-1])*100, 2))+'%)',
                   style={"textAlign":'center',
                          'color':'green',
                          'fontSize':15,
                          'margin-top':'-18px'})
        ],className='card_container three columns'),

        html.Div([
            html.H6(
                children='Global Active',
                style={'textAlign':'center',
                       'color':'white'}
            ),
            html.P(f"{data1['active'].iloc[-1]:,.0f}",
                   style={"textAlign":'center',
                          'color':'#e55467',
                          'fontSize':40}),
            html.P('new: '+f"{data1['active'].iloc[-1] - data1['active'].iloc[-2]:,.0f}"
                   + ' (' + str(round(((data1['active'].iloc[-1] - data1['active'].iloc[-2])/
                                       data1['active'].iloc[-1])*100, 2))+'%)',
                   style={"textAlign":'center',
                          'color':'#e55467',
                          'fontSize':15,
                          'margin-top':'-18px'})
        ],className='card_container three columns')


    ],className='row flex display'),
    html.Div([
        html.Div([
            html.P('Select Country',className='fix_label',style={'color':'white'}),
            dcc.Dropdown(id='w_countries',
                         multi=False,
                         searchable=True,
                         value='US',
                         placeholder='Select Countries',
                         options=[{'label':c,'value':c} for c in (data['Country/Region'].unique())],
                         className='dcc_compon'),
            html.P("New Cases: " + ' '+ str(data['date'].iloc[-1].strftime('%B %d %Y')),
                   className='fix_label',style={'text-align':'center','color':'white'}),

            dcc.Graph(id='confirmed',config={'displayModeBar':True},className='dcc_compon',
                      style={'margin-top':'20px'}),
            dcc.Graph(id='deaths',config={'displayModeBar':False},className='dcc_compon',
                      style={'margin-top':'20px'}),
            dcc.Graph(id='recovered',config={'displayModeBar':False},className='dcc_compon',
                      style={'margin-top':'20px'}),
            dcc.Graph(id='active',config={'displayModeBar':False},className='dcc_compon',
                      style={'margin-top':'20px'})

        ],className='create_container three columns'),

        html.Div([
            dcc.Graph(id='pie_chart', config={'displayModeBar':'hover'})
        ],className='create_container four columns'),

        html.Div([
            dcc.Graph(id='line_chart',config={'displayModeBar': 'hover'})
        ],className='create_container five columns')
    ],className='row flex display')
],id='mainContainer',style={'display':'flex','flex-direction':'column'})

















@app.callback(Output('confirmed','figure'),
              [Input('w_countries','value')])
def update_confirmed(w_countries):
    data2 = data.groupby(['date','Country/Region']) \
             [['confirmed','deaths','recovered','active']].sum().reset_index()
    value_confirmed = data2[data2['Country/Region'] == w_countries]['confirmed'].iloc[-1] - \
                      data2[data2['Country/Region'] == w_countries]['confirmed'].iloc[-2]
    delta_confirmed = data2[data2['Country/Region'] == w_countries]['confirmed'].iloc[-2] - \
                      data2[data2['Country/Region'] == w_countries]['confirmed'].iloc[-3]
    return  {
        'data':[go.Indicator(
            mode='number+delta',
            value=value_confirmed,
            delta= {'reference':delta_confirmed,
                    'position':'right',
                    'valueformat':',g',
                    'relative':False,
                    'font':{'size':15}},
            number={'valueformat':',',
                    'font':{'size':20}},
            domain={'y':[0,1],'x':[0,1]}
        )],
        'layout':go.Layout(
            title={'text':'New Confirmed',
                   'y':1,
                   'x':0.5,
                   'xanchor':'center',
                   'yanchor':'top'},
            font=dict(color='orange'),
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            height=50
        )
    }

@app.callback(Output('deaths','figure'),
              [Input('w_countries','value')])
def update_confirmed(w_countries):
    data2 = data.groupby(['date','Country/Region']) \
             [['confirmed','deaths','recovered','active']].sum().reset_index()
    value_deaths = data2[data2['Country/Region'] == w_countries]['deaths'].iloc[-1] - \
                      data2[data2['Country/Region'] == w_countries]['deaths'].iloc[-2]
    delta_deaths = data2[data2['Country/Region'] == w_countries]['deaths'].iloc[-2] - \
                      data2[data2['Country/Region'] == w_countries]['deaths'].iloc[-3]
    return  {
        'data':[go.Indicator(
            mode='number+delta',
            value=value_deaths,
            delta= {'reference':delta_deaths,
                    'position':'right',
                    'valueformat':',g',
                    'relative':False,
                    'font':{'size':15}},
            number={'valueformat':',',
                    'font':{'size':20}},
            domain={'y':[0,1],'x':[0,1]}
        )],
        'layout':go.Layout(
            title={'text':'New Death',
                   'y':1,
                   'x':0.5,
                   'xanchor':'center',
                   'yanchor':'top'},
            font=dict(color='#dd1e35'),
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            height=50
        )
    }

@app.callback(Output('recovered','figure'),
              [Input('w_countries','value')])
def update_confirmed(w_countries):
    data2 = data.groupby(['date','Country/Region'])[['confirmed','deaths','recovered','active']].sum().reset_index()
    value_recovered = data2[data2['Country/Region'] == w_countries]['recovered'].iloc[-1] - \
                      data2[data2['Country/Region'] == w_countries]['recovered'].iloc[-2]
    delta_recovered = data2[data2['Country/Region'] == w_countries]['recovered'].iloc[-2] - \
                      data2[data2['Country/Region'] == w_countries]['recovered'].iloc[-3]
    return  {
        'data':[go.Indicator(
            mode='number+delta',
            value=value_recovered,
            delta= {'reference':delta_recovered,
                    'position':'right',
                    'valueformat':',g',
                    'relative':False,
                    'font':{'size':15}},
            number={'valueformat':',',
                    'font':{'size':20}},
            domain={'y':[0,1],'x':[0,1]}
        )],
        'layout':go.Layout(
            title={'text':'New Recovered',
                   'y':1,
                   'x':0.5,
                   'xanchor':'center',
                   'yanchor':'top'},
            font=dict(color='green'),
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            height=50
        )
    }

@app.callback(Output('active','figure'),
              [Input('w_countries','value')])
def update_confirmed(w_countries):
    data2 = data.groupby(['date','Country/Region']) \
             [['confirmed','deaths','recovered','active']].sum().reset_index()
    value_active = data2[data2['Country/Region'] == w_countries]['active'].iloc[-1] - \
                      data2[data2['Country/Region'] == w_countries]['active'].iloc[-2]
    delta_active = data2[data2['Country/Region'] == w_countries]['active'].iloc[-2] - \
                      data2[data2['Country/Region'] == w_countries]['active'].iloc[-3]
    return  {
        'data':[go.Indicator(
            mode='number+delta',
            value=value_active,
            delta= {'reference':delta_active,
                    'position':'right',
                    'valueformat':',g',
                    'relative':False,
                    'font':{'size':15}},
            number={'valueformat':',',
                    'font':{'size':20}},
            domain={'y':[0,1],'x':[0,1]}
        )],
        'layout':go.Layout(
            title={'text':'New Active',
                   'y':1,
                   'x':0.5,
                   'xanchor':'center',
                   'yanchor':'top'},
            font=dict(color='#e55467'),
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            height=50
        )
    }

@app.callback(Output('pie_chart','figure'),
              [Input('w_countries','value')])
def update_graph(w_countries):
    data2 = data.groupby(['date', 'Country/Region']) \
        [['confirmed', 'deaths', 'recovered', 'active']].sum().reset_index()
    confirmed_value = data2[data2['Country/Region'] == w_countries]['confirmed'].iloc[-1]
    deaths_value = data2[data2['Country/Region'] == w_countries]['deaths'].iloc[-1]
    recovered_value = data2[data2['Country/Region'] == w_countries]['recovered'].iloc[-1]
    acrive_value = data2[data2['Country/Region'] == w_countries]['active'].iloc[-1]
    colors=['orange','#dd1e35','green','#e55467']

    return {
        'data' : [go.Pie(
            labels=['Confirmed','Death','Recovered','Active'],
            values=[confirmed_value,deaths_value,recovered_value,acrive_value],
            marker=dict(colors=colors),
            hoverinfo='label+value+percent',
            textinfo='label+value',
            hole=.7,
            rotation=45
        )],

        'layout': go.Layout(
            title={'text':'Total Cases: '+ (w_countries),
                   'y':0.93,
                   'x':0.5,
                   'xanchor':'center',
                   'yanchor':'top'},
            titlefont={'color':'white',
                       'size':20},
            font=dict(family='sans-serif',
                      color='white',
                      size=12),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation':'h',
                    'bgcolor':'#1f2c56',
                    'xanchor':'center','x':0.5,'y':-0.7}
        )
    }
@app.callback(Output('line_chart','figure'),
              [Input('w_countries','value')])
def update_graph(w_countries):
    data2 = data.groupby(['date', 'Country/Region']) \
        [['confirmed', 'deaths', 'recovered', 'active']].sum().reset_index()
    data3 = data2[data2['Country/Region'] == w_countries][['Country/Region','date','confirmed']].reset_index()
    data3['daily confirmed'] = data3['confirmed'] - data3['confirmed'].shift(1)
    data3['Rolling Ave'] = data3['daily confirmed'].rolling(window=7).mean()

    return {
        'data' : [go.Bar(
            x=data3['date'].tail(30),
            y=data3['daily confirmed'].tail(30),
            name='Daily Confirmed Cases',
            marker=dict(color='orange'),
            hoverinfo='text',
            hovertext=
            '<b>Date</b>: ' + data3['date'].tail(30).astype(str) + '<br>' +
            '<b>Daily Confirmed Cases</b>: ' + [f'{x:,.0f}' for x in data3['daily confirmed'].tail(30)] + '<br>' +
            '<b>Country</b>: '+data3['Country/Region'].tail(30).astype(str) + '<br>'
        ),
            go.Scatter(
                x=data3['date'].tail(30),
                y=data3['Rolling Ave'].tail(30),
                mode='lines',
                name='Rolling Average of the last 7 days - daily confirmed cases',
                line=dict(width=3,color='#FF00FF'),
                hoverinfo='text',
                hovertext=
                        '<b>Date</b>: ' + data3['date'].tail(30).astype(str) + '<br>' +
                        '<b>Daily Confirmed Cases</b>: ' + [f'{x:,.0f}' for x in data3['Rolling Ave'].tail(30)] + '<br>'

            )],

        'layout': go.Layout(
            title={'text':'Last 30 Days Daily Confirmed Cases' + (w_countries),
                   'y':0.93,'x':0.5,
                   'xanchor':'center','yanchor':'top'},
            titlefont={'color':'white','size':20},
            font=dict(family='sans-serif',color='white',size=12),
            hovermode='closest',
            paper_bgcolor='#1f2c56',
            plot_bgcolor='#1f2c56',
            legend={'orientation': 'h',
                    'bgcolor':'#1f2c56',
                    'xanchor':'center','x':0.5,'y':-0.7},
            margin=dict(r=0),
            xaxis=dict(title='<b>Date</b>',
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
                           size=12)),
            yaxis=dict(title='<b>Daily Confirmed Cases</b>',
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
                           size=12)
                       )
        )
    }
if __name__ == '__main__':
    app.run_server(debug=False,port=8080,host='127.0.0.1')
