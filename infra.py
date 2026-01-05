import streamlit as st
from ultralytics import YOLO
import cv2
import tempfile
import os
from datetime import datetime
import numpy as np
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Page Configuration
st.set_page_config(
    page_title="Sentryx - Infrastructure Monitoring",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Optimized Custom CSS - Reduced complexity for better performance
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    
    .main-header {
        background: rgba(99, 102, 241, 0.1);
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 25px;
        border: 1px solid rgba(99, 102, 241, 0.3);
    }
    
    .main-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        text-align: center;
    }
    
    .subtitle {
        color: #a5b4fc;
        text-align: center;
        font-size: 1rem;
        margin-top: 8px;
    }
    
    .alert-box {
        background: rgba(239, 68, 68, 0.15);
        border-left: 4px solid #ef4444;
        border-radius: 12px;
        padding: 20px;
        margin: 20px 0;
    }
    
    .alert-success {
        background: rgba(34, 197, 94, 0.15);
        border-left: 4px solid #22c55e;
    }
    
    .alert-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #fca5a5;
        margin-bottom: 10px;
    }
    
    .alert-success .alert-title {
        color: #86efac;
    }
    
    .status-badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85rem;
        margin: 5px;
    }
    
    .status-critical {
        background: #ef4444;
        color: white;
    }
    
    .status-safe {
        background: #22c55e;
        color: white;
    }
    
    .detection-box {
        background: rgba(30, 27, 75, 0.5);
        border-radius: 12px;
        padding: 15px;
        border: 1px solid rgba(99, 102, 241, 0.3);
        margin: 8px 0;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'detection_history' not in st.session_state:
    st.session_state.detection_history = []
if 'total_scans' not in st.session_state:
    st.session_state.total_scans = 0
if 'total_defects' not in st.session_state:
    st.session_state.total_defects = 0

# Header
st.markdown("""
<div class="main-header">
    <h1 class="main-title">🛡️ SENTRYX</h1>
    <p class="subtitle">AI-Powered Infrastructure Monitoring & Defect Detection System</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ System Controls")
    st.markdown("---")
    
    confidence_threshold = st.slider(
        "Detection Confidence",
        min_value=0.01,
        max_value=1.0,
        value=0.25,
        step=0.01,
        help="Adjust sensitivity of defect detection"
    )
    
    st.markdown("---")
    st.markdown("### 📊 System Status")
    st.success("🟢 ONLINE")
    
    st.markdown("---")
    st.markdown("### 📈 Statistics")
    st.metric("Total Scans", st.session_state.total_scans)
    st.metric("Defects Found", st.session_state.total_defects)
    
    if st.session_state.total_scans > 0:
        detection_rate = (st.session_state.total_defects / st.session_state.total_scans) * 100
        st.metric("Detection Rate", f"{detection_rate:.1f}%")

# Main Content
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📤 Upload Infrastructure Image")
    uploaded_file = st.file_uploader(
        "Choose an image file",
        type=["jpg", "jpeg", "png"],
        help="Upload an image of infrastructure for defect detection"
    )

with col2:
    st.markdown("### ℹ️ Quick Info")
    st.info("""
    **Supported Formats:**
    - JPG, JPEG, PNG
    
    **Detection Types:**
    - Cracks
    - Structural damage
    - Surface defects
    - Anomalies
    """)

# Load YOLO model - Using custom infrastructure detection model
@st.cache_resource
def load_model():
    return YOLO("microsoft infra.pt")

model = load_model()

# Detection Processing
if uploaded_file is not None:
    # Save uploaded file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp.write(uploaded_file.read())
        image_path = tmp.name
    
    # Display original image
    st.markdown("---")
    st.markdown("### 🔍 Analysis Results")
    
    col_orig, col_detect = st.columns(2)
    
    with col_orig:
        st.markdown("#### Original Image")
        original_img = Image.open(image_path)
        st.image(original_img, use_column_width=True)
    
    # Run detection
    with st.spinner('🔄 Analyzing infrastructure...'):
        results = model.predict(
            source=image_path,
            conf=confidence_threshold,
            iou=0.45,
            imgsz=1024,
            save=False
        )
    
    # Process results
    result_img = results[0].plot()
    result_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
    
    # Get detection details
    boxes = results[0].boxes
    num_detections = len(boxes)
    
    # Update statistics
    st.session_state.total_scans += 1
    st.session_state.total_defects += num_detections
    
    # Add to history
    detection_record = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'detections': num_detections,
        'confidence': confidence_threshold,
        'status': 'Critical' if num_detections > 0 else 'Safe'
    }
    st.session_state.detection_history.insert(0, detection_record)
    if len(st.session_state.detection_history) > 10:
        st.session_state.detection_history.pop()
    
    with col_detect:
        st.markdown("#### Detection Result")
        st.image(result_img, use_column_width=True)
    
    # Alert Notification
    st.markdown("---")
    if num_detections > 0:
        st.markdown(f"""
        <div class="alert-box">
            <div class="alert-title">⚠️ ALERT: Defects Detected!</div>
            <p style="color: #fecaca; font-size: 1.1rem; margin: 10px 0;">
                <strong>{num_detections}</strong> potential infrastructure defect(s) identified
            </p>
            <p style="color: #fca5a5; margin: 5px 0;">
                📍 Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            </p>
            <p style="color: #fca5a5; margin: 5px 0;">
                🎯 Confidence Threshold: {confidence_threshold:.0%}
            </p>
            <span class="status-badge status-critical">REQUIRES ATTENTION</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Show detection details
        st.markdown("### 📋 Detection Details")
        
        detection_data = []
        for idx, box in enumerate(boxes):
            conf = float(box.conf[0])
            cls = int(box.cls[0])
            class_name = model.names[cls]
            
            detection_data.append({
                'ID': idx + 1,
                'Type': class_name,
                'Confidence': f"{conf:.2%}",
                'Severity': '🔴 High' if conf > 0.7 else '🟡 Medium' if conf > 0.4 else '🟢 Low'
            })
        
        st.dataframe(detection_data, use_container_width=True)
        
        # Interactive Graphs
        st.markdown("---")
        st.markdown("### 📊 Detection Analytics")
        
        # Prepare data for graphs
        confidences = [float(box.conf[0]) for box in boxes]
        class_names = [model.names[int(box.cls[0])] for box in boxes]
        severities = ['High' if c > 0.7 else 'Medium' if c > 0.4 else 'Low' for c in confidences]
        
        # Create two columns for graphs
        graph_col1, graph_col2 = st.columns(2)
        
        with graph_col1:
            # Confidence Distribution Bar Chart
            fig_conf = go.Figure(data=[go.Bar(
                x=[f"Detection {i+1}" for i in range(len(confidences))],
                y=confidences,
                marker=dict(
                    color=confidences,
                    colorscale='RdYlGn',
                    showscale=True,
                    colorbar=dict(title="Confidence", x=1.15),
                    line=dict(color='rgba(255,255,255,0.3)', width=1)
                ),
                text=[f"{c:.1%}" for c in confidences],
                textposition='outside',
                hovertemplate='<b>Detection %{x}</b><br>Confidence: %{y:.2%}<extra></extra>'
            )])
            
            fig_conf.update_layout(
                title=dict(
                    text="Confidence Levels by Detection",
                    font=dict(size=16, color='#a5b4fc')
                ),
                xaxis_title="Detection ID",
                yaxis_title="Confidence Score",
                template="plotly_dark",
                height=400,
                plot_bgcolor='rgba(30, 27, 75, 0.5)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#a5b4fc'),
                yaxis=dict(range=[0, 1], tickformat='.0%'),
                margin=dict(t=50, b=50, l=50, r=100)
            )
            st.plotly_chart(fig_conf, use_container_width=True)
        
        with graph_col2:
            # Severity Breakdown Pie Chart
            severity_counts = {s: severities.count(s) for s in ['High', 'Medium', 'Low']}
            severity_colors = {'High': '#ef4444', 'Medium': '#f59e0b', 'Low': '#22c55e'}
            
            fig_severity = go.Figure(data=[go.Pie(
                labels=list(severity_counts.keys()),
                values=list(severity_counts.values()),
                marker=dict(
                    colors=[severity_colors[s] for s in severity_counts.keys()],
                    line=dict(color='rgba(255,255,255,0.3)', width=2)
                ),
                textinfo='label+percent+value',
                textfont=dict(size=14),
                hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>',
                hole=0.4
            )])
            
            fig_severity.update_layout(
                title=dict(
                    text="Severity Distribution",
                    font=dict(size=16, color='#a5b4fc')
                ),
                template="plotly_dark",
                height=400,
                plot_bgcolor='rgba(30, 27, 75, 0.5)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#a5b4fc'),
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_severity, use_container_width=True)
        
        # Detection Type Distribution (if multiple types detected)
        if len(set(class_names)) > 1:
            st.markdown("#### 🏷️ Defect Type Distribution")
            
            type_counts = {}
            for name in class_names:
                type_counts[name] = type_counts.get(name, 0) + 1
            
            fig_types = go.Figure(data=[go.Bar(
                x=list(type_counts.keys()),
                y=list(type_counts.values()),
                marker=dict(
                    color='#667eea',
                    line=dict(color='rgba(255,255,255,0.3)', width=1)
                ),
                text=list(type_counts.values()),
                textposition='outside',
                hovertemplate='<b>%{x}</b><br>Count: %{y}<extra></extra>'
            )])
            
            fig_types.update_layout(
                title=dict(
                    text="Defect Types Detected",
                    font=dict(size=16, color='#a5b4fc')
                ),
                xaxis_title="Defect Type",
                yaxis_title="Count",
                template="plotly_dark",
                height=350,
                plot_bgcolor='rgba(30, 27, 75, 0.5)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#a5b4fc'),
                margin=dict(t=50, b=50, l=50, r=50)
            )
            st.plotly_chart(fig_types, use_container_width=True)
        
        # Confidence Statistics
        st.markdown("#### 📈 Confidence Statistics")
        stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
        
        with stat_col1:
            st.metric("Average Confidence", f"{np.mean(confidences):.1%}")
        with stat_col2:
            st.metric("Highest Confidence", f"{np.max(confidences):.1%}")
        with stat_col3:
            st.metric("Lowest Confidence", f"{np.min(confidences):.1%}")
        with stat_col4:
            st.metric("Std Deviation", f"{np.std(confidences):.1%}")
        
    else:
        st.markdown(f"""
        <div class="alert-box alert-success">
            <div class="alert-title">✅ All Clear!</div>
            <p style="color: #bbf7d0; font-size: 1.1rem; margin: 10px 0;">
                No defects detected in the infrastructure
            </p>
            <p style="color: #86efac; margin: 5px 0;">
                📍 Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
            </p>
            <span class="status-badge status-safe">INFRASTRUCTURE SAFE</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Cleanup
    os.remove(image_path)

# Detection History
if st.session_state.detection_history:
    st.markdown("---")
    st.markdown("### 📜 Recent Detection History")
    
    for record in st.session_state.detection_history[:5]:
        status_class = "status-critical" if record['status'] == 'Critical' else "status-safe"
        st.markdown(f"""
        <div class="detection-box">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <p style="color: #a5b4fc; margin: 0;">🕐 {record['timestamp']}</p>
                    <p style="color: white; font-size: 1.1rem; margin: 5px 0;">
                        Detections: <strong>{record['detections']}</strong>
                    </p>
                </div>
                <span class="status-badge {status_class}">{record['status']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Detection Trend Graph
    if len(st.session_state.detection_history) >= 2:
        st.markdown("---")
        st.markdown("### 📈 Detection Trend Analysis")
        
        # Prepare trend data (reverse to show chronological order)
        history_reversed = list(reversed(st.session_state.detection_history))
        timestamps = [record['timestamp'] for record in history_reversed]
        detection_counts = [record['detections'] for record in history_reversed]
        
        # Create trend line chart
        fig_trend = go.Figure()
        
        # Add line trace
        fig_trend.add_trace(go.Scatter(
            x=list(range(1, len(timestamps) + 1)),
            y=detection_counts,
            mode='lines+markers',
            name='Detections',
            line=dict(color='#667eea', width=3),
            marker=dict(
                size=10,
                color=detection_counts,
                colorscale='RdYlGn_r',
                showscale=True,
                colorbar=dict(title="Count", x=1.15),
                line=dict(color='white', width=2)
            ),
            text=[f"Scan {i+1}<br>{ts}<br>{count} defects" 
                  for i, (ts, count) in enumerate(zip(timestamps, detection_counts))],
            hovertemplate='<b>%{text}</b><extra></extra>'
        ))
        
        # Add threshold line at 0
        fig_trend.add_hline(
            y=0, 
            line_dash="dash", 
            line_color="rgba(34, 197, 94, 0.5)",
            annotation_text="Safe Threshold",
            annotation_position="right"
        )
        
        fig_trend.update_layout(
            title=dict(
                text="Detection Count Over Time",
                font=dict(size=18, color='#a5b4fc')
            ),
            xaxis_title="Scan Number",
            yaxis_title="Number of Defects Detected",
            template="plotly_dark",
            height=400,
            plot_bgcolor='rgba(30, 27, 75, 0.5)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#a5b4fc'),
            hovermode='x unified',
            margin=dict(t=60, b=50, l=50, r=100)
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Summary statistics for history
        total_detections_history = sum(detection_counts)
        avg_detections = total_detections_history / len(detection_counts)
        scans_with_defects = sum(1 for count in detection_counts if count > 0)
        
        hist_col1, hist_col2, hist_col3 = st.columns(3)
        with hist_col1:
            st.metric("Total Historical Detections", total_detections_history)
        with hist_col2:
            st.metric("Average per Scan", f"{avg_detections:.1f}")
        with hist_col3:
            st.metric("Scans with Defects", f"{scans_with_defects}/{len(detection_counts)}")


# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #a5b4fc; padding: 20px;">
    <p style="margin: 0;">Powered by SENTRYX AI | Real-time Infrastructure Monitoring</p>
    <p style="margin: 5px 0; font-size: 0.9rem;">🛡️ Protecting Infrastructure with Advanced AI Detection</p>
</div>
""", unsafe_allow_html=True)
