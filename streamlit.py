# Create a Streamlit app that includes:
# A short title and description of the case.
# One or more visualizations (line chart, bar chart, etc.) that show trends in the data (e.g., births vs. deaths, hand-washing introduction impact).
# Short explanation (2–3 sentences) within the app describing your findings
# Optional: Add filters or sliders for exploring different years or hospitals.

import deaths_by_clinic.streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('yearly_deaths_by_clinic-1.csv')