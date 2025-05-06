
import streamlit as st

# Set page configuration (title, icon, layout) and apply a custom theme.
st.set_page_config(
    page_title="Stock Performance Analyzer",
    page_icon="📈",
    layout="wide"
)


# Title of the app and an introduction (written to the main page, not sidebar).
st.title("📊 Interactive Stock Performance Analyzer")
st.markdown(
    "This interactive tool helps you prepare for finance interviews by analyzing stock performance, "
    "clustering similar stocks, and computing key metrics like Sharpe ratio, Beta/Alpha, and valuation multiples. "
    "Use the sidebar to configure your analysis and explore the results below."
)
st.write("""
**Analyze and compare the performance of publicly listed companies.**
Select companies and a date range to visualize their stock price trends,
see how they correlate with each other, and even cluster them into groups
based on risk and return. This tool helps identify which companies behave
similarly in the market and how they differ in volatility and growth.
""")

# Sidebar inputs for user interaction.
st.sidebar.header("Input Options")
st.sidebar.markdown(
    "Use these inputs to select the companies, time period, clustering parameters, and benchmark for your analysis."
)
st.sidebar.write("Select the dataset and parameters for analysis:")

st.sidebar.markdown("### 1️⃣ Company Selection\nChoose one or more stock tickers to analyze. At least one ticker is required.")
# 1. Company Selection:
# Provide a list of example stock tickers for user to choose from.
# We include a diverse set of companies across industries for meaningful comparisons.
available_tickers = [
    "AAPL",  # Apple Inc.
    "MSFT",  # Microsoft Corp.
    "GOOGL", # Alphabet Inc.
    "AMZN",  # Amazon.com Inc.
    "TSLA",  # Tesla Inc.
    "JPM",   # JPMorgan Chase & Co.
    "JNJ",   # Johnson & Johnson
    "XOM",   # Exxon Mobil Corp.
    "WMT",   # Walmart Inc.
    "NVDA",  # NVIDIA Corp.
    "NFLX",  # Netflix, Inc.
    "META",  # Meta Platforms (Facebook)
    "BAC",   # Bank of America Corp.
    "PG",    # Procter & Gamble Co.
    "DIS"    # Walt Disney Co.
]
# Allow multiple selection of tickers. Provide some defaults (e.g., a few tech and non-tech).
selected_tickers = st.sidebar.multiselect(
    "Select one or more stock tickers to analyze:",
    options=available_tickers,
    default=["AAPL", "MSFT", "GOOGL", "AMZN"]  # default selection
)
# Ensure at least one ticker is selected, else show a warning.
if len(selected_tickers) == 0:
    st.sidebar.error("Please select at least one company.")
    st.stop()

st.sidebar.markdown("### 2️⃣ Date Range Selection\nSelect the start and end dates to define the historical period for analysis.")
# 2. Date Range Selection:
# Use two date inputs (or a single range slider for simplicity) for start and end dates.
# Here we use st.date_input for start and end.
from datetime import datetime, timedelta
# Default date range: last 1 year from today.
default_end = datetime.today().date()
default_start = default_end - timedelta(days=365)
start_date = st.sidebar.date_input("Start date:", value=default_start)
end_date = st.sidebar.date_input("End date:", value=default_end)
if start_date >= end_date:
    st.sidebar.error("Start date must be before end date.")
    st.stop()

st.sidebar.markdown("### 3️⃣ Clustering Parameters\nSelect how many clusters to form based on risk-return profiles (2–6).")
# 3. Cluster Count Selection (for ML KMeans):
# Allow user to choose how many clusters to form for grouping similar stocks.
num_clusters = st.sidebar.slider(
    "Number of clusters (for grouping stocks):",
    min_value=2, max_value=6, value=3, step=1
)
# (We set a minimum of 2 clusters because a single cluster isn't very interesting for grouping.)

st.sidebar.markdown("### 4️⃣ Benchmark & Risk-Free Rate\nEnter a benchmark index ticker (e.g., ^GSPC) and an annual risk-free rate for computing Beta, Alpha, and Sharpe ratio.")
# Benchmark selection for regression analysis (e.g., S&P 500)
benchmark_ticker = st.sidebar.text_input(
    "Benchmark index ticker (e.g., ^GSPC):", value="^GSPC"
)
# Risk-free rate input for Sharpe ratio (annual)
risk_free_rate_annual = st.sidebar.number_input(
    "Risk-free rate (annual %, e.g., 2.5):", min_value=0.0, max_value=10.0, value=0.0, step=0.1
) / 100.0

# 4. Optional: File Uploader for user dataset (not mandatory for this scenario, but could be an extension).
uploaded_file = st.sidebar.file_uploader(
    "Or upload your own dataset (CSV) for analysis:",
    type=['csv'],
    help="You can upload a CSV with columns like Date and price data to analyze your own data."
)
use_uploaded_data = False
if uploaded_file is not None:
    # If a file is uploaded, we could parse it into a DataFrame.
    # For demonstration, we expect the CSV to have a 'Date' column and one or more price columns.
    try:
        user_df = pd.read_csv(uploaded_file)
        # Basic check: require a 'Date' column
        if 'Date' in user_df.columns:
            user_df['Date'] = pd.to_datetime(user_df['Date'])
            user_df.set_index('Date', inplace=True)
            use_uploaded_data = True
        else:
            st.sidebar.error("Uploaded CSV must have a 'Date' column.")
    except Exception as e:
        st.sidebar.error(f"Error reading CSV: {e}")
        use_uploaded_data = False

# Inform the user what data is being used (either live data from Yahoo or their uploaded file)
if use_uploaded_data:
    st.write("Using uploaded dataset for analysis.")
else:
    st.write(f"Fetching historical stock data from Yahoo Finance for: {', '.join(selected_tickers)}.")

# Data Loading and Caching
import pandas as pd

@st.cache_data(ttl=3600)
def load_stock_data(tickers, start_date, end_date):
    """
    Fetch historical stock data (OHLCV) for given tickers and date range from Yahoo Finance.

    Parameters:
        tickers (list[str]): List of stock ticker symbols.
        start_date (datetime.date): Start date for historical data.
        end_date (datetime.date): End date for historical data.
    Returns:
        pandas.DataFrame: DataFrame containing the historical data.
                          If multiple tickers, returns a MultiIndex DataFrame (Ticker x [Open, High, Low, Close, Adj Close, Volume]).
                          If single ticker, returns a DataFrame with columns [Open, High, Low, Close, Adj Close, Volume].
    """
    import yfinance as yf
    # yfinance will fetch daily historical data for the tickers.
    # We set auto_adjust=False to get raw prices and an explicit 'Adj Close' column for adjusted close prices.
    # We disable progress printout by setting progress=False if available (in newer yfinance).
    try:
        data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=False, progress=False)
    except TypeError:
        # In case older yfinance doesn't support progress param, call without it.
        data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=False)
    return data

# Load data (either from Yahoo or use uploaded data if provided)
if use_uploaded_data:
    data = user_df.copy()
    # If uploaded data, assume it is already in a similar format (Date index, columns as tickers or series).
    # We'll treat each numeric column (besides Date) as a separate series for analysis.
    # For simplicity, we proceed if so.
    stock_prices = data  # We'll consider this as equivalent to Adj Close data.
    selected_tickers = list(stock_prices.columns)
else:
    # Use Yahoo Finance data for selected tickers
    data = load_stock_data(selected_tickers, start_date, end_date)
    # The returned `data` can have different shapes depending on number of tickers.
    # We need to extract the Adjusted Close prices for each ticker for analysis, since that reflects true performance (adjusted for splits/dividends).
    if isinstance(data.columns, pd.MultiIndex):
        # If multiple tickers, data columns are MultiIndex: first level ticker, second level price attribute.
        # Extract the 'Adj Close' level for all tickers, resulting in a DataFrame of adjusted close prices for each ticker.
        stock_prices = data['Adj Close'].copy()
    else:
        # If only one ticker, data is DataFrame with columns including 'Adj Close'.
        stock_prices = data[['Adj Close']].copy()
        # Rename the column to the ticker name for consistency
        stock_name = selected_tickers[0] if isinstance(selected_tickers, list) else selected_tickers
        stock_prices.columns = [stock_name]
