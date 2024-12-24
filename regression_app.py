import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import threading

# Ensures thread-safety for Matplotlib in Streamlit
# _lock = RendererAgg.lock

# Set Streamlit page config
st.set_page_config(page_title="Interactive Linear Regression", layout="wide")

# Initialize variables
slope = st.sidebar.slider("Slope", -10.0, 10.0, 1.0, 0.1)
intercept = st.sidebar.slider("Y-Intercept", -20.0, 20.0, 1.0, 0.1)

# Generate random data
np.random.seed(42)
x = np.linspace(0, 10, 50)
y = 3 * x + 5 + np.random.normal(0, 2, size=x.shape)

# Calculate regression line and error
def calculate_regression_line(x, slope, intercept):
    return slope * x + intercept

def calculate_total_error(y_true, y_pred):
    return np.sum((y_true - y_pred) ** 2)

# Generate the plot
y_pred = calculate_regression_line(x, slope, intercept)
total_error = calculate_total_error(y, y_pred)

_lock = threading.RLock()
with _lock:  # Thread-safety for Matplotlib
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), gridspec_kw={'height_ratios': [3, 1]})

    # Scatter plot
    ax1.scatter(x, y, color='blue', label='Data Points')
    ax1.plot(x, y_pred, color='red', label='Regression Line')
    ax1.set_xlim(0, 10)
    ax1.set_ylim(min(y) - 5, max(y) + 5)
    ax1.set_title("Interactive Linear Regression")
    ax1.legend()

    # Equation display
    ax1.text(0.5, max(y) + 2, f"y = {slope:.2f}x + {intercept:.2f}", fontsize=12, color='purple', ha='center')

    # Total error bar
    ax2.barh(['Total Error'], [total_error], color='green', height=0.2)
    ax2.set_xlim(0, max(500, total_error + 10))
    ax2.set_title("Total Error (Minimized Area)")

    st.pyplot(fig)
