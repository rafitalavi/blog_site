# home/context_processors.py
from .models import Websetting

def websetting_processor(request):
    websetting = Websetting.objects.first()
    return {'websetting': websetting}
