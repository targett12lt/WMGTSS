from django.contrib import admin
from .models import ModuleBoard
from .models import LectureDay
from .models import SlidePack
from .models import VersionHistory

# Register your models here.

admin.site.register(ModuleBoard)
admin.site.register(LectureDay)
admin.site.register(SlidePack)
admin.site.register(VersionHistory)

