# Blood Donation Dashboard

## 🏗️ **Project Structure**

```
.
├── config.py              # App configuration
├── dashboard/             # Dashboard components
│   └── __init__.py        # Layout definitions
├── data/                  # Data storage
│   └── preprocessed/      # Processed data (auto-generated)
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

**Install Dependencies**  
   ```sh
   pip install .
   ```

**Run the App**  
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

**Access Dashboard**  
   Open your browser at:  
   🔗 [http://127.0.0.1:8050/](http://127.0.0.1:8050/)  

**Confif the API url (optional)**

    In case the you want to use an API for the Eligibility prediction model, you can set it as a environment variable like below.

    ```sh
    ELIGIBILITY_PREDICTION_API=https://example.com
    ```
