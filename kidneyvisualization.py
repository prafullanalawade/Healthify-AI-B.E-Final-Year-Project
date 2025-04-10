import streamlit as st
import matplotlib.pyplot as plt

def kidney_visualization_page():
    st.title("Kidney Disease Visualization")

    # Debugging: Check if data is available in session state
    st.write("Session State Data: ", st.session_state.get('user_data', 'No Data Found'))

    # Retrieve data from session state
    if 'user_data' not in st.session_state:
        st.error("No prediction data available.")
        return

    data = st.session_state['user_data']

    # Display the extracted data table and keys for debugging 
    st.subheader("Extracted Data Table")
    st.table(data)
    st.write("Available keys in data:", list(data.keys()))

    # Define mapping between display labels and data keys (using only specified features)
    column_mapping = {
        "Age": "Age",
        "Blood Pressure": "Blood Pressure",
        "Blood Sugar Level > 120 mg/dl": "Blood Sugar Level > 120 mg/dl",
        "Albumin": "Albumin",
        "Serum Creatinine": "Serum Creatinine",
        "Blood Urea Nitrogen": "Blood Urea Nitrogen",
        "Red Blood Cells": "Red Blood Cells",
        "Haemoglobin Level": "Haemoglobin Level"
    }

    # Prepare data for plotting
    columns = list(column_mapping.keys())
    values = []

    for col in columns:
        key = column_mapping[col]
        if key in data:
            try:
                values.append(float(data[key]))
            except ValueError:
                values.append(0.0)  # If conversion to float fails, append 0.0
        else:
            values.append(0.0)  # Append 0.0 if key is missing

    # Create Bar Chart
    st.subheader("Bar Chart of Input Values")
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(columns, values, color='skyblue')

    # Customize bar chart
    ax.set_xlabel('Attributes', fontsize=12)
    ax.set_ylabel('Values', fontsize=12) 
    ax.set_title('Kidney Disease Prediction Input Features', fontsize=14, pad=20)

    # Rotate x-axis labels
    plt.xticks(rotation=45, ha='right')

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom')

    plt.tight_layout()
    st.pyplot(fig)

    # Create Pie Chart
    st.subheader("Distribution of Input Values") 
    fig, ax = plt.subplots(figsize=(10, 8))

    # Calculate percentages
    total = sum(values)
    percentages = [val/total * 100 for val in values]

    # Custom colors
    colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC', 
              '#99CCFF', '#FF99FF', '#FFFF99']

    # Create pie chart
    wedges, texts, autotexts = ax.pie(percentages,
                                       labels=columns,
                                       colors=colors, 
                                       autopct='%1.1f%%',
                                       startangle=90,
                                       pctdistance=0.85)

    # Enhance appearance
    plt.setp(autotexts, size=9, weight="bold")
    plt.setp(texts, size=10)

    ax.set_title("Distribution of Input Values", fontsize=14, pad=20)

    # Add legend
    ax.legend(wedges, columns,
              title="Attributes",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))

    plt.axis('equal')
    plt.tight_layout()
    st.pyplot(fig)

    # Show prediction result
    kidney_result = st.session_state.get("kidney_result", "No Prediction Made")

    if kidney_result in ["The person may have kidney disease", "The person does not have kidney disease"]:
        st.subheader("Prediction Result Distribution")
        has_disease = 1 if kidney_result == "The person may have kidney disease" else 0

        result_counts = {
            "Has Kidney Disease": has_disease,
            "No Kidney Disease": 1 - has_disease
        }

        # Create result pie chart
        fig, ax = plt.subplots()
        ax.pie(result_counts.values(),
               labels=result_counts.keys(),
               autopct="%1.1f%%",
               startangle=90,
               colors=['#FF9999', '#66B2FF'])
        ax.set_title("Kidney Disease Prediction Result")
        st.pyplot(fig)
    else:
        st.warning("No prediction result available for visualization.")
