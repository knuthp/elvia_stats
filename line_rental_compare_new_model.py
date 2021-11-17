import altair as alt
import pandas as pd
import streamlit as st


from elvia_stats import metervalueapi

st.title("2022 Norwegian Power Consumption Line Rental Models")


@st.cache
def load_data():
    return metervalueapi.get_metervalues(2021)


data_load_state = st.text("Loading data...")
json = load_data()
data_load_state.text("Loading data...done!")

df = pd.json_normalize(
    json["meteringpoints"][0], record_path=["metervalue", "timeSeries"]
)
df["startTimeStr"] = df["startTime"]
df["startTime"] = pd.to_datetime(df["startTime"], utc=True).dt.tz_convert("Europe/Oslo")
df["endTime"] = pd.to_datetime(df["endTime"], utc=True).dt.tz_convert("Europe/Oslo")
df["hour"] = df["startTime"].dt.hour
df["weekday"] = df["startTime"].dt.weekday
df["date"] = df["startTime"].dt.date.astype(str)
df["month"] = df["startTime"].dt.month

data_load_state.text("Preparing data...done!")


df_max_per_month = df[["startTime", "value"]].groupby(by=df["startTime"].dt.month).max()
st.header("Max consumption per hour per month")
# st.write(df_max_per_month)

chart_max_month = (
    alt.Chart(df_max_per_month)
    .mark_bar()
    .encode(
        alt.X("month(startTime):O", title="Month"),
        alt.Y("value", title="Max kWh per hour", scale=alt.Scale(zero=False)),
        alt.Tooltip("value"),
    )
)
st.write(chart_max_month)
