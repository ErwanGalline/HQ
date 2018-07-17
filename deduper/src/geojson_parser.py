import csv
import json
import logging
import sys

from postal.parser import parse_address

from fields_mapper import FieldsMapper
from utils import Utils

log = logging.getLogger(__name__)
csv.field_size_limit(sys.maxsize)


class Parser(object):
    def __init__(self, fields_mapper_file, input, output, limit=None, bind_geojson=None):
        self.fields_mapper = FieldsMapper(fields_mapper_file)
        self.input = input
        self.output = output
        self.item_limit = limit
        self.bind_list = Utils.get_binding_list(bind_geojson) if bind_geojson is not None else None
        print("INFO :: GeoJson parser initialized for file  " + self.input)
        if self.item_limit is not None:
            print("INFO :: [Evaluation Mode] Parser will export the " + str(self.item_limit) + " first rows from file.")
        if self.bind_list is not None:
            print("INFO :: [Evaluation Mode] Parser will export the items matching to input binding list (lenght : " + str(len(self.bind_list)) + ")")

    def parseCsv(self):
        log.info("Parsing CSV ::" + self.input)
        with open(self.input) as csvfile:
            if self.fields_mapper.delimiter is not None:
                reader = csv.DictReader(csvfile, delimiter=self.fields_mapper.delimiter)
            else:
                reader = csv.DictReader(csvfile)
            cols = self.fields_mapper.columns
            geojson_list = self.toGeoJson(reader, cols)
        return geojson_list

    def toGeoJson(self, reader, cols):
        geojson = {'type': 'FeatureCollection', 'features': []}
        i = 0
        err = 0
        for row in reader:
            # to avoid duplicate entries in evaluation mode
            if (self.item_limit is not None)  and (self.isContain(geojson, row[cols['ref_id']].encode('utf-8'))):
                continue
            # if bind list not null means we are running evaluation
            if (self.bind_list is not None) and (row[cols['bind_id'].encode('utf-8')].encode('utf-8') not in self.bind_list):
                continue
            else:
                try:
                    lon = float(row[cols['lon']])
                    lat = float(row[cols['lat']])
                    name = row[cols['name']]
                    address = row[cols['address']]
                    parsed = parse_address(row[cols['address']])
                    try:
                        city = row[cols['city']]
                    except:
                        city = self.getDataFromLibpostal(parsed, 'city')

                    try:
                        zip = row[cols['zip_code']]
                    except:
                        zip = self.getDataFromLibpostal(parsed, 'postcode')

                    try:
                        country = row[cols['country']]
                    except:
                        country = self.getDataFromLibpostal(parsed, 'country')

                    try:
                        number = row[cols['number']]
                    except:
                        number = self.getDataFromLibpostal(parsed, 'house_number')

                    try:
                        street = row[cols['street']]
                    except:
                        street = self.getDataFromLibpostal(parsed, 'road')

                    ref = row[cols['ref_id']]

                    if (self.bind_list is not None):
                        bind_id = row[cols['bind_id']]
                    else:
                        bind_id = ""

                    feature = self.createFeature(lon, lat, name, zip, city, country, address, number, street, ref,
                                                 bind_id)
                    geojson['features'].append(feature)
                    i += 1

                    # if limit is not null means we are doing evaluation (test on limited amount of item )
                    if ((self.item_limit is not None) and (i >= self.item_limit)) or (
                            (self.bind_list is not None) and (i >= len(self.bind_list))):
                        break

                except KeyError:
                    print("ERROR ::: Key error : key doesn't exists or value is empty.")
                    err += 1

                except UnicodeDecodeError:
                    print("ERROR ::: Error parsing row : " + str(row))
                    err += 1

                except:
                    print("ERROR ::: Row: " + str(row))
                    err += 1

        print("Total rows parsed :: " + str(i))
        print("Error parsing :: " + str(err))
        print("---------------------------")
        return geojson

    def getDataFromLibpostal(self, address_full_parsed, look_for):
        try:
            for item in address_full_parsed:
                elem = (item[0].encode('utf-8'), item[1].encode('utf-8'))
                if elem[1] == look_for:
                    return elem[0]
            return ""
        except:
            return ""

    def isContain(self, list, item_ref):

        for row in list['features']:
            if row['reference']['id'].encode('utf-8') == item_ref:
                return True
        return False

    def createFeature(self, lon, lat, name, zip, city, country, address, number, street, ref, ref_hq):

        feature = {'type': 'Feature',
                   'properties': {},
                   'reference': {},
                   'geometry': {'type': 'Point',
                                'coordinates': []}
                   }
        feature['geometry']['coordinates'] = [float(lon), float(lat)]
        feature['properties']['addr:full'] = address
        feature['properties']['addr:housenumber'] = number
        feature['properties']['addr:street'] = street
        feature['properties']['addr:postcode'] = zip
        feature['properties']['addr:city'] = city
        feature['properties']['addr:country'] = country
        feature['properties']['name'] = name

        feature['reference']['id'] = ref
        feature['reference']['bind_id'] = ref_hq

        return feature

    def exportGeoJson(self, listIn):
        output_filename = self.output
        with open(output_filename, 'wb') as output_file:
            json.dump(listIn, output_file, indent=4)

    def run(self):
        list = self.parseCsv()
        self.exportGeoJson(list)
        return list
