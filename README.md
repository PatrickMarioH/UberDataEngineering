# Uber Data Engineering End-To-End Project

This Repository Contains A Self‑Contained Data Engineering Pipeline That Simulates An Uber‑Like Ride‑Sharing Dataset, Ingests Streaming Data, And Builds Analytics Tables Using **PySpark** Pipelines. The Code Generates Synthetic Ride Confirmations, Streams Them Through Azure Event Hubs (Or Kafka), And Assembles Them With Historical Bulk Data Into A Medallion‑Style Architecture (Bronze → Silver → Gold) Inside A Lakehouse Environment.

The Goal Is To Demonstrate A Spark‑Centric, Code‑First Approach To Building Dimension And Fact Tables With Change‑Data‑Capture (CDC) And Slowly Changing Dimensions (SCDs).

## Architecture

### Data Flow
```
Synthetic Data Generator → Event Hub / Kafka → Bronze Layer (Raw Stream) \
          ↘                           ↘                       ↘
     Bulk_rides.json (Historical) → Silver Layer (Staging/OBT)   
                                              ↘
                                      Gold Layer (Dimensions & Facts)
```

### Technology Stack

- **Compute**: PySpark (Built On Databricks)
- **Streaming**: Azure Event Hubs (Kafka‑Compatible) Or Kafka
- **Data Generation**: `data.py` With Faker
- **Python Dependencies**: See `requirements.txt`
- **Static Reference Data**: JSON Files In `data/`
- **Notebook Examples**: `scripts/*.ipynb`

## Project Structure

```
UberDataEngineering/
├── README.md                # This File
├── connection.py            # Sends Generated Records To Event Hub
├── data.py                  # Synthetic Uber Ride Generator & Mappings
├── requirements.txt         # Python Dependencies
├── files_array.json         # Utility (Unused) Placeholder
├── data/                    # Reference And Bulk History Files
│   ├── bulk_rides.json      # Initial Dataset For Silver Layer
│   ├── map_*.json           # Lookup Tables (Cities, Vehicle Makes, Etc.)
│
├── scripts/                 # PySpark Pipelines And Notebooks
│   ├── ingest.py            # Bronze‑Layer Streaming Reader
│   ├── silver.py            # Merge Historical + Stream Into Staging (OBT)
│   ├── gold.py              # Build Dimensions & Fact Tables With CDC/SCD
│   ├── *.ipynb              # Example Notebooks Illustrating Usage
│   ├── silver_obt.sql       # SQL Version Of Silver/OBT Logic
└── __pycache__/             # Compiled Python Artifacts
```

## Data Model

The Pipeline Uses A Simplified Medallion Architecture:

- **Bronze**: Raw JSON Rides Consumed From Kafka/Event Hub (`rides_raw` Table)
- **Silver**: One Big Table (`stg_rides`) That Appends Bulk Historical Rides And Streaming Events
- **Gold**: CDC‑Driven Dimension Tables (`dim_passenger`, `dim_driver`, Etc.) And `fact` Table Built From The Silver Layer. All Gold Tables Are Configured As Streaming Tables With Auto‑CDC Flows In Spark Pipelines.

Lookup Mappings Under `data/` Provide Source Values For:
- Cities, Vehicle Makes/Types, Payment Methods, Ride Statuses, Cancellation Reasons

## Getting Started

### Prerequisites

1. **Python 3.8+** With A Virtual Environment
2. **Spark 3.x** Cluster (Databricks, Local Install, Or EMR)
3. **Azure Event Hubs** Or Kafka For Streaming (Optional If Only Using Bulk Data)

### Installation

```powershell
# Clone Repository
git clone <repo-url>
cd UberDataEngineering

# Create & Activate Virtualenv
python -m venv .venv
.venv\Scripts\Activate.ps1   # Windows PowerShell

# Install Dependencies
pip install -r requirements.txt
``` 

### Configuration

1. Copy `.env.example` (If Exists) To `.env` And Set:
   ```ini
   CONNECTION_STRING=<Your-Event-Hub-Connection>
   EVENT_HUBNAME=<Your-Hub-Name>
   ```
2. If Using Databricks, Configure Secrets Or Cluster Spark Config To Provide `connection_string` To The Notebook (Used By `ingest.py`).

### Running The Pipeline

1. **Start The Bronze Reader** (E.g. In A Notebook):
   ```python
   # ingest.py Defines rides_raw Streaming Table
   %run ./scripts/ingest.py
   ```
2. **Load Historical Data** (One‑Time):
   - Copy `data/bulk_rides.json` To A Spark Table Named `bulk_rides` (Managed Or External).
3. **Execute Silver Logic**:
   ```python
   %run ./scripts/silver.py
   ```
   This Creates `stg_rides` And Appends Both Sources.
4. **Build Gold Tables**:
   ```python
   %run ./scripts/gold.py
   ```
   This Constructs Streaming SCD Tables And The Fact Table.

Alternatively, Run The `.ipynb` Notebooks In `scripts/` For An Interactive Walkthrough.

## Key Features

- **Synthetic Data Generator** (`data.py`) That Returns Realistic Uber Ride Confirmations.
- **Event Hub/Kafka Ingestion** In `ingest.py` With Streaming Reader Configured For SASL/SSL.
- **Append‑Only Silver Layer** That Merges Bulk Historical JSON With Incoming Stream.
- **CDC/SCD Gold Layer** Using `dp.create_auto_cdc_flow` To Maintain Dimensions Automatically.
- **PySpark Pipelines API** (`pyspark.pipelines`) Drives Table And Flow Creation.

## Usage Notes

- Bulk Data Can Be Refreshed By Overwriting `bulk_rides` Table And Restarting Silver Pipeline.
- Lookup JSONs Can Be Updated And Re‑Ingested As New Dimension Records By Running Gold Pipeline Again.
- Notebooks Show How To Query The Streaming Tables With SQL Or DataFrame APIs.

## 📄 License

This Project Is For Educational Purposes And May Be Freely Used And Modified.