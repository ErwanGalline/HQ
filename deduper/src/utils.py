
class Utils(object):

    @classmethod
    def get_binding_list(cls,geojsonIn):
        bind_list = []
        for item in geojsonIn['features']:
            bind_list.append(item["reference"]["id"])
        return bind_list

