import streamlit as st
from datetime import datetime, timedelta
import requests
import os

# time step
fd_list = [
    'FD0000', 'FD0006', 'FD0012', 'FD0018',
    'FD0100', 'FD0106', 'FD0112', 'FD0118',
    'FD0200', 'FD0206', 'FD0212', 'FD0218',
    'FD0300', 'FD0306', 'FD0312', 'FD0318',
    'FD0400', 'FD0406', 'FD0412', 'FD0418',
    'FD0500', 'FD0506', 'FD0512', 'FD0518',
    'FD0600', 'FD0606', 'FD0612', 'FD0618',
    'FD0700', 'FD0706', 'FD0712', 'FD0718',
    'FD0800', 'FD0806', 'FD0812', 'FD0818',
    'FD0900', 'FD0906', 'FD0912', 'FD0918',
    'FD1000', 'FD1006', 'FD1012', 'FD1018',
    'FD1100'
]

# function
def download_gsm_file(base_datetime, fd_code, save_dir="downloads"):
    timestamp = base_datetime.strftime("%Y%m%d%H") + "0000"
    filename = f"Z__C_RJTD_{timestamp}_GSM_GPV_Rgl_{fd_code}_grib2.bin"

    yr = base_datetime.strftime("%Y")
    mh = base_datetime.strftime("%m")
    dy = base_datetime.strftime("%d")
    base_url = f"http://database.rish.kyoto-u.ac.jp/arch/jmadata/data/gpv/original/{yr}/{mh}/{dy}"
    url = f"{base_url}/{filename}"

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

# Streamlit UI
st.title("GSM GPV Downloader (RISH, Kyoto University)")

st.markdown("指定した期間・時刻の GSM GPV 各時間分割ファイル（FDxxxx）をダウンロードします。")

col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Start Date", datetime(2025, 5, 5).date())
    start_hour = st.selectbox("Start Hour (UTC)", [0, 6, 12, 18], index=0)
with col2:
    end_date = st.date_input("End Date", datetime(2025, 5, 6).date())
    end_hour = st.selectbox("End Hour (UTC)", [0, 6, 12, 18], index=3)

start_dt = datetime.combine(start_date, datetime.min.time()) + timedelta(hours=start_hour)
end_dt = datetime.combine(end_date, datetime.min.time()) + timedelta(hours=end_hour)

save_dir = st.text_input("Download folder path", value="//wsl.localhost/Ubuntu-22.04/home/rsaito_wsl/WRF/GSM_DATA")

if start_dt > end_dt:
    st.error("End datetime must be after start datetime.")
else:
    run = st.button("Start Download")

    if run:
        st.info(f"Downloading from {start_dt} to {end_dt} (UTC)...")

        datetimes = []
        current = start_dt
        while current <= end_dt:
            datetimes.append(current)
            current += timedelta(hours=6)

        total = len(datetimes) * len(fd_list)
        progress = st.progress(0)
        counter = 0

        for dt in datetimes:
            for fd in fd_list:
                msg = download_gsm_file(dt, fd, save_dir)
                st.write(msg)
                counter += 1
                progress.progress(counter / total)

        st.success("All downloads completed.")
