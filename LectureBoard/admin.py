from django.contrib import admin
from .models import Module
from .models import LectureDay
from .models import SlidePack
from .models import ModuleAccess

# Registering models so they can be accessed and modified on the Administrator site:
admin.site.site_header = 'WMGTSS Administration'
admin.site.register(ModuleAccess)
admin.site.register(Module)
admin.site.register(LectureDay)
admin.site.register(SlidePack)

