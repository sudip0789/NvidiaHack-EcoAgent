# 🚀 START HERE - EcoAgent Setup

## Welcome to EcoAgent! 🌍

Your complete NVIDIA Nemotron-powered environmental reporting system is ready.

---

## ⚡ 3-Step Quick Start

### Step 1: Get Your API Key (2 minutes)

1. Visit: **https://build.nvidia.com/**
2. Sign in (free account)
3. Go to any model page
4. Click **"Get API Key"**
5. Copy your key (starts with `nvapi-`)

### Step 2: Configure (30 seconds)

Open the `.env` file and paste your API key:

```bash
NVIDIA_API_KEY=nvapi-paste-your-key-here
```

**⚠️ Important:** Replace `your_api_key_here` with your actual key!

### Step 3: Run (30 seconds)

```bash
# Make script executable (first time only)
chmod +x run.sh

# Launch EcoAgent
./run.sh
```

The browser will open automatically! 🎉

---

## 📱 Alternative: Manual Start

```bash
# Install dependencies
pip install -r requirements.txt

# Launch web interface
streamlit run ui/dashboard.py
```

---

## ✅ Verify Setup

Before uploading images, test your installation:

```bash
python3 test_agent.py
```

Expected output:
```
✅ NVIDIA_API_KEY found
✅ eco_agent module
✅ tools module
✅ utils module
✅ EcoAgent initialized successfully
```

---

## 🎯 What to Do Next

### 1. Open the Web Interface
- Should auto-open at `http://localhost:8501`
- If not, copy the URL from terminal

### 2. Upload a Test Image
- Click "Browse files"
- Select any image of waste or pollution
- See the preview

### 3. Enter Location
- Type where the waste is located
- Example: "Main Street Park"

### 4. Click Analyze
- Wait 30-60 seconds (models are processing!)
- Watch the progress indicator

### 5. Explore Results
- **Full Report** tab - Complete civic report
- **Classification** tab - Waste type details  
- **Severity** tab - Risk assessment
- **Raw Data** tab - JSON output

### 6. Download Report
- Click "📥 Download Full Report"
- Save for submission to authorities

---

## 📚 Documentation Quick Links

| I want to... | Read this... |
|--------------|--------------|
| Get started quickly | `QUICKSTART.md` |
| Learn all features | `README.md` |

---

## 🎨 Features at a Glance

✨ **AI-Powered Analysis**
- Waste classification using Nemotron VLM
- Severity assessment with AI reasoning
- Professional report generation

🖼️ **Image Analysis**
- 13+ waste categories
- Confidence scoring
- Item identification

⚠️ **Severity Levels**
- Critical to Minimal (5 levels)
- Health risk assessment
- Response time recommendations

📝 **Professional Reports**
- Executive summary
- Detailed findings
- Recommended actions
- Downloadable format

🎯 **Easy to Use**
- Beautiful web interface
- Drag & drop upload
- Real-time progress
- Multi-tab results

---

## 🔧 Troubleshooting

### "NVIDIA_API_KEY not found"
➡️ Edit `.env` file and add your key

### "Module not found" 
➡️ Run: `pip install -r requirements.txt`

### "Permission denied: ./run.sh"
➡️ Run: `chmod +x run.sh`

### "Streamlit command not found"
➡️ Try: `python3 -m streamlit run ui/dashboard.py`

### Analysis takes too long
➡️ First run is slower; be patient (30-60 seconds is normal)

### Results seem inaccurate
➡️ Use clearer images with better lighting

---

## 💻 Command Line Interface

Prefer terminal? Use the CLI:

```bash
python3 eco_agent.py path/to/image.jpg "Location description"
```

Example:
```bash
python3 eco_agent.py waste_photo.jpg "Central Park, NYC"
```

---

## 🐍 Python API

Want to integrate into your code?

```python
from eco_agent import EcoAgent

# Initialize
agent = EcoAgent(verbose=True)

# Analyze
results = agent.analyze_image(
    image_path_or_bytes="waste_image.jpg",
    location="Downtown City Center",
    additional_notes="Large accumulation"
)

# Get report
report = agent.get_formatted_report(results)
print(report)
```

---

## 🎓 Quick Tips

1. **Use Good Images** - Clear, well-lit, close-up shots work best
2. **Be Specific** - Detailed location helps generate better reports
3. **Add Context** - Use the notes field for extra observations
4. **Try Both Modes** - Toggle AI vs rule-based severity in settings
5. **Save Reports** - Download reports for record-keeping

---

## 📊 What It Analyzes

### Waste Types
- Plastic, Glass, Metal
- E-waste, Hazardous materials
- Organic waste, Construction debris
- Water/Air pollution
- And more...

### Assessment Includes
- Primary waste type
- Confidence level
- Visible items
- Severity score (1-5)
- Health risks
- Environmental impact
- Recommended response time
- Specific actions needed

---

## 🚀 Project Structure

```
ecoagent/
├── 🎯 eco_agent.py           # Main orchestrator
├── 🧪 test_agent.py           # Test suite
├── ▶️  run.sh                  # Quick launch
│
├── 🛠️  tools/                  # AI tools
│   ├── waste_classifier.py   # VLM classification
│   ├── severity_estimator.py # Severity AI
│   └── report_generator.py   # Report AI
│
├── 🎨 ui/
│   └── dashboard.py          # Web interface
│
├── 🔧 utils/
│   └── helpers.py            # API functions
│
└── 📚 Documentation/
    ├── README.md
    ├── QUICKSTART.md
    ├── PROJECT_STRUCTURE.md
    ├── SUMMARY.md
    └── START_HERE.md (this file)
```

---

## 🤖 Models Used

1. **nvidia/llama-3.1-nemotron-nano-vl-8b-v1**
   - Image understanding
   - Waste classification
   
2. **nvidia/nvidia-nemotron-nano-9b-v2**
   - Fast reasoning
   - Severity assessment
   
3. **nvidia/llama-3_3-nemotron-super-49b-v1_5**
   - Report generation
   - Professional writing

---

## 🎯 Success Checklist

Before you start analyzing:

- [ ] API key configured in `.env`
- [ ] Dependencies installed
- [ ] Test script passes
- [ ] Web interface opens
- [ ] Ready to upload images!

---

## 🌟 You're All Set!

Everything is configured and ready. Launch EcoAgent and start making a difference! 🌱

```bash
./run.sh
```

**Questions?** Check the documentation files listed above.

**Issues?** Run `python3 test_agent.py` to diagnose.

**Ready?** Let's analyze some waste and generate reports! 🚀

---

**Powered by NVIDIA Nemotron**
