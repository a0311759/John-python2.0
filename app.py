import streamlit as st
import subprocess
import sys
import os

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

# Streamlit UI
st.title("Python Online Interpreter")
st.write("Enter your Python code below and click 'Run Code' to execute it.")

# Default sample code for users
sample_code = """import math

# Calculate the square root of 16
result = math.sqrt(16)
print("The square root of 16 is:", result)
"""

# Text area for user input (with pre-filled sample code)
user_code = st.text_area("Python Code", sample_code, height=250)

# Execute code
if st.button("Run Code"):
    if user_code.strip():
        if write_code_to_file(user_code):
            output, error, returncode = run_code()
            if returncode == 0:
                st.success("Output:")
                st.code(output)
            else:
                st.error("Error:")
                st.code(error)
        else:
            st.error("Failed to write code to file.")
    else:
        st.warning("Please enter some Python code to run.")
        
