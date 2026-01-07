import datetime
from django.core.serializers.json import DjangoJSONEncoder

class MyJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        return super().default(o)
