import streamlit as st
import json
from datetime import datetime
import time
import schedule
import threading
from plyer import notification

# ====== DATA FUNCTIONS ======
def load_data():
    try:
        with open("data.json", "r") as file:
            return json.load(file)
    except:
        return {"water": [], "medications": []}

def save_data(data):
    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

data = load_data()


# ====== PUSH NOTIFICATION FUNCTION ======
def show_notification(medicine):
    notification.notify(
        title="Medication Reminder",
        message=f"Don't forget to take your medicine: {medicine}",
        timeout=10
    )
    print(f"Reminder shown for {medicine}")

# ====== SCHEDULER THREAD ======
def start_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)

threading.Thread(target=start_scheduler, daemon=True).start()


# ====== STREAMLIT UI ======
st.title("💊 Personal Health Reminder Bot")

# Water intake
if st.button("I drank water 💧"):
    data["water"].append(str(datetime.now()))
    save_data(data)
    st.success("Water logged!")

st.write(f"Water glasses today: {len(data['water'])}")

# Medication reminder
medicine = st.text_input("Enter medicine name")
time_input = st.time_input("Reminder time")

if st.button("Set Medication Reminder"):
    if medicine:
        schedule.every().day.at(str(time_input)).do(show_notification, medicine)
        st.success(f"✅ Reminder set for {medicine} at {time_input}")
    else:
        st.warning("Enter a medicine name!")

if st.button("I took my medicine"):
    if medicine:
        data["medications"].append({"name": medicine, "time": str(datetime.now())})
        save_data(data)
        st.success("✅ Logged!")
    else:
        st.warning("Enter medicine name")

# Show history
if st.checkbox("Show history"):
    st.write("Water:", data["water"])
    st.write("Medicines:", data["medications"])

