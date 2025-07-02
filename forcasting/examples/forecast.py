import psycopg2
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA


def load_sales_series(db_path: str, posbestand_id: int) -> pd.Series:
    """Return daily sales series for a POS inventory item."""
    conn = psycopg2.connect("dma_bananen.db")
    query = "SELECT verkaufsdatum, verkauftemengekg " \
            "FROM posverkauf WHERE posbestandId = %s ORDER BY verkaufsdatum"
    df = pd.read_sql_query(query, conn, params=[posbestand_id], parse_dates=["verkaufsdatum"])
    conn.close()
    if df.empty:
        return pd.Series(dtype=float)
    series = (
        df.groupby("verkaufsdatum")["verkauftemengekg"].sum()
        .asfreq("D")
        .fillna(0.0)
    )
    return series


def forecast_inventory(db_path: str, posbestand_id: int, periods: int = 7) -> pd.Series:
    """Forecast inventory levels for the next ``periods`` days."""
    sales_ts = load_sales_series(db_path, posbestand_id)
    if sales_ts.empty:
        raise ValueError("No sales data for posbestand_id %s" % posbestand_id)

    model = ARIMA(sales_ts, order=(1, 1, 1))
    fitted = model.fit()
    forecast_sales = fitted.forecast(steps=periods)

    conn = psycopg2.connect("dma_bananen.db")
    cur = conn.execute(
        "SELECT mengekg FROM posbestand WHERE posbestandId = ?", (posbestand_id,)
    )
    row = cur.fetchone()
    conn.close()
    if not row:
        raise ValueError(f"posbestandId {posbestand_id} not found")
    current_inv = row[0]

    predicted_inv = current_inv - forecast_sales.cumsum()
    predicted_inv.index = pd.date_range(sales_ts.index.max() + pd.Timedelta(days=1), periods=periods)
    return predicted_inv


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Forecast POS inventory levels")
    parser.add_argument("db", help="Path to SQLite database")
    parser.add_argument("posbestand", type=int, help="POS inventory id")
    parser.add_argument("--days", type=int, default=7, help="forecast horizon")
    args = parser.parse_args()

    result = forecast_inventory(args.db, args.posbestand, args.days)
    print(result)
