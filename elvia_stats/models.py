""" The models for charging power line rental (nettleie)."""
import pandas as pd


def extract_properties(df: pd.DataFrame) -> pd.DataFrame:
    """ Extracts properties like weekday, hour, month that are used in charge models."""
    df["hour"] = df["startTime"].dt.hour
    df["weekday"] = df["startTime"].dt.weekday
    # df["date"] = df["startTime"].dt.date.astype(str)
    df["month"] = df["startTime"].dt.month
    return df


df_elvia_night_day_variable = pd.DataFrame(
    [
        ["summer_day", 0.2765],
        ["summer_night", 0.2515],
        ["winter_day", 0.7170],
        ["winter_night", 0.2890],
    ],
    columns=["line_rental_period", "elvia_night_day_cost_nok_per_kwh"],
)


def apply_elvia_night_day(df: pd.DataFrame) -> pd.DataFrame:
    df["line_rental_time_of_day"] = "day"
    df.loc[
        (df["hour"] < 6) | (df["hour"] >= 22), "line_rental_time_of_day"
    ] = "night"

    df["line_rental_season"] = "summer"
    df.loc[(df["month"] < 4) | (df["month"] > 10), "line_rental_season"] = "winter"
    df["elvia_night_day_period"] = (
        df["line_rental_season"] + "_" + df["line_rental_time_of_day"]
    )
    df.drop(columns=['line_rental_time_of_day', 'line_rental_season'])
    return pd.merge(
        df,
        df_elvia_night_day_variable,
        left_on="elvia_night_day_period",
        right_on="line_rental_period"
    ).sort_values('startTime').reset_index(drop=True)
