import json
import logging
import math

from lieu.input import GeoJSONParser, GeoJSONLineParser

log = logging.getLogger(__name__)


class Matcher(object):

    def __init__(self, file, geojson_1, geojson_2, threshold, distance_threshold=200):
        self.input = file
        self.threshold = threshold
        self.distance_threshold = distance_threshold
        self.data_set_size = self.calculate_data_set_size(geojson_1, geojson_2)

    def open_geojson_file(self, filename):
        try:
            f = GeoJSONLineParser(filename)
        except ValueError:
            f = GeoJSONParser(filename)
        return f

    def calculate_data_set_size(self, geojson_1, geojson_2):

        with open(geojson_1) as f1:
            g1 = json.load(f1)
        with open(geojson_2) as f2:
            g2 = json.load(f2)
        return min(len(g1['features']), len(g2['features']))

    def analyseFeature(self):
        file = self.open_geojson_file(self.input)
        print(":::Feature analyse start")
        it = 0
        true_pos = 0
        false_pos = 0
        same_as = 0
        while True:
            try:
                feature = file.next_feature()
                if ("same_as" in feature):
                    dupe = feature["same_as"]
                    tp, fp = self.verifySimilarity(feature["object"], dupe)
                    true_pos = true_pos + tp
                    false_pos = false_pos + fp
                    same_as += 1
                if ("possibly_same_as" in feature):
                    dupe = feature["possibly_same_as"]
                    tp, fp = self.verifySimilarity(feature["object"], dupe)
                    true_pos = true_pos + tp
                    false_pos = false_pos + fp
                    same_as += 1
                it += 1
            except StopIteration:
                break

        print("----------------------------")
        print("::: Feature analyse done :::")

        print("SIMILARITY THRESHOLD (%): " + str(self.threshold * 100))
        print("DISTANCE THRESHOLD (m): " + str(self.distance_threshold))

        print("Item analysed : " + str(it))
        print("Data set size :" + str(self.data_set_size))
        print("True positive :" + str(true_pos))
        print("False positive :" + str(false_pos))
        print(" ")
        precision = ((float(true_pos) / (float(true_pos) + float(false_pos))))
        print("Precision :" + str(precision * 100) + " %")
        recall = ((float(true_pos) / (float(true_pos) + ((self.data_set_size) - (float(true_pos) + float(false_pos))))))
        print("Recall :" + str(recall * 100) + " %")
        print("Same as :" + str(same_as))

    def verifySimilarity(self, item, dupeList):
        truePos = 0
        falsePos = 0
        real_dupe_list = []
        fake_dupe_list = []

        for potentialDupe in dupeList:
            p1 = (item['geometry']['coordinates'][0], item['geometry']['coordinates'][1])
            p2 = (potentialDupe['object']['geometry']['coordinates'][0],
                  potentialDupe['object']['geometry']['coordinates'][1])
            dist = self.distance(p1, p2)

            if potentialDupe["similarity"] > self.threshold and self.distance(p1, p2) < self.distance_threshold:
                if self.findRef(item, potentialDupe):
                    truePos += 1
                    real_dupe_list.append(potentialDupe)
                else:
                    print("------------------------------")
                    print("DUP ERROR : ")
                    print("Score ::: " + str(potentialDupe["similarity"]))
                    print("Distance :" + str(dist) + " meters")

                    if not item["reference"]["bind_id"]:
                        print("Item name (id=" + item["reference"]["id"] + ") ::" + item['properties']['name'])
                        print("False dupe name (id=" + potentialDupe["object"]["reference"]["bind_id"] + ") ::" +
                              potentialDupe['object']['properties']['name'])
                    else:
                        print("Item name (id=" + item["reference"]["bind_id"] + ") ::" + item['properties']['name'])
                        print("False dupe name (id=" + potentialDupe["object"]["reference"]["id"] + ") ::" +
                              potentialDupe['object']['properties']['name'])
                    falsePos += 1
                    fake_dupe_list.append(potentialDupe)
        return truePos, falsePos

    def findRef(self, item, potentialDupe):
        if potentialDupe["object"]["reference"]["bind_id"] == "":
            return potentialDupe["object"]["reference"]["id"] == item["reference"]["bind_id"]
        else:
            return potentialDupe["object"]["reference"]["bind_id"] == item["reference"]["id"]

    def distance(self, origin, destination):
        lat1, lon1 = origin
        lat2, lon2 = destination
        radius = 6371 * 1000  # km
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        d = radius * c
        return d
