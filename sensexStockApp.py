import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import yfinance as yf

st.title('BSE SENSEX App')

st.markdown("""
This app retrieves the list of the **BSE SENSEX** (from Wikipedia) and its corresponding **stock closing price** (year-to-date)!
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn
* **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_BSE_SENSEX_companies).
""")

st.sidebar.header('User Input Features')


#Web scraping of the list of sensex companies
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_BSE_SENSEX_companies'
    html = pd.read_html(url, header = 0)
    df = html[0]
    return df

#Loading the data into df, separated by sectors
df = load_data()
sector = df.groupby('Sector')

sorted_sector_unique = sorted( df['Sector'].unique() )
selected_sector = st.sidebar.multiselect('Sector', sorted_sector_unique, sorted_sector_unique, help = 'Select the various sectors for comparing stock prices')

df_selected_sector = df[ (df['Sector'].isin(selected_sector)) ]

st.header('Display Companies in Selected Sector')
st.write('Data Dimension: ' + str(df_selected_sector.shape[0]) + ' rows and ' + str(df_selected_sector.shape[1]) + ' columns.')
st.dataframe(df_selected_sector)

data = yf.download(
        tickers = list(df_selected_sector[:10].Symbol),
        period = "ytd",
        interval = "1d",
        group_by = 'ticker',
        auto_adjust = True,
        prepost = True,
        threads = True,
        proxy = None
    )


def price_plot(symbol):
    df = pd.DataFrame(data[symbol].Close)
    df['Date'] = df.index
    #plt.fill_between(df.Date, df.Close, color='skyblue', alpha=0.3)
    x = df.Date
    y = df.Close
    ax = plt.axes()
    plt.plot(x, y, color='skyblue', alpha=1)
    plt.xticks(rotation=90)
    plt.title(symbol, fontweight='bold')
    plt.xlabel('Date', fontweight='bold')
    plt.ylabel('Closing Price', fontweight='bold')
    return st.pyplot()

num_company = st.sidebar.slider('Number of Companies', 1, 10)

st.set_option('deprecation.showPyplotGlobalUse', False)

#if st.button('Show Plots'):
st.header('Stock Closing Price')
for i in list(df_selected_sector.Symbol)[:num_company]:
    price_plot(i)