import streamlit as st
import pandas as pd
import joblib

# Load trained model (no month used in formula)
model = joblib.load("bike_model_nb.pkl")

# Streamlit UI
st.title("🚲 NYC East River Bike Count Predictor")
st.write("Predict daily bicycle traffic based on weather and day of the week.")

# User inputs
temp_avg = st.slider("Average Temperature (°F)", min_value=20, max_value=100, value=60)
precip = st.radio("Is there precipitation (rain/snow)?", ["No", "Yes"])
day_of_week = st.selectbox("Day of Week", [
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
])

# Preprocess input
precip_bin = 1 if precip == "Yes" else 0

# Prepare input DataFrame
input_df = pd.DataFrame({
    "temp_avg": [temp_avg],
    "precip_bin": [precip_bin],
    "day_of_week": [day_of_week]
})

# Ensure categorical values match model training
input_df['day_of_week'] = pd.Categorical(
    input_df['day_of_week'],
    categories=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
)

# Predict
prediction = model.predict(input_df)[0]

# Display result
st.metric("🚴 Predicted Bike Count", f"{int(prediction):,} riders")
