# download_grib2_for_wrfinput

This repository provides a few small Streamlit applications to download GRIB2
meteorological data that can be used to create input for the Weather Research
and Forecasting (WRF) model.  Each application downloads data from a different
public data source and saves the files to a directory that you specify.

## Requirements

- Python 3.8 or later
- [Streamlit](https://streamlit.io/) for the web interfaces
- `requests` for HTTP downloads

You can install the Python dependencies with pip:

```bash
pip install streamlit requests
```

## Available downloaders

| Script | Data source | Description |
| ------ | ----------- | ----------- |
| `fnl_downloader.py` | [UCAR RDA](https://rda.ucar.edu/) | Downloads the six‑hourly NCEP Final (FNL) Operational Global Analysis. |
| `gsm_downloader_Rgl.py` | [Kyoto University RISH](http://database.rish.kyoto-u.ac.jp/) | Retrieves Global Spectral Model (GSM) GPV regional files. |
| `gfs_downloader_noaa.py` | [NOAA NOMADS](https://nomads.ncep.noaa.gov/) | Fetches Global Forecast System (GFS) forecast files. |

Each Streamlit script accepts a start and end time (at 6‑hour intervals) and a
local folder path for saving the downloaded GRIB2 files.

## Running the applications

Use the `streamlit run` command with the script you want to execute.  For
example, to start the FNL downloader:

```bash
streamlit run python/fnl_downloader.py
```

You can replace the script name with `gsm_downloader_Rgl.py` or
`gfs_downloader_noaa.py` to download those datasets instead.  When the
application starts, it opens in your web browser and lets you configure the
date range and output directory.

## Notes

- The scripts download potentially large amounts of data. Ensure you have
  enough disk space before starting a long range download.
- The default save paths in the UI examples point to locations on WSL. Feel
  free to change them to any accessible directory on your system.


