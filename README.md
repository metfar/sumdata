# sumData

Common data layer for the SUM ecosystem. r20 catalogs the 108 objects returned by the agreed `datasets` reference list. The release intentionally does **not** bundle the upstream CSV/RDA payloads.

`mtcars` is generated natively in Python for zero-download examples. Fetch the rest after installation with:

```bash
sumdata-fetch-r-datasets
# or one dataset
sumdata-fetch-r-datasets --dataset iris
```

The default cache is `~/.local/share/sumdata/r-datasets`; set `SUMDATA_HOME` or `--destination` to change it. `read_rds()` / `save_rds()` use the optional `pyreadr` bridge for external RDS files.

<p align=center><b>- oOo -</b></p>