# Ensure the DataFrame index is of datetime type (it should be from yfinance, but double-check or convert if needed).
stock_prices.index = pd.to_datetime(stock_prices.index)

# Basic data sanity check and handling:
if stock_prices.isnull().values.any():
    # If any missing values (e.g., no trading data on some days, or if a ticker didn't exist for part of range), fill or drop as appropriate.
    # We forward-fill missing prices to handle non-trading days or missing data points (assuming markets closed).
    stock_prices.ffill(inplace=True)
# If after filling there are still NaNs (e.g., at very start if a stock didn't exist yet), drop those dates:
stock_prices.dropna(axis=0, how='all', inplace=True)

# Now `stock_prices` is a DataFrame where each column is the adjusted price of a selected stock over time.
st.subheader("Raw Data Preview")
st.write("Below is a preview of the adjusted closing price data for the selected period:")
st.dataframe(stock_prices.head(10))  # show first 10 rows as a sample
st.write(
    "Above is a preview of the adjusted closing prices for your selected stocks. "
    "Ensure the data looks correct before proceeding to visualizations."
)

# ---- Visualization 1: Price trend chart ----
st.subheader("Stock Price Performance Over Time")
st.write("This line chart normalizes each stock to 100 at the start date, showing relative performance over time.")
# We will create a line chart of the normalized price trends.
# Normalization: We set each stock's price to 100 at the start date to compare relative growth.
# This way, regardless of their absolute price, we can see how much each grew or fell in percentage terms.
# Compute normalized prices:
norm_prices = stock_prices.div(stock_prices.iloc[0]) * 100.0

# Prepare data for plotting (long format for plotly express).
plot_df = norm_prices.reset_index().melt(id_vars=norm_prices.index.name or 'Date',
                                         var_name='Ticker', value_name='Normalized Price')
# Ensure the date column is named 'Date' for clarity in labels:
if 'index' in plot_df.columns:
    plot_df.rename(columns={'index': 'Date'}, inplace=True)

# Use Plotly for interactive line chart:
import plotly.express as px
fig = px.line(plot_df, x='Date', y='Normalized Price', color='Ticker',
              title="Normalized Stock Price (Start = 100)",
              labels={'Normalized Price': 'Normalized Price (Start=100)', 'Date': 'Date'})
# Enhance the figure (e.g., add a horizontal line at 100 for reference, add tooltip formatting)
fig.add_hline(y=100, line_dash="dot", line_color="gray", annotation_text="Start (100)", annotation_position="bottom right")
fig.update_layout(legend_title_text='Company', hovermode="x unified")
# Display the chart in the Streamlit app:
st.plotly_chart(fig, use_container_width=True)
# The above chart allows the user to hover over dates to see each stock's normalized price, and toggle lines via the legend.

# ---- Visualization 2: Correlation Heatmap ----
st.subheader("Correlation Matrix of Daily Returns")
st.write("This heatmap reveals pairwise correlations of daily returns, helping identify stocks that move together.")
# Calculate daily percentage returns for each stock:
returns = stock_prices.pct_change().dropna()
# Compute correlation matrix:
corr_matrix = returns.corr()
# Use Plotly to display an interactive heatmap of correlation matrix:
fig_corr = px.imshow(corr_matrix, text_auto=".2f", aspect="auto", origin="lower",
                     color_continuous_scale="RdBu", zmin=-1, zmax=1,
                     title="Correlation of Daily Returns")
fig_corr.update_xaxes(side="bottom", tickangle=45)  # show ticker symbols on x-axis at bottom
fig_corr.update_yaxes(tickangle=0)  # keep y-axis labels readable
fig_corr.update_layout(coloraxis_colorbar=dict(title="Correlation"))
st.plotly_chart(fig_corr, use_container_width=True)
# The heatmap uses a red-blue colormap: red for positive correlation, blue for negative.
# We annotated each cell with the correlation value (two decimal places) for clarity.

