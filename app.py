import streamlit as st
import subprocess
import sys
import re

# Keywords, operators, numbers, strings, comments for syntax highlighting
KEYWORDS = [
    'False', 'await', 'else', 'import', 'pass', 'None', 'break', 'except', 'in', 
    'raise', 'True', 'class', 'finally', 'is', 'return', 'and', 'continue', 'for', 
    'lambda', 'try', 'as', 'def', 'from', 'nonlocal', 'while', 'assert', 'del', 
    'global', 'not', 'with', 'async', 'elif', 'if', 'or', 'yield'
]
OPERATORS = ['=', '==', '!=', '<', '>', '<=', '>=', '\+', '-', '\*', '/', '//', '\%', '\*\*', '&', '\|', '\^', '~', '<<', '>>']
COMMENTS_PATTERN = r'#.*'
STRING_PATTERN = r'(["\'])(?:(?=(\\?))\2.)*?\1'
NUMBER_PATTERN = r'\b\d+\.?\d*\b'

# Function to colorize code for different elements
def colorize_code(code):
    # Highlight comments
    code = re.sub(COMMENTS_PATTERN, lambda x: f'<span style="color: #008000;">{x.group(0)}</span>', code)

    # Highlight strings
    code = re.sub(STRING_PATTERN, lambda x: f'<span style="color: #D2691E;">{x.group(0)}</span>', code)

    # Highlight numbers
    code = re.sub(NUMBER_PATTERN, lambda x: f'<span style="color: #FF4500;">{x.group(0)}</span>', code)

    # Highlight operators
    for op in OPERATORS:
        code = re.sub(r'{}'.format(op), f'<span style="color: #0000FF;">{op}</span>', code)

    # Highlight keywords
    for kw in KEYWORDS:
        code = re.sub(r'\b{}\b'.format(kw), f'<span style="color: #ff6347;">{kw}</span>', code)
    
    return code

# Streamlit UI
st.title("Python Online Compiler with Syntax Highlighting")
st.write("Enter your Python code below:")

# Text area for user input
user_code = st.text_area("Python Code", height=250)

# Colorized code preview
if user_code:
    st.markdown("**Preview with Syntax Highlighting**", unsafe_allow_html=True)
    st.markdown(f"<pre>{colorize_code(user_code)}</pre>", unsafe_allow_html=True)

# Compile and Run code using subprocess
if st.button("Run Code"):
    if user_code:
        try:
            # Write the user code to a temporary file
            with open("temp_code.py", "w") as f:
                f.write(user_code)
                
            # Run the code with subprocess
            result = subprocess.run([sys.executable, "temp_code.py"], capture_output=True, text=True, timeout=5)
            
            # Display output or error
            if result.returncode == 0:
                st.success("Output:")
                st.code(result.stdout)
            else:
                st.error("Error:")
                st.code(result.stderr)
        except subprocess.TimeoutExpired:
            st.error("Error: Code execution timed out.")
    else:
        st.error("Please enter Python code to run.")

# Display a prompt to try out data science code examples
st.markdown("### Try running this sample code:")
sample_code = """
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Create a sample DataFrame
data = {'X': [1, 2, 3, 4, 5], 'Y': [2, 4, 6, 8, 10]}
df = pd.DataFrame(data)

# Print DataFrame
print("Sample DataFrame:")
print(df)

# Plotting
plt.plot(df['X'], df['Y'])
plt.title('Sample Plot')
plt.xlabel('X Axis')
plt.ylabel('Y Axis')
plt.grid(True)
plt.show()
"""
st.code(sample_code)
