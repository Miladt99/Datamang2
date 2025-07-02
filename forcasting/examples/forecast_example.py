from pathlib import Path
from forecast import forecast_inventory

DB_PATH = Path(__file__).resolve().parents[1] / 'dma_bananen.db'
POSBESTAND_ID = 1  # example id

print(f"Forecasting inventory for posbestand {POSBESTAND_ID} using {DB_PATH}")
forecast = forecast_inventory(str(DB_PATH), POSBESTAND_ID)
print(forecast