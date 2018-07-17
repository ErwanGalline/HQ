# HQ hotel deduper
* docker : containes dockerfile with libpostal and lieu dependencies
* src : all code for deduing and evaluation
* resources/fields_mappers : contains field mappings for Geojson conversion

### Requierements
* Run `pip install -r requirements.txt` from src folder
* Build Docker image from Dockerfile 
### How to
Run API script passing pairs of input file (as CSV) with corresponding fields mapping description file (see about) and output folder
```
python hq_deduper_api .../../mysource_1.csv ../../mapper_1.json .../../mysource_2.csv ../../mapper_2.json -o ../../outputs/
```
