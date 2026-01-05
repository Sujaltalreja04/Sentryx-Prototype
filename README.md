# 🛡️ SENTRYX - AI Infrastructure Monitoring Dashboard

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> AI-Powered Infrastructure Defect Detection System with Real-time Alerts and Analytics

![SENTRYX Dashboard](https://via.placeholder.com/800x400/0f0c29/667eea?text=SENTRYX+Dashboard)

## 🌟 Features

### 🎯 Core Capabilities
- **AI-Powered Detection** - Custom YOLOv8 model trained for infrastructure defects
- **Real-time Alerts** - Instant notifications when defects are detected
- **Interactive Analytics** - 6 comprehensive graphs for data visualization
- **Trend Analysis** - Track detection patterns over time
- **Professional UI/UX** - Modern dark theme with glassmorphism effects

### 📊 Analytics Dashboard
- **Confidence Distribution** - Bar charts showing detection confidence levels
- **Severity Breakdown** - Donut charts categorizing defect severity
- **Defect Type Analysis** - Distribution of different defect types
- **Historical Trends** - Line charts tracking detections over time
- **Statistical Metrics** - Average, max, min, and standard deviation

### 🚨 Alert System
- Color-coded notifications (Red: Critical, Green: Safe)
- Timestamp tracking
- Confidence threshold display
- Status badges for quick identification

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/sentryx-dashboard.git
cd sentryx-dashboard
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run infra.py
```

4. **Open your browser**
```
http://localhost:8501
```

## 🌐 Deploy to Streamlit Cloud

### Option 1: One-Click Deploy

[![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy)

### Option 2: Manual Deployment

1. **Push to GitHub**
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/sentryx-dashboard.git
git push -u origin main
```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository
   - Set main file: `infra.py`
   - Click "Deploy"

## 📖 Usage

### 1. Upload Image
- Click the "Browse files" button
- Select an infrastructure image (JPG, JPEG, PNG)
- Wait for AI analysis (1-3 seconds)

### 2. View Results
- See original vs detection comparison
- Check alert notification
- Review detection details table

### 3. Analyze Data
- Explore interactive graphs
- Check confidence levels
- Review severity distribution
- Analyze defect types

### 4. Track History
- View past scans
- Analyze trends over time
- Monitor detection patterns

## 🎨 Screenshots

### Main Dashboard
![Dashboard](https://via.placeholder.com/800x400/0f0c29/667eea?text=Main+Dashboard)

### Detection Results
![Detection](https://via.placeholder.com/800x400/0f0c29/ef4444?text=Detection+Results)

### Analytics Graphs
![Analytics](https://via.placeholder.com/800x400/0f0c29/22c55e?text=Analytics+Graphs)

## 🛠️ Technology Stack

### Backend
- **Python** - Core programming language
- **Ultralytics YOLO** - Object detection framework
- **OpenCV** - Image processing
- **NumPy** - Numerical computations

### Frontend
- **Streamlit** - Web application framework
- **Plotly** - Interactive visualizations
- **Custom CSS** - Modern UI styling

### AI Model
- **YOLOv8** - State-of-the-art object detection
- **Custom Training** - Specialized for infrastructure defects
- **High Accuracy** - Optimized for crack and damage detection

## 📊 Graph Types

| Graph | Purpose | When Shown |
|-------|---------|------------|
| Confidence Bar Chart | Shows detection confidence levels | When defects found |
| Severity Donut Chart | Categorizes by severity | When defects found |
| Defect Type Chart | Distribution of defect types | When multiple types |
| Trend Line Chart | Historical detection patterns | After 2+ scans |
| Statistics Metrics | Statistical summary | When defects found |

## 🎯 Use Cases

### Infrastructure Managers
- Monitor structural health
- Track maintenance effectiveness
- Prioritize repair work
- Generate inspection reports

### Maintenance Teams
- Identify critical defects
- Plan resource allocation
- Focus on high-priority issues
- Track repair progress

### Civil Engineers
- Assess structural integrity
- Analyze defect patterns
- Predict maintenance needs
- Document infrastructure condition

## ⚙️ Configuration

### Adjust Detection Sensitivity
Use the sidebar slider to control confidence threshold:
- **Lower (0.01-0.25)** - More sensitive, detects more defects
- **Medium (0.25-0.50)** - Balanced detection
- **Higher (0.50-1.00)** - Only obvious defects

### Theme Customization
Edit `.streamlit/config.toml` to customize colors:
```toml
[theme]
primaryColor="#667eea"
backgroundColor="#0f0c29"
secondaryBackgroundColor="#302b63"
textColor="#a5b4fc"
```

## 📁 Project Structure

```
sentryx-dashboard/
├── infra.py                    # Main application
├── microsoft infra.pt          # AI model (custom trained)
├── requirements.txt            # Python dependencies
├── packages.txt               # System dependencies
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── .gitignore                 # Git ignore rules
├── README.md                  # This file
├── QUICK_START.md            # Quick reference guide
├── GRAPHS_DOCUMENTATION.md   # Graph details
└── DEPLOYMENT_GUIDE.md       # Deployment instructions
```

## 🔧 Troubleshooting

### Model Not Loading
- Ensure `microsoft infra.pt` is in the project root
- Check file permissions
- Verify file size (should be ~22MB)

### Performance Issues
- Use smaller images (<5MB)
- Close unnecessary browser tabs
- Clear browser cache
- Use Chrome or Edge browser

### No Detections
- Lower confidence threshold
- Ensure image shows clear defects
- Check image quality and lighting

## 📈 Performance

- **Load Time:** 1-2 seconds
- **Detection Speed:** 1-3 seconds per image
- **Graph Rendering:** <1 second
- **Memory Usage:** ~500MB
- **Supported Image Size:** Up to 10MB

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Name](https://linkedin.com/in/yourprofile)

## 🙏 Acknowledgments

- Ultralytics for the YOLO framework
- Streamlit for the amazing web framework
- Plotly for interactive visualizations

## 📞 Support

For support, email your-email@example.com or open an issue on GitHub.

## 🔮 Future Enhancements

- [ ] PDF report generation
- [ ] Email notifications
- [ ] Multi-image batch processing
- [ ] 3D visualization
- [ ] Mobile app
- [ ] API integration
- [ ] Database storage
- [ ] User authentication

---

**Made with ❤️ for Infrastructure Safety**

[![Star this repo](https://img.shields.io/github/stars/yourusername/sentryx-dashboard?style=social)](https://github.com/yourusername/sentryx-dashboard)
