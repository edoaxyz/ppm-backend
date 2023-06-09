import json

from rest_framework.parsers import MultiPartParser


class BetterJSONParser(MultiPartParser):
    def parse(self, stream, media_type=None, parser_context=None):
        data_and_files = super().parse(stream, media_type, parser_context)
        if len(data_and_files.data) == 1 and data_and_files.data.get("json"):
            json_data = json.loads(data_and_files.data["json"])

            def replace_files(d):
                new = dict(d)
                for k, v in d.items():
                    if isinstance(v, dict):
                        new[k] = replace_files(v)
                    elif isinstance(v, str) and data_and_files.files.get(v):
                        new[k] = data_and_files.files[v]
                return new

            return replace_files(json_data)
        return data_and_files
