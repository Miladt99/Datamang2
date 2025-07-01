 Data Warehouse Layer

This folder contains a simple star schema and ETL script that build a
reporting layer from the operational SQLite database `dma_bananen.db`.

## Schema

The SQL file `create_dw_schema.sql` defines dimension and fact tables:

- `dim_date` – calendar dimension used by all facts
- `dim_partnerunternehmen` – business partners
- `dim_product` – products
- `dim_plantage`, `dim_qcstelle`, `dim_hafenlager`, `dim_dcstandort`,
  `dim_posstandort` – location dimensions for each supply chain stage
- `dim_dienstleister` – transport service providers
- Fact tables capturing events such as harvests, QC results, goods
  receipts and sales (`fact_ernte`, `fact_qcprobe`, `fact_hafen_eingang`,
  `fact_dc_eingang`, `fact_pos_eingang`, `fact_pos_verkauf`, `fact_transport`).

## ETL

Run `etl_to_dw.py` after the operational database is populated. The
script reads from `dma_bananen.db`, creates the warehouse schema in a
new SQLite database `dma_dw.db` and loads all dimensions and facts.

```bash
python warehouse/etl_to_dw.py
```

The resulting database can be used for analytics or to feed business
intelligence tools.