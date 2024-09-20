import streamlit as st
import subprocess
import sys
import io
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pandas as pd

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
        result = subprocess.run([sys.executable, filename], capture_output=True, text=True, timeout=100)
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "Error: Code execution timed out.", 1
    except Exception as e:
        return "", f"Error executing code: {e}", 1

# Function to display matplotlib plots
def display_matplotlib_plot():
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    st.image(buf)
    buf.close()
    plt.close()

# Streamlit UI
st.title("Python Online Interpreter with Plotting Support")
st.write("Enter your Python code below and click 'Run Code' to execute it.")

# Default sample code for users
sample_code = """
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# Sample data for the bar plot
data = pd.DataFrame({
    'Fruits': ['Apples', 'Bananas', 'Cherries', 'Dates'],
    'Quantities': [30, 20, 25, 15]
})

# Create a bar plot
plt.figure(figsize=(8, 5))
sns.barplot(x='Fruits', y='Quantities', data=data, palette='viridis')

# Add titles and labels
plt.title('Fruit Quantities')
plt.xlabel('Fruits')
plt.ylabel('Quantities')

# Show the plot
plt.show()



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
                
                # Check if user code generated a plot
                try:
                    # Reset figure and figure variables
                    plt.close('all')
                    globals()['fig'] = None
                    
                    exec(user_code)
                    
                    # Display matplotlib or seaborn plots
                    if plt.get_fignums():
                        display_matplotlib_plot()  # Display matplotlib or seaborn plots
                    
                    # Display Plotly plot if `fig` exists
                    if 'fig' in globals() and globals()['fig'] is not None:
                        st.plotly_chart(globals()['fig'])  # Display Plotly plots
                        
                except Exception as plot_error:
                    st.error(f"Plotting error: {plot_error}")
            else:
                st.error("Error:")
                st.code(error)
        else:
            st.error("Failed to write code to file.")
    else:
        st.warning("Please enter some Python code to run.")
