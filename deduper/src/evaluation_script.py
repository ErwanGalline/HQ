from metrics import Metrics
from geojson_parser import Parser
import os

# Config
DEDUPE_SCRIPT = '/home/erwan/Work/NFQ/HQ/deduper/src/dedupe_geojson.py'

FIELD_MAP_1 = '/home/erwan/Work/NFQ/HQ/deduper/resources/fields_mappers/ean_map.json'
INPUT_1 = '/home/erwan/Work/NFQ/HQ/data/Confident.csv'
GEOJSON_OUTPUT_1 = '/home/erwan/Desktop/hotel_test_set/ean.geojson'

FIELD_MAP_2 = '/home/erwan/Work/NFQ/HQ/deduper/resources/fields_mappers/hq_map.json'
INPUT_2 = '/home/erwan/Work/NFQ/HQ/data/hotel_full_invent_june18.csv'
GEOJSON_OUTPUT_2 = '/home/erwan/Desktop/hotel_test_set/hq.geojson'

DEDUPE_OUTPUTS_FOLDER = '/home/erwan/Desktop/hotel_test_set/outputs/'

# Source geojson parser
ean_parser = Parser(FIELD_MAP_1, INPUT_1, GEOJSON_OUTPUT_1, 1000, None)
ean_geojson = ean_parser.run()

# Target geojson parser
hq_parser = Parser(FIELD_MAP_2, INPUT_2, GEOJSON_OUTPUT_2, None, ean_geojson)
hq_parser.run()

# Run lieu deduper using above geojson list and '--name-only' option
argsStr = GEOJSON_OUTPUT_1 + ' ' + GEOJSON_OUTPUT_2 + ' -o ' + DEDUPE_OUTPUTS_FOLDER + ' --name-only'
cmd_str = ''.join(['python', ' ', DEDUPE_SCRIPT, ' ', argsStr])
os.system(cmd_str)

# Calculate metrics
matcher = Metrics(DEDUPE_OUTPUTS_FOLDER + "/deduped.geojson", GEOJSON_OUTPUT_1, GEOJSON_OUTPUT_2, 0.9, 100)
matcher.analyseFeature()
