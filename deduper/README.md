# HQ hotel deduper

* /docker : contains docker file with Libpostal and Lieu library installation command
* /src : implementation for CSV to Geojson parser, lieu deduper and solution evaluation
* /resources/fields_mappers : field mappings for Geojson parsing

### Requierements

* Run `pip install -r requirements.txt` from src folder
* Build Docker image from Dockerfile 

### How to run
##### 1. Evaluation

Edit and run `evaluation_run.py` script : you have to set 2 input files (CSV) and corresponding field mapping fields (JSON).
You can choose how many items you want to run evaluation on (dataset size) : `BIND_LIST_SIZE`.


Edit `SIMILARITY_THRESHOLD` and `DISTANCE_THRESHOLD_METERS` thresholds to make precision and recall vary.

##### 2. Deduper 

Edit and run `deduper_run.py` script : you have to set 1 or n input files (CSV) and corresponding field mapping fields (JSON).
    
