from django.contrib import admin
from .models import Animal, HealthRecord, Vaccination,VetVisit

admin.site.register(Animal)
admin.site.register(HealthRecord)
admin.site.register(Vaccination)
admin.site.register(VetVisit)
