# 🚀 EcoAgent Quick Start Guide

Get EcoAgent running in 3 minutes!

---

## Step 1: Get Your NVIDIA API Key (2 minutes)

1. Go to [https://build.nvidia.com/](https://build.nvidia.com/)
2. Sign in or create an account (it's free!)
3. Navigate to any model (e.g., "Nemotron VLM")
4. Click "Get API Key" button
5. Copy your API key

---

## Step 2: Configure EcoAgent (30 seconds)

1. Open the `.env` file in the `ecoagent` folder
2. Replace `your_api_key_here` with your actual API key:
   ```
   NVIDIA_API_KEY=nvapi-xxxxxxxxxxxxxxxxxxxxx
   ```
3. Save the file

---

## Step 3: Install & Run (30 seconds)

### Option A: Using the run script (Mac/Linux)

```bash
chmod +x run.sh
./run.sh
```

### Option B: Manual installation

```bash
# Install dependencies
pip install -r requirements.txt

# Run the web interface
streamlit run ui/dashboard.py
```

---

## Step 4: Use EcoAgent! 🎉

1. Your browser will open automatically to `http://localhost:8501`
2. Upload an image of waste or pollution
3. Enter the location
4. Click "🚀 Analyze Image"
5. View your AI-generated environmental report!

---

## 🧪 Test Your Setup

Before uploading images, verify everything works:

```bash
python test_agent.py
```

This will check:
- ✅ API key is configured
- ✅ All modules load correctly
- ✅ EcoAgent initializes properly

---

## 💡 Tips

- **First run takes longer** - Models need to load
- **Use clear images** - Better quality = better analysis
- **Be specific with location** - Helps with report accuracy
- **Try different waste types** - See the full range of capabilities

---

## 🆘 Need Help?

**Problem: "NVIDIA_API_KEY not found"**
- Make sure you saved the `.env` file after adding your key

**Problem: "Module not found"**
- Run `pip install -r requirements.txt` again

**Problem: Streamlit won't start**
- Try: `python -m streamlit run ui/dashboard.py`

**Problem: Analysis takes too long**
- First run is slower - subsequent runs are faster
- Check your internet connection

---

## 📚 Learn More

- See `README.md` for full documentation
- Explore the code in the `tools/` folder
- Check out individual modules in `utils/`

---

**Ready to make a difference? Let's go! 🌍**