import streamlit as st
import matplotlib.pyplot as plt

def kidney_visualization_page():
    st.title("Kidney Disease Visualization")

    # Debugging: Check if data is available in session state
    st.write("Session State Data: ", st.session_state.get('user_data', 'No Data Found'))

    # Retrieve data from session state
    if 'user_data' not in st.session_state:
        st.error("No prediction data available.")
        return

    data = st.session_state['user_data']

    # Display the extracted data table and keys for debugging 
    st.subheader("Extracted Data Table")
    st.table(data)
    st.write("Available keys in data:", list(data.keys()))

    # Define mapping between display labels and data keys (using only specified features)
    column_mapping = {
        "Age": "Age",
        "Blood Pressure": "Blood Pressure",
        "Blood Sugar Level > 120 mg/dl": "Blood Sugar Level > 120 mg/dl",
        "Albumin": "Albumin",
        "Serum Creatinine": "Serum Creatinine",
        "Blood Urea Nitrogen": "Blood Urea Nitrogen",
        "Red Blood Cells": "Red Blood Cells",
        "Haemoglobin Level": "Haemoglobin Level"
    }

    # Prepare data for plotting
    columns = list(column_mapping.keys())
    values = []

    for col in columns:
        key = column_mapping[col]
        if key in data:
            try:
                values.append(float(data[key]))
            except ValueError:
                values.append(0.0)  # If conversion to float fails, append 0.0
        else:
            values.append(0.0)  # Append 0.0 if key is missing

    # Debugging: Check values list
    st.write("Values List for Plotting:", values)

    # Create Bar Chart
    st.subheader("Bar Chart of Input Values")
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(columns, values, color='skyblue')

    # Customize bar chart
    ax.set_xlabel('Attributes', fontsize=12)
    ax.set_ylabel('Values', fontsize=12) 
    ax.set_title('Kidney Disease Prediction Input Features', fontsize=14, pad=20)

    # Rotate x-axis labels
    plt.xticks(rotation=45, ha='right')

    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom')

    plt.tight_layout()
    st.pyplot(fig)

    # Create Pie Chart
    st.subheader("Distribution of Input Values") 
    fig, ax = plt.subplots(figsize=(10, 8))

    # Calculate percentages
    total = sum(values)
    percentages = [val/total * 100 for val in values]

    # Custom colors
    colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC', 
              '#99CCFF', '#FF99FF', '#FFFF99']

    # Create pie chart
    wedges, texts, autotexts = ax.pie(percentages,
                                       labels=columns,
                                       colors=colors, 
                                       autopct='%1.1f%%',
                                       startangle=90,
                                       pctdistance=0.85)

    # Enhance appearance
    plt.setp(autotexts, size=9, weight="bold")
    plt.setp(texts, size=10)

    ax.set_title("Distribution of Input Values", fontsize=14, pad=20)

    # Add legend
    ax.legend(wedges, columns,
              title="Attributes",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))

    plt.axis('equal')
    plt.tight_layout()
    st.pyplot(fig)

    # Show prediction result
    kidney_result = st.session_state.get("kidney_result", "No Prediction Made")

    # Debugging: Check kidney result
    st.write("Kidney Disease Prediction Result:", kidney_result)

    if kidney_result in ["The person may have kidney disease", "The person does not have kidney disease"]:
        st.subheader("Prediction Result Distribution")
        has_disease = 1 if kidney_result == "The person may have kidney disease" else 0

        result_counts = {
            "Has Kidney Disease": has_disease,
            "No Kidney Disease": 1 - has_disease
        }

        # Create result pie chart
        fig, ax = plt.subplots()
        ax.pie(result_counts.values(),
               labels=result_counts.keys(),
               autopct="%1.1f%%",
               startangle=90,
               colors=['#FF9999', '#66B2FF'])
        ax.set_title("Kidney Disease Prediction Result")
        st.pyplot(fig)
    else:
        st.warning("No prediction result available for visualization.")
