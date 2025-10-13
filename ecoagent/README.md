# 🌍 EcoAgent

**AI-Powered Environmental Reporting System**

EcoAgent is an intelligent application that analyzes images of waste and pollution, classifies environmental issues, estimates severity, and generates professional civic reports for environmental authorities—all powered by NVIDIA Nemotron models.

---

## 🎯 Features

- **🔍 Intelligent Waste Classification** - Uses Nemotron nano vl 8B for accurate image analysis
- **⚠️ Severity Assessment** - LLM based and Rule-based severity estimation
- **📝 Automated Report Generation** - Professional civic reports using Nemotron LLM
- **🎨 Beautiful Streamlit UI** - User-friendly web interface
- **🏗️ Modular Architecture** - Clean, maintainable, MCP-style agent design

---

## 🤖 NVIDIA Models Used

1. **nvidia/llama-3.1-nemotron-nano-vl-8b-v1** - Vision-language model for image analysis
2. **nvidia/nvidia-nemotron-nano-9b-v2** - Lightweight model for severity reasoning
3. **nvidia/llama-3_3-nemotron-super-49b-v1_5** - Powerful model for report generation

---

## 📁 Project Structure

```
ecoagent/
├── eco_agent.py                 # Main orchestrator (agent)
├── tools/
│   ├── __init__.py
│   ├── waste_classifier.py      # Nemotron VLM classification
│   ├── severity_estimator.py    # Severity assessment
│   └── report_generator.py      # Report generation
├── ui/
│   ├── __init__.py
│   └── dashboard.py             # Streamlit interface
├── utils/
│   ├── __init__.py
│   └── helpers.py               # NVIDIA API calls
├── .env                         # API key configuration
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- NVIDIA API key (get one at [build.nvidia.com](https://build.nvidia.com/))

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd ecoagent
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your API key:**
   
   Edit the `.env` file and add your NVIDIA API key:
   ```
   NVIDIA_API_KEY=your_actual_api_key_here
   ```

### Running the Application

#### Option 1: Streamlit Web Interface (Recommended)

```bash
streamlit run ui/dashboard.py
```

Then open your browser to `http://localhost:8501`

#### Option 2: Command Line Interface

```bash
python eco_agent.py path/to/image.jpg "Location Description"
```

Example:
```bash
python eco_agent.py waste_photo.jpg "Central Park, New York"
```

---

## 🎨 Using the Web Interface

1. **Upload Image** - Click "Browse files" and select an image of waste or pollution
2. **Enter Location** - Provide the location where the issue was observed
3. **Add Notes** (Optional) - Include any additional context
4. **Analyze** - Click the "🚀 Analyze Image" button
5. **View Results** - Explore the generated report in multiple tabs

### Interface Features

- **Analysis Summary** - Quick overview with key metrics
- **Full Report** - Complete civic report ready for submission
- **Classification Details** - Detailed waste type analysis
- **Severity Assessment** - Risk evaluation and urgency
- **Raw Data** - JSON view of all analysis data
- **Download Report** - Export report as text file

---

## 🔧 Configuration

### Environment Variables

Create or edit `.env` file:

```env
NVIDIA_API_KEY=your_api_key_here
```

### Settings (in Streamlit UI)

- **Use AI for severity estimation** - Toggle between LLM and rule-based severity assessment

---

## 🧪 Example Usage

### Python API

```python
from eco_agent import EcoAgent

# Initialize agent
agent = EcoAgent(verbose=True)

# Analyze image
results = agent.analyze_image(
    image_path_or_bytes="waste_image.jpg",
    location="Downtown City Center",
    additional_notes="Large accumulation near water source"
)

# Get formatted report
report = agent.get_formatted_report(results)
print(report)
```

### Individual Tools

```python
from utils.helpers import encode_image_to_base64
from tools.waste_classifier import classify_waste
from tools.severity_estimator import estimate_severity
from tools.report_generator import generate_civic_report

# Encode image
image_base64 = encode_image_to_base64("image.jpg")

# Classify waste
classification = classify_waste(image_base64)

# Estimate severity
severity = estimate_severity(classification, location="City Park")

# Generate report
report = generate_civic_report(classification, severity, location="City Park")
```

---

## 📊 Supported Waste Categories

- Plastic waste
- Organic waste
- Electronic waste (e-waste)
- Metal waste
- Glass waste
- Paper/Cardboard waste
- Textile waste
- Hazardous waste (chemicals, batteries)
- Construction debris
- General litter/mixed waste
- Water pollution (oil, sewage)
- Air pollution (smoke, emissions)
- Other

---

## ⚠️ Severity Levels

| Level | Score | Description | Response Time |
|-------|-------|-------------|---------------|
| **Critical** | 5 | Immediate threat to public health or environment | Within 24 hours |
| **High** | 4 | Significant environmental or health concern | Within 3 days |
| **Medium** | 3 | Moderate concern requiring attention | Within 1 week |
| **Low** | 2 | Minor issue, routine cleanup needed | Within 2 weeks |
| **Minimal** | 1 | Minimal impact, preventive action suggested | As resources permit |

---

## 🛠️ Architecture

EcoAgent follows an MCP (Model Context Protocol) style agent architecture:

```
┌─────────────────────────────────────────┐
│          EcoAgent Orchestrator          │
│         (eco_agent.py)                  │
└────────────┬────────────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
    ▼                 ▼
┌─────────┐      ┌──────────┐
│  Tools  │      │   Utils  │
└─────────┘      └──────────┘
    │                 │
    ├─ Classifier     ├─ API Helpers
    ├─ Estimator      ├─ Image Encoding
    └─ Generator      └─ JSON Parsing
```

### Design Principles

- **Modularity** - Each tool is independent and reusable
- **Error Handling** - Graceful fallbacks at every stage
- **API Abstraction** - Easy to swap or mock API calls
- **Clean Code** - Well-documented with type hints
- **Extensibility** - Easy to add new tools or models

---

## 🚧 Future Enhancements

- [ ] Multi-image analysis
- [ ] GPS coordinate integration
- [ ] Historical trend analysis
- [ ] Direct submission to authorities
- [ ] Mobile app version
- [ ] Offline mode with local models
- [ ] Multi-language support
---

## 🤝 Contributing

This project is created for the NVIDIA Hackathon 2025, but suggestions are welcome!

---
