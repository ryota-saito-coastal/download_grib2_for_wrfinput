import streamlit as st
from datetime import datetime, timedelta
import requests
import os

def download_fnl_file(date_time, save_dir="downloads"):
    base_url = "https://data.rda.ucar.edu/ds083.2/grib2"
    date_str = date_time.strftime("%Y/%Y.%m")
    filename = f"fnl_{date_time.strftime('%Y%m%d_%H_00')}.grib2"
    url = f"{base_url}/{date_str}/{filename}"

    os.makedirs(save_dir, exist_ok=True)
    file_path = os.path.join(save_dir, filename)

    try:
        with requests.get(url, stream=True) as r:
            if r.status_code == 200:
                with open(file_path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                return f"✅ Downloaded: {filename}"
            else:
                return f"❌ Not Found: {filename}"
    except Exception as e:
        return f"❌ Error downloading {filename}: {e}"

# UI
st.title("FNL Data Downloader")

st.markdown("Specify the download **start and end datetime** (UTC).")

# 日時入力
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", datetime(2025, 1, 1).date())
    start_hour = st.selectbox("Start Hour (UTC)", [0, 6, 12, 18], index=1)
with col2:
    end_date = st.date_input("End Date", datetime(2025, 1, 2).date())
    end_hour = st.selectbox("End Hour (UTC)", [0, 6, 12, 18], index=3)

start_dt = datetime.combine(start_date, datetime.min.time()) + timedelta(hours=start_hour)
end_dt = datetime.combine(end_date, datetime.min.time()) + timedelta(hours=end_hour)

# 保存先ディレクトリ入力
save_dir = st.text_input("Download folder path", value="//wsl.localhost/Ubuntu-22.04/home/rsaito_wsl/WRF/FNL_DATA")

# 実行ボタン
if start_dt > end_dt:
    st.error("End datetime must be after start datetime.")
else:
    run = st.button("Start Download")

    if run:
        st.info(f"Downloading from {start_dt} to {end_dt} (UTC)...")
        current = start_dt
        datetimes = []

        while current <= end_dt:
            if current.hour in [0, 6, 12, 18]:
                datetimes.append(current)
            current += timedelta(hours=6)

        total = len(datetimes)
        progress = st.progress(0)

        for i, dt in enumerate(datetimes):
            msg = download_fnl_file(dt, save_dir)
            st.write(msg)
            progress.progress((i + 1) / total)

        st.success("Download completed.")