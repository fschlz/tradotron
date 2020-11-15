# TRADOTRON 🤖📈

A super simple dashboard app to display stock prices over time.

You can also display the rolling mean for up to a year based on the closing price.

Tickers you display will be saved in `./tradotron/resources/preferences.json`, so you don't have to type them in every time.

The underlying data is pulled from [Yahoo! Finance](https://finance.yahoo.com/) with the `yfinance` package and there you can find Ticker handles to plot.

The dashboard is built with `plotly` & `ipywidgets`.

Feel free to use this for your own stuff.
