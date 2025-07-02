import psycopg2
import pandas as pd


def load_inventory_levels(db_path: str) -> pd.DataFrame:
    """Load current inventory levels from the SQLite database."""
    conn = psycopg2.connect("dma_bananen.db")
    df = pd.read_sql_query(
        "SELECT posbestandId, mengekg FROM posbestand", conn
    )
    conn.close()
    return df


def detect_outliers_zscore(df: pd.DataFrame, threshold: float = 3.0) -> pd.DataFrame:
    """Return dataframe with z-scores and outlier flag using the given threshold."""
    mean = df["mengekg"].mean()
    std = df["mengekg"].std()
    df = df.copy()
    df["zscore"] = (df["mengekg"] - mean) / std
    df["is_outlier"] = df["zscore"].abs() > threshold
    return df


def detect_outliers_iqr(df: pd.DataFrame, factor: float = 1.5) -> pd.DataFrame:
    """Return dataframe with outlier flag based on IQR method."""
    q1 = df["mengekg"].quantile(0.25)
    q3 = df["mengekg"].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - factor * iqr
    upper = q3 + factor * iqr
    df = df.copy()
    df["is_outlier"] = (df["mengekg"] < lower) | (df["mengekg"] > upper)
    return df


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Detect outliers in POS inventory")
    parser.add_argument("db", help="Path to SQLite database")
    parser.add_argument("--method", choices=["zscore", "iqr"], default="zscore")
    args = parser.parse_args()

    data = load_inventory_levels(args.db)
    if args.method == "zscore":
        result = detect_outliers_zscore(data)
    else:
        result = detect_outliers_iqr(data)
    print(result)