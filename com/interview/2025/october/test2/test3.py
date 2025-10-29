import pandas as pd
import numpy as np

def clean_sales_dataset(csv_path: str = "sales_data_missing.csv") -> np.ndarray:
    df = pd.read_csv(csv_path)

    # 1) Fill missing promotion_id
    df["promotion_id"] = df["promotion_id"].fillna("No Promotion")

    # Choose sales column (use order_value_column if present, else order_value)
    sales_col = "order_value_column" if "order_value_column" in df.columns else "order_value"

    # 2) Monthly totals per product_id
    df["_month"] = pd.to_datetime(df["order_date"], errors="coerce").dt.month
    totals = (
        df.groupby(["product_id", "_month"], dropna=True)[sales_col]
          .sum()
          .unstack(fill_value=0.0)
    )

    # Keep month columns in ascending order (there are only two months in data)
    month_cols = sorted([c for c in totals.columns if pd.notna(c)])
    totals = totals.reindex(columns=month_cols, fill_value=0.0)
    totals.columns = [int(c) for c in totals.columns]  # ensure integer month labels

    # 3) Final dataset: order_id, product_id, promotion_id, monthly totals
    final_df = df[["order_id", "product_id", "promotion_id"]].join(totals, on="product_id")
    final_df = final_df[["order_id", "product_id", "promotion_id"] + list(totals.columns)]

    # 4) Return as NumPy array
    return final_df.to_numpy()

if __name__ == "__main__":
    cleaned = clean_sales_dataset()
    print(cleaned)
