import streamlit as st
import subprocess
import sys
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import io

# Function to write user code to a temporary file
def write_code_to_file(code, filename="temp_code.py"):
    try:
        with open(filename, "w") as f:
            f.write(code)
        return True
    except Exception as e:
        st.error(f"Error writing code to file: {e}")
        return False

# Function to run the code and capture output
def run_code(filename="temp_code.py"):
    try:
        result = subprocess.run([sys.executable, filename], capture_output=True, text=True, timeout=10)
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "Error: Code execution timed out.", 1
    except Exception as e:
        return "", f"Error executing code: {e}", 1

# Function to capture matplotlib plots and display them
def display_plot():
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    st.image(buf)
    buf.close()
    plt.close()

# Streamlit UI
st.title("Python Online Interpreter with Plotting Support")
st.write("Enter your Python code below and click 'Run Code' to execute it.")

# Default sample code for users
sample_code = """import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import plotly.express as px

# Example matplotlib plot
plt.figure()
x = np.linspace(0, 10, 100)
y = np.sin(x)
plt.plot(x, y)
plt.title("Matplotlib Example")

# Example seaborn plot
sns.set(style="whitegrid")
tips = sns.load_dataset("tips")
sns.boxplot(x="day", y="total_bill", data=tips)
plt.figure()

# Example plotly plot
df = px.data.iris()
fig = px.scatter(df, x="sepal_width", y="sepal_length", color="species", title="Plotly Example")
fig.show()
"""

# Text area for user input (with pre-filled sample code)
user_code = st.text_area("Python Code", sample_code, height=250)

# Execute code
if st.button("Run Code"):
    if user_code.strip():
        if write_code_to_file(user_code):
            # Try to run the code
            output, error, returncode = run_code()
            
            # Display output if successful
            if returncode == 0:
                st.success("Output:")
                st.code(output)
                
                # Check if the user code generates a plot (for matplotlib, seaborn)
                try:
                    exec(user_code)
                    display_plot()  # Display matplotlib or seaborn plots
                except Exception as plot_error:
                    st.error(f"Plotting error: {plot_error}")
            else:
                st.error("Error:")
                st.code(error)
        else:
            st.error("Failed to write code to file.")
    else:
        st.warning("Please enter some Python code to run.")
