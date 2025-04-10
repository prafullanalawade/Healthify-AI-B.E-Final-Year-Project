import streamlit as st
import matplotlib.pyplot as plt

def diabetes_visualization_page():
    # Check if the prediction type is 'diabetes'
    if 'prediction_type' not in st.session_state or st.session_state['prediction_type'] != 'diabetes':
        st.warning("Please make a diabetes prediction first to see the relevant visualization.")
        return
    
    st.title("Diabetes Prediction Visualization")
    
    # Retrieve data from session state
    if 'user_data' not in st.session_state:
        st.error("No prediction data available.")
        return
    
    data = st.session_state['user_data']
    
    # Display the extracted data table and keys for debugging
    st.subheader("Extracted Data Table")
    st.table(data)
    st.write("Available keys in data:", list(data.keys()))
    
    # Define the mapping between your desired labels and the actual keys in your data
    column_mapping = {
        "Glucose Level": "Glucose Level",
        "Blood Pressure": "Blood Pressure Value",  # Updated to match your data
        "Insulin": "Insulin Value",               # Updated to match your data
        "BMI": "BMI Value",                      # Updated to match your data
        "Age": "Age"
    }
    
    # Prepare data for plotting with proper key mapping
    columns = list(column_mapping.keys())  # These are your display labels
    values = [float(data[column_mapping[col]]) for col in columns]  # Get values using mapped keys
    
    # Create Bar Chart with improved formatting
    st.subheader("Bar Chart of Input Values")
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(columns, values, color='skyblue')
    
    # Customize bar chart
    ax.set_xlabel('Attributes', fontsize=12)
    ax.set_ylabel('Values', fontsize=12)
    ax.set_title('Input Values Bar Chart', fontsize=14, pad=20)
    
    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')
    
    # Add value labels on top of each bar
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom')
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    st.pyplot(fig)
    
    # Create Pie Chart with improved formatting
    st.subheader("Distribution of Input Values")
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Calculate percentages for pie chart
    total = sum(values)
    percentages = [val/total * 100 for val in values]
    
    # Custom colors for better visualization
    colors = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#FF99CC']
    
    # Create pie chart with better formatting
    wedges, texts, autotexts = ax.pie(percentages, 
                                     labels=columns,
                                     colors=colors,
                                     autopct='%1.1f%%',
                                     startangle=90,
                                     pctdistance=0.85)
    
    # Enhance pie chart appearance
    plt.setp(autotexts, size=9, weight="bold")
    plt.setp(texts, size=10)
    
    # Add a title
    ax.set_title("Distribution of Input Values", fontsize=14, pad=20)
    
    # Add legend
    ax.legend(wedges, columns,
             title="Attributes",
             loc="center left",
             bbox_to_anchor=(1, 0, 0.5, 1))
    
    plt.axis('equal')
    
    # Adjust layout to prevent label cutoff
    plt.tight_layout()
    st.pyplot(fig)