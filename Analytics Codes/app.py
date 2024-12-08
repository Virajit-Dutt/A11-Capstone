from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import plotly.express as px
import json

app = Flask(__name__)

df = pd.read_excel('trade_year_country.xlsx')

@app.route('/')
def index():
    countries = df['COUNTRY_NAME'].unique()
    indicators = df['INDICATOR_NAME'].unique()
    regions = df['REGION'].unique()
    income_groups = df['INCOME_GROUP'].unique()
    return render_template('index.html', countries=countries, indicators=indicators, regions=regions, income_groups=income_groups)

@app.route('/cnt_trade_plot', methods=['POST'])
def cnt_trade_plot():
    selected_country = request.form['country']
    selected_indicator = request.form['indicator']

    filtered_data = df[
        (df['COUNTRY_NAME'] == selected_country) &
        (df['INDICATOR_NAME'] == selected_indicator)
    ]

    fig = px.line(
        filtered_data,
        x='YEAR',
        y='TRADE_VALUE',
        title=f'TRADE_VALUE for {selected_country} ({selected_indicator})',
        labels={'TRADE_VALUE': 'Trade Value (%)', 'YEAR': 'Year'}
    )

    fig_html = fig.to_html(full_html=False)

    return render_template('cnt_trade_plot.html', fig_html=fig_html)

@app.route('/decade_plot', methods=['POST'])
def decade_plot():
    selected_country = request.form['country_decade']
    selected_indicator = request.form['indicator_decade']

    filtered_data_decade = df[(df['COUNTRY_NAME'] == selected_country) & (df['INDICATOR_NAME'] == selected_indicator)]

    filtered_data_decade = filtered_data_decade[['TRADE_VALUE', 'DECADE']]

    filtered_data_decade = filtered_data_decade.dropna(subset=['TRADE_VALUE'])

    grouped_data_decade = filtered_data_decade.groupby('DECADE').agg({'TRADE_VALUE': 'mean'}).reset_index()

    if grouped_data_decade.empty:
        return render_template('error.html', message="No data available for the selected country and indicator.")

    fig_decade = px.bar(
        grouped_data_decade,
        x='DECADE',
        y='TRADE_VALUE',
        title=f'TRADE_VALUE for {selected_country} ({selected_indicator}) by Decade',
        labels={'TRADE_VALUE': 'Trade Value (%)', 'DECADE': 'Decade'},
        color='DECADE',
        template='plotly_dark'
    )

    graph_html_decade = fig_decade.to_html(full_html=False)

    return render_template('decade_plot.html', fig_html=graph_html_decade)

@app.route('/region_year_plot', methods=['POST'])
def region_year_plot():
    selected_region = request.form['region_year']
    selected_indicator = request.form['indicator_year']

    filtered_data_region_year = df[(df['REGION'] == selected_region) & (df['INDICATOR_NAME'] == selected_indicator)]

    filtered_data_region_year = filtered_data_region_year[['YEAR', 'REGION', 'TRADE_VALUE']]

    grouped_data_region_year = filtered_data_region_year.groupby(['YEAR', 'REGION']).agg({'TRADE_VALUE': 'mean'}).reset_index()

    fig_region_year = px.line(
        grouped_data_region_year,
        x='YEAR',
        y='TRADE_VALUE',
        color='REGION',
        title=f'Comparison of TRADE_VALUE by Region for {selected_indicator} over Years',
        labels={'TRADE_VALUE': 'Trade Value (%)', 'YEAR': 'Year'},
        markers=True
    )

    graph_html_region_year = fig_region_year.to_html(full_html=False)

    return render_template('region_year_plot.html', fig_html=graph_html_region_year)

@app.route('/income_year_plot', methods=['POST'])
def plot_income_group_year():
    selected_income_group = request.form['income_year']
    selected_indicator = request.form['indicator_year']

    filtered_data_income_group_year = df[(df['INCOME_GROUP'] == selected_income_group) & (df['INDICATOR_NAME'] == selected_indicator)]

    filtered_data_income_group_year = filtered_data_income_group_year[['YEAR', 'INCOME_GROUP', 'TRADE_VALUE']]

    grouped_data_income_group_year = filtered_data_income_group_year.groupby(['YEAR', 'INCOME_GROUP']).agg({'TRADE_VALUE': 'mean'}).reset_index()

    if grouped_data_income_group_year.empty:
        return render_template('error.html', message="No data available for the selected income group and indicator.")

    fig_income_group_year = px.line(
        grouped_data_income_group_year,
        x='YEAR',
        y='TRADE_VALUE',
        color='INCOME_GROUP',
        title=f'Comparison of TRADE_VALUE by Income Group for {selected_indicator} over Years',
        labels={'TRADE_VALUE': 'Trade Value (%)', 'YEAR': 'Year'},
        markers=True
    )

    graph_html_income_group_year = fig_income_group_year.to_html(full_html=False)

    return render_template('income_year_plot.html', fig_html=graph_html_income_group_year)



if __name__ == '__main__':
    app.run(debug=True)
