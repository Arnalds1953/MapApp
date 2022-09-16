import pandas as pd           # pip install pandas openpyxl
import plotly.express as px   # pip install plotly-express
import streamlit as st        # pip install streamlit
import json

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Select Sales Dashboard", page_icon=":bar_chart:", layout="wide")

df1 = pd.read_excel('D:/Streamlit/data/kadehome.xlsx')
# df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
df = df1.dropna()
df.head(3)

st.sidebar.header("选择供应商名称")
apply = st.sidebar.selectbox(
    "选择供应商", 
    options=df['供应商编码'].unique(),
    index=0, 
    key=None, 
    help=None, 
    on_change=None, 
    args=None, 
    kwargs=None,
    disabled=False
)

df_selection = df.query(
    "供应商编码 == @apply"
)
# SALES BY PRODUCT LINE [BAR CHART]
sales_by_product_line = (
    df_selection.groupby(["平台SKU"],as_index=False)["总销售额"].sum()
)
fig_product_sales = px.bar(
    sales_by_product_line,
    x="总销售额",
    y='平台SKU',
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

st.plotly_chart(fig_product_sales,use_container_width=True)


file = open('D:/Streamlit/data/features.geojson','r',encoding='utf-8')
counties = json.load(file)
df = pd.read_excel('D:/Streamlit/data/US销售数据.xlsx')
px.set_mapbox_access_token(token='pk.eyJ1IjoiYXJuYWxkczE5NTMiLCJhIjoiY2w4NDg1NXFrMGJxNzN5cGNhMXJsd3dvaSJ9.ToNjfVJdez4EspCamoUNOA')
fig = px.choropleth_mapbox(df, geojson=counties, locations='地图名称', color='订单数量',
                           color_continuous_scale="Viridis",
                           range_color=(0, 200),
                           mapbox_style="light",
                           zoom=3, center = {"lat": 37.0902, "lon": -95.7129},
                           opacity=0.5,
                           labels={'unemp':'unemployment rate'}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig,use_container_width=True)