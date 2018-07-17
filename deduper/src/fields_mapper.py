import io
import json


class FieldsMapper(object):
    def __init__(self, fields_mapper_file):
        self.mapper_description = self.loadMapper(fields_mapper_file)
        self.id = self.mapper_description['id'].encode('utf-8')
        try:
            self.delimiter = self.mapper_description['delimiter'].encode('utf-8')
        except KeyError:
            self.delimiter = None
        self.columns = self.mapper_description['columns']

    def loadMapper(self, mapper_file):
        file = io.open(mapper_file, mode="r", encoding="utf-8")
        mapper = json.load(file)
        return mapper
