import streamlit as st
from datetime import datetime, timedelta
import requests
import os


def download_gfs_file(cycle_datetime, forecast_hour, save_dir="downloads", resolution="0p25"):
    base_url = "https://nomads.ncep.noaa.gov/pub/data/nccf/com/gfs/prod"
    date_str = cycle_datetime.strftime("%Y%m%d")
    cycle = cycle_datetime.strftime("%H")
    filename = f"gfs.t{cycle}z.pgrb2.{resolution}.f{forecast_hour:03d}"
    url = f"{base_url}/gfs.{date_str}/{cycle}/atmos/{filename}"

    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, filename)

    try:
        with requests.get(url, stream=True) as r:
            if r.status_code == 200:
                with open(file_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                return f"Downloaded: {filename}"
            else:
                return f"Not Found: {filename}"
    except Exception as e:
        return f"Error downloading {filename}: {e}"


st.title("GFS Data Downloader (NOAA)")

st.markdown("Download GFS forecast GRIB2 files from NOAA's NOMADS server.")

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Cycle Date", datetime(2025, 1, 1).date())
    start_hour = st.selectbox("Start Cycle Hour (UTC)", [0, 6, 12, 18], index=0)
with col2:
    end_date = st.date_input("End Cycle Date", datetime(2025, 1, 1).date())
    end_hour = st.selectbox("End Cycle Hour (UTC)", [0, 6, 12, 18], index=3)

start_cycle = datetime.combine(start_date, datetime.min.time()) + timedelta(hours=start_hour)
end_cycle = datetime.combine(end_date, datetime.min.time()) + timedelta(hours=end_hour)

st.markdown("Forecast hour range (0-384, step 3)")
col3, col4 = st.columns(2)
with col3:
    fh_start = st.number_input("Start Forecast Hour", value=0, step=3, min_value=0, max_value=384)
with col4:
    fh_end = st.number_input("End Forecast Hour", value=48, step=3, min_value=0, max_value=384)

save_dir = st.text_input("Download folder path", value="//wsl.localhost/Ubuntu-22.04/home/rsaito_wsl/WRF/GFS_DATA")

if start_cycle > end_cycle:
    st.error("End cycle must be after start cycle.")
elif fh_start > fh_end:
    st.error("End forecast hour must be after start forecast hour.")
else:
    run = st.button("Start Download")

    if run:
        st.info(f"Downloading cycles from {start_cycle} to {end_cycle} (UTC)...")
        cycles = []
        current = start_cycle
        while current <= end_cycle:
            cycles.append(current)
            current += timedelta(hours=6)

        total = len(cycles) * ((fh_end - fh_start) // 3 + 1)
        progress = st.progress(0)
        counter = 0

        for cy in cycles:
            for fh in range(fh_start, fh_end + 1, 3):
                msg = download_gfs_file(cy, fh, save_dir)
                st.write(msg)
                counter += 1
                progress.progress(counter / total)

        st.success("All downloads completed.")
