import numpy as np
import matplotlib.pyplot as plt

# Sample data
np.random.seed(42)
x = np.linspace(0, 10, 50)
y = 3 * x + 5 + np.random.normal(0, 2, size=x.shape)

# Initialize parameters
slope = 1
intercept = 1

# Calculate regression line
def calculate_regression_line(x, slope, intercept):
    return slope * x + intercept

# Calculate total error
def calculate_total_error(y_true, y_pred):
    return np.sum((y_true - y_pred) ** 2)

# Create the plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

# Scatter plot for data points
sc = ax1.scatter(x, y, color='blue', label='Data Points')
(line,) = ax1.plot(x, calculate_regression_line(x, slope, intercept), color='red', label='Regression Line')
(control_start,) = ax1.plot([x[0]], [calculate_regression_line(x[0], slope, intercept)], 
                            'o', color='green', label='Control Point Start', markersize=8)
(control_end,) = ax1.plot([x[-1]], [calculate_regression_line(x[-1], slope, intercept)], 
                          'o', color='orange', label='Control Point End', markersize=8)
###equation_text = ax1.text(0.5, max(y) + 2, f"y = {slope:.2f}x + {intercept:.2f}", fontsize=12, color='purple', ha='center')

equation_text = ax1.text(2.5, max(y) + 2, f"y = {slope:.2f}x + {intercept:.2f}", 
                         fontsize=12, color='purple', ha='center')

ax1.set_title('Interactive Linear Regression')
ax1.legend()
ax1.set_xlim(0, 10)
ax1.set_ylim(min(y) - 5, max(y) + 5)

# Bar for total error
bar = ax2.barh(['Total Error'], [0], color='green', height=0.5)
ax2.set_xlim(0, 500)  # Scaled down for a narrow strip
ax2.set_title('Total Error')

# Initialize the total error
y_pred = calculate_regression_line(x, slope, intercept)
total_error = calculate_total_error(y, y_pred)
bar[0].set_width(total_error)

# Variables to track dragging
dragging = None  # Track what is being dragged ('start', 'end', 'line', None)
start_event = None  # Store the initial click event

def on_press(event):
    """Handler for mouse press events."""
    global dragging, start_event
    if control_start.contains(event)[0]:  # Check if the start control point is clicked
        dragging = 'start'
    elif control_end.contains(event)[0]:  # Check if the end control point is clicked
        dragging = 'end'
    elif line.contains(event)[0]:  # Check if the line is clicked
        dragging = 'line'
    start_event = event

def on_release(event):
    """Handler for mouse release events."""
    global dragging, start_event
    dragging = None
    start_event = None

def on_motion(event):
    """Handler for mouse motion events."""
    global slope, intercept, dragging, start_event

    if dragging == 'start' and event.xdata is not None and event.ydata is not None:
        # Update the start control point position
        control_start.set_data([x[0]], [event.ydata])
        
        # Recalculate slope and intercept
        y_start = event.ydata
        y_end = slope * x[-1] + intercept
        slope = (y_end - y_start) / (x[-1] - x[0])
        intercept = y_start - slope * x[0]
    elif dragging == 'end' and event.xdata is not None and event.ydata is not None:
        # Update the end control point position
        control_end.set_data([x[-1]], [event.ydata])
        
        # Recalculate slope and intercept
        y_start = slope * x[0] + intercept
        y_end = event.ydata
        slope = (y_end - y_start) / (x[-1] - x[0])
        intercept = y_start - slope * x[0]
    elif dragging == 'line' and event.xdata is not None and event.ydata is not None:
        # Adjust the intercept based on vertical movement
        dy = event.ydata - start_event.ydata
        intercept += dy
        start_event = event  # Update start_event for continuous drag

    # Update regression line and control points
    y_pred = calculate_regression_line(x, slope, intercept)
    line.set_ydata(y_pred)
    control_start.set_data([x[0]], [slope * x[0] + intercept])
    control_end.set_data([x[-1]], [slope * x[-1] + intercept])

    # Update total error
    total_error = calculate_total_error(y, y_pred)
    bar[0].set_width(total_error)
    ax2.set_xlim(0, max(500, total_error + 10))  # Adjust dynamically

    # Update regression line equation
    equation_text.set_text(f"y = {slope:.2f}x + {intercept:.2f}")

    fig.canvas.draw_idle()

# Connect event handlers to the figure
fig.canvas.mpl_connect('button_press_event', on_press)
fig.canvas.mpl_connect('button_release_event', on_release)
fig.canvas.mpl_connect('motion_notify_event', on_motion)

plt.tight_layout()
plt.show()