# ---- Machine Learning: Clustering stocks by performance ----
st.subheader("K-Means Clustering of Stocks (Risk vs Return)")
st.write("Clustering groups stocks with similar total return and volatility characteristics. Adjust cluster count to see different groupings.")
st.write(f"We apply an unsupervised machine learning model (K-Means) to cluster the selected stocks into **{num_clusters}** groups, "
         "based on their **risk and return** characteristics over the chosen period. "
         "Here, we define 'return' as the total percentage change in price over the period, and 'risk' as the volatility (standard deviation of daily returns).")

# Prepare features for clustering:
# Feature 1: Total return (%) over the period for each stock.
total_return = (stock_prices.iloc[-1] / stock_prices.iloc[0] - 1) * 100  # percentage change from first to last day
# Feature 2: Volatility (%) - we take standard deviation of daily returns and convert to percentage.
volatility = returns.std() * 100

# Create a DataFrame of features for each stock:
features_df = pd.DataFrame({
    'Return (%)': total_return,
    'Volatility (%)': volatility
})
# Drop any stocks where return or volatility couldn't be computed (shouldn't happen unless data issues).
features_df.dropna(inplace=True)

# Scale features before clustering (K-Means is distance-based, so it's good to normalize features).
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
X = scaler.fit_transform(features_df[['Return (%)', 'Volatility (%)']])

# Perform K-Means clustering:
from sklearn.cluster import KMeans
kmeans = KMeans(n_clusters=num_clusters, n_init='auto', random_state=42)
cluster_labels = kmeans.fit_predict(X)
features_df['Cluster'] = cluster_labels  # assign cluster labels to each stock

# Evaluate clustering performance using silhouette score (only if more than 1 cluster):
from sklearn.metrics import silhouette_score
# Compute silhouette score only when cluster count is valid (at least 2 clusters and fewer clusters than samples)
if num_clusters > 1 and features_df.shape[0] > num_clusters:
    sil_score = silhouette_score(X, cluster_labels)
    st.write(f"**Silhouette Score** of the clustering: {sil_score:.2f} "
             "(Silhouette score ranges from -1 to 1, where higher is better. Scores above 0 indicate meaningful clustering.)")
else:
    st.warning(
        f"Cannot compute silhouette score: number of clusters ({num_clusters}) "
        f"must be at least 2 and less than the number of stocks ({features_df.shape[0]})."
    )

# Display cluster centers (in original scale) if needed:
# cluster_centers = scaler.inverse_transform(kmeans.cluster_centers_)
# We could show cluster centers for return/volatility, but it's optional.

# Create an interactive scatter plot for clusters:
features_df['Ticker'] = features_df.index  # bring ticker name as a column for plotting
fig_clusters = px.scatter(
    features_df, x='Volatility (%)', y='Return (%)', color=features_df['Cluster'].astype(str),
    text='Ticker', opacity=0.8, size_max=60,
    title="Clusters of Stocks by Risk (Volatility) and Return",
    labels={'color': 'Cluster'}
)
fig_clusters.update_traces(textposition='top center')
fig_clusters.update_layout(legend_title_text='Cluster')
st.plotly_chart(fig_clusters, use_container_width=True)
# The scatter plot shows each stock positioned by its volatility (x-axis) and total return (y-axis).
# Points with the same color belong to the same cluster.
# We also label each point with the ticker symbol for clarity.

# Additionally, let's list the stocks in each cluster for easier interpretation:
st.write("**Cluster Composition:**")
for cluster_num in sorted(features_df['Cluster'].unique()):
    members = features_df[features_df['Cluster'] == cluster_num]['Ticker'].tolist()
    st.write(f"- **Cluster {cluster_num}:** " + ", ".join(members))

# ---- Financial Metrics for Interview Prep ----
st.write(
    "Below are key performance and risk metrics commonly discussed in finance interviews, calculated for each stock."
)
st.subheader("Financial Metrics for Interview Prep")
st.write("Key metrics often discussed in finance interviews: annualized return, volatility, Sharpe ratio, maximum drawdown, and Beta/Alpha relative to a benchmark.")

