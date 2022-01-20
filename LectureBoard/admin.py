from django.contrib import admin
from .models import LectureBoard
from .models import LectureDay
from .models import SlidePack
from .models import VersionHistory

# Register your models here.

admin.site.register(LectureBoard)
admin.site.register(LectureDay)
admin.site.register(SlidePack)
admin.site.register(VersionHistory)

