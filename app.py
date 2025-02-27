import streamlit as st
import pandas as pd
import os
from io import BytesIO

# ✅ Set Page Config with a dynamic title and wide layout
st.set_page_config(page_title="🚀 HyperData Nexus", layout="wide")

# Custom CSS for Futuristic Styling with Intense Animations
def custom_css():
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Orbitron&display=swap');
            body { font-family: 'Orbitron', sans-serif; background: linear-gradient(135deg, #000428, #004e92); color: #ffffff; }
            .stApp { background: linear-gradient(135deg, #020024, #090979, #00d4ff); }
            .stButton>button, .stDownloadButton>button { 
                background: linear-gradient(90deg, #ff416c, #ff4b2b); 
                color: white !important; 
                border-radius: 12px; 
                transition: 0.3s ease-in-out; 
                font-weight: bold;
                border: 2px solid #ffffff;
                padding: 12px;
            }
            .stButton>button:hover, .stDownloadButton>button:hover { 
                transform: scale(1.1) rotate(-2deg); 
                box-shadow: 0 0 20px rgba(255, 75, 43, 0.8);
            }
            .stFileUploader { border: 3px dashed #ff4b2b; padding: 12px; animation: glow 1.5s infinite alternate; }
            @keyframes glow {
                0% { box-shadow: 0 0 15px #ff416c; }
                100% { box-shadow: 0 0 25px #ff4b2b; }
            }
            h1 { text-align: center; animation: fadeIn 1.5s ease-in-out; color: #ffffff; }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(-30px); }
                to { opacity: 1; transform: translateY(0); }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
custom_css()

# Sidebar for Theme Customization
with st.sidebar:
    st.header("⚡ Theme Customization")
    theme_choice = st.radio("Choose a Theme:", ["Dark Cyber", "Neon Future", "Galaxy"], horizontal=True)
    st.button("🔄 Apply Theme")

def set_theme(theme_choice):
    if theme_choice == "Neon Future":
        st.markdown(
            """
            <style>
                body, .stApp { background-color: #000000 !important; color: #00FFCC !important; }
            </style>
            """,
            unsafe_allow_html=True,
        )
set_theme(theme_choice)

# Main App Title with Animation
st.markdown('<h1>🚀 HyperData Nexus</h1>', unsafe_allow_html=True)
st.write("An ultra-modern data processing hub with dynamic visuals and interactivity!")

# File Uploader
uploaded_files = st.file_uploader("📂 Upload Your CSV or Excel Files:", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        # Read the uploaded file
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue
        
        st.success(f"✅ File Loaded: {file.name} ({len(file.getbuffer()) / 1024:.2f} KB)")
        
        # Display Data Preview
        st.subheader("🔍 Data Preview")
        st.dataframe(df.head())
        
        # Data Cleaning Options
        st.subheader("🛠️ Data Cleaning")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"🚮 Remove Duplicates for {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates Removed!")
            with col2:
                if st.button(f"🔧 Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing Values Filled!")
        
        # Column Selection
        st.subheader("🎯 Choose Columns")
        selected_columns = st.multiselect(f"Select Columns for {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        
        # Data Visualization
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Graph for {file.name}"):
            st.line_chart(df.select_dtypes(include='number').iloc[:, :2])
        
        # Convert File Format
        st.subheader("🔁 Convert File Format")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)
        if st.button(f"📥 Convert {file.name}"):
            buffer = BytesIO()
            file_name = file.name.replace(file_ext, ".csv" if conversion_type == "CSV" else ".xlsx")
            mime_type = "text/csv" if conversion_type == "CSV" else "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            df.to_csv(buffer, index=False) if conversion_type == "CSV" else df.to_excel(buffer, index=False)
            buffer.seek(0)
            st.download_button(label=f"📥 Download {file.name} as {conversion_type}", data=buffer, file_name=file_name, mime=mime_type)

st.success("🚀 HyperData Nexus: Transforming data into futuristic insights!")
