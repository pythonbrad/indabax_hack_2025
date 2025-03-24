# 🏆 IndabaX Hackathon 2025: Blood Donation Dashboard  

**📊 A Python-powered dashboard for visualizing and analyzing blood donation campaign data.**  

![Dashboard Preview](https://github.com/user-attachments/assets/360d09ef-e094-4c6f-aa9e-128bc119e542)

## 🚀 **Team TechSpectra**  

| Member            | Role                     | GitHub                                         |  
|-------------------|--------------------------|------------------------------------------------|  
| Brady Fomegne     | DevOps Developer         | [@pythonbrad](https://github.com/pythonbrad)   |  
| Brayan Weko       | Software Developer       | [@brayan-weko](https://github.com/brayan-weko) |  
| Melvin Awe        | Team Lead                | [@kingmam237](https://github.com/kingmam237)   |  
| Gamuah Ryane      | Analyst                  | [@joyryane](https://github.com/joyryane)       |  

## 🔥 **Live Demo**  
Experience our interactive dashboard here:  
👉 **[https://ixh24-tech-spectra.onrender.com](https://ixh24-tech-spectra.onrender.com)**  

⚠️ **Heads up!**  
*This is a free-hosted demo. If the page takes ~60 seconds to load or look inactive, just wait—it’s waking up from inactivity! Refresh if needed.*  
*(For faster testing, consider [local deployment](#-deployment-guide).)*  

## 📖 **User Manual**
Consult our [`USER-MANUAL.md`](USER-MANUAL.md) to understand more about how to use how dashboard. 

## 🤔 **Assumptions**
Some of our assumptions and decision are available at [`ASSUMPTION.md`](ASSUMPTION.md).

---

## 🏗️ **Project Structure**

```
.
├── config.py              # App configuration
├── dashboard/             # Dashboard components
│   └── __init__.py        # Layout definitions
├── data/                  # Data storage
│   ├── raw/               # 📌 Raw datasets (place dataset.xlsx here)
│   ├── geo/               # Geographic files (shapefiles)
│   └── preprocessed/      # Processed data (auto-generated)
├── preprocess/            # Data pipeline
│   ├── __init__.py
│   └── utils.py           # Cleaning/transformation functions
├── main.py                # Application entry point
├── docker-compose.yaml    # Ready to use docker compose file
├── Dockerfile             # Container configuration
├── pyproject.toml         # Project metadata & dependencies
```

## 🛠️ **Deployment Guide**  

### **Prerequisites**  
- **Python 3.11+** ([Download](https://python.org))  
- **Cameroon Admin Boundaries** ([Download Shapefiles](https://data.humdata.org/dataset/cod-ab-cmr))  
- **Docker** (Optional) ([Install Docker](https://docs.docker.com/get-started/get-docker/))  
- **UV** (Optional, for fast Python management) ([Install UV](https://docs.astral.sh/uv/getting-started/installation/))  

### **Setup Instructions**  

1️⃣ **Add Dataset**  
   - Place `dataset.xlsx` in `data/raw/`.  

2️⃣ **Download & Extract Geo-Data**  
   - Get it at [`cmr_admbnda_inc_20180104_shp.zip`](https://data.humdata.org/...).  
   - Extract into `data/geo/`.  

3️⃣ **Install Dependencies**  
   ```sh
   pip install .
   ```

4️⃣ **Run the App**  
   - **With Python:**  
     ```sh
     python main.py
     ```  
   - **With UV (Faster):**  
     ```sh
     uv run main.py
     ```  
   - **With Docker:**  
     ```sh
     docker compose up -d
     ```  

5️⃣ **Access Dashboard**  
   Open your browser at:  
   🔗 [http://127.0.0.1:8050/](http://127.0.0.1:8050/)  

---

## 📜 **License**  
This project is open-source under the **[MIT License](LICENSE)**.  
