# Blood Donation Eligibility Prediction Model API

## 🏗️ **Project Structure**

```
.
├── config.py              # App configuration
├── ai.py                  # AI model
├── data/                  # Data storage
│   └── preprocessed/      # Pre-processed data
├── main.py                # Application entry point
├── docker-compose.yaml    # Ready to use docker compose file
├── Dockerfile             # Container configuration
├── pyproject.toml         # Project metadata & dependencies
```

## 🛠️ **Deployment Guide**  

### **Prerequisites**  
- **Python 3.11+** ([Download](https://python.org))  
- **Docker** (Optional) ([Install Docker](https://docs.docker.com/get-started/get-docker/))  
- **UV** (Optional, for fast Python management) ([Install UV](https://docs.astral.sh/uv/getting-started/installation/))  

### **Setup Instructions**  

1️⃣ **Add Dataset**  
   - Place the pre-processed dataset `dataset.xlsx` in `data/preprocessed/`.  

2️⃣ **Install Dependencies**  
   ```sh
   pip install .
   ```

3️⃣ **Run the App**  
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

4️⃣ **Access the API documentation**  
   Open your browser at:  
   🔗 [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  

