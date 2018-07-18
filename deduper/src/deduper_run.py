from metrics import Metrics
from geojson_parser import Parser
import os

to_process = []

# Config
DEDUPE_SCRIPT = '/home/erwan/Work/NFQ/HQ/deduper/src/dedupe_geojson.py'
DEDUPE_OUTPUTS_FOLDER = '/home/erwan/Desktop/hotel_test_set/outputs/'

FIELD_MAP_1 = '/home/erwan/Work/NFQ/HQ/deduper/resources/fields_mappers/ean_map.json'
INPUT_1 = '/home/erwan/Work/NFQ/HQ/data/Confident.csv'
GEOJSON_OUTPUT_1 = '/home/erwan/Desktop/hotel_test_set/ean.geojson'

FIELD_MAP_2 = '/home/erwan/Work/NFQ/HQ/deduper/resources/fields_mappers/hq_map.json'
INPUT_2 = '/home/erwan/Work/NFQ/HQ/data/hotel_full_invent_june18.csv'
GEOJSON_OUTPUT_2 = '/home/erwan/Desktop/hotel_test_set/hq.geojson'

# geojson parser 1
ean_parser = Parser(FIELD_MAP_1, INPUT_1, GEOJSON_OUTPUT_1, None, None)
ean_geojson = ean_parser.run()
to_process.append(GEOJSON_OUTPUT_1)
#
# # geojson parser 2
hq_parser = Parser(FIELD_MAP_2, INPUT_2, GEOJSON_OUTPUT_2, None, None)
hq_parser.run()
to_process.append(GEOJSON_OUTPUT_2)

# Run lieu deduper using above geojson list and '--name-only' option
file_list = ' '.join(' ' + geojson for geojson in to_process)

argsStr = file_list + ' -o ' + DEDUPE_OUTPUTS_FOLDER + ' --name-only'
cmd_str = ''.join(['python', ' ', DEDUPE_SCRIPT, ' ', argsStr])
os.system(cmd_str)