# Compute annualized return and volatility
trading_days = 252
annual_return = (1 + returns).prod() ** (trading_days / len(returns)) - 1
annual_vol = returns.std() * (trading_days ** 0.5)

# Compute Sharpe ratio
sharpe_ratio = (annual_return - risk_free_rate_annual) / annual_vol

# Compute max drawdown
cum_returns = (1 + returns).cumprod()
running_max = cum_returns.cummax()
drawdown = (cum_returns - running_max) / running_max
max_drawdown = drawdown.min()

# Prepare metrics DataFrame
metrics_df = pd.DataFrame({
    'Annual Return': annual_return,
    'Annual Volatility': annual_vol,
    'Sharpe Ratio': sharpe_ratio,
    'Max Drawdown': max_drawdown
})

# Fetch benchmark data and compute returns
bench_data = load_stock_data(benchmark_ticker, start_date, end_date)
if isinstance(bench_data.columns, pd.MultiIndex):
    bench_prices = bench_data['Adj Close'][benchmark_ticker]
else:
    bench_prices = bench_data['Adj Close']
bench_returns = bench_prices.pct_change().dropna()

# Align returns
aligned = returns.join(bench_returns.rename('Benchmark'), how='inner')

# Compute Beta and Alpha using linear regression
from sklearn.linear_model import LinearRegression
betas = {}
alphas = {}
for ticker in returns.columns:
    y = aligned[ticker].values.reshape(-1, 1)
    x = aligned['Benchmark'].values.reshape(-1, 1)
    model = LinearRegression().fit(x, y)
    betas[ticker] = model.coef_[0][0]
    alphas[ticker] = model.intercept_[0]

metrics_df['Beta'] = pd.Series(betas)
metrics_df['Alpha'] = pd.Series(alphas)

# Round for display
metrics_df = metrics_df.round(4)


# Display metrics table
st.dataframe(metrics_df)

# ---- Valuation Multiples for IB/PE Interview Prep ----
st.write(
    "Common valuation multiples are essential for IB/PE case discussions. We fetch these from market data for your selected tickers."
)
st.subheader("Valuation Multiples for IB/PE Interview Prep")
st.write("Common valuation multiples: P/E (trailing & forward), PEG ratio, P/B ratio, EV/EBITDA, EV/Sales.")

# Fetch fundamental metrics for each ticker
import yfinance as yf
multiples = {}
for ticker in selected_tickers:
    info = yf.Ticker(ticker).info
    multiples[ticker] = {
        'Trailing P/E': info.get('trailingPE', None),
        'Forward P/E': info.get('forwardPE', None),
        'PEG Ratio': info.get('pegRatio', None),
        'Price/Book': info.get('priceToBook', None),
        'EV/EBITDA': info.get('enterpriseToEbitda', None),
        'EV/Sales': info.get('enterpriseToSales', None)
    }

multiples_df = pd.DataFrame(multiples).T
# Round numeric values for display
multiples_df = multiples_df.round(2)
# Display multiples table
st.dataframe(multiples_df)

st.markdown("""
**How to interpret the results:**
- The line chart above shows how each selected stock's price evolved over time (normalized to start at 100 for easy comparison).
  You can visually identify which stocks outperformed others (ending above 100) or underperformed (below 100).
- The correlation matrix indicates which stocks tend to move together. Highly correlated stocks (orange/red) might belong to the same industry or be influenced by similar market factors. Low or negative correlations (blue) suggest the stocks behave differently, which could be useful for diversification.
- The clustering attempts to group stocks with similar risk-return profiles. For example, one cluster might contain high-tech growth stocks with high volatility and high returns, while another cluster might contain stable, lower-volatility stocks with modest returns. This helps in identifying **structural differences**: companies in the same cluster share similar market behavior.
- You can adjust the number of clusters to see if the grouping changes (e.g., more clusters might separate stocks into finer groups).

Use this interactive tool to explore and gain insights into the market behavior of different companies!
""")
