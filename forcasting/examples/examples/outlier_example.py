from pathlib import Path
from detect_outliers import load_inventory_levels, detect_outliers_zscore

DB_PATH = Path(__file__).resolve().parents[1] / 'dma_bananen.db'

data = load_inventory_levels(str(DB_PATH))
results = detect_outliers_zscore(data)
print(results)