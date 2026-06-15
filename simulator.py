import random
import pandas as pd
from datetime import datetime
import os

CSV_FILE = "data/waste_data.csv"

def generate_bin_data():
    fill_percentage = random.randint(0, 100)

    if fill_percentage < 30:
        status = "Empty"
        alert = "Normal"
    elif fill_percentage < 70:
        status = "Half Full"
        alert = "Warning"
    elif fill_percentage < 90:
        status = "Nearly Full"
        alert = "Warning"
    else:
        status = "Full"
        alert = "Critical"

    data = {
        "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Fill Percentage": fill_percentage,
        "Status": status,
        "Alert": alert
    }

    return data

def save_data(data):
    os.makedirs("data", exist_ok=True)

    df = pd.DataFrame([data])

    if os.path.exists(CSV_FILE):
        df.to_csv(CSV_FILE, mode="a", header=False, index=False)
    else:
        df.to_csv(CSV_FILE, index=False)