from django.db import models

class Animal(models.Model):
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50)
    breed = models.CharField(max_length=50, blank=True)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10)
    tag_number = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return f"{self.name} ({self.tag_number})"

class HealthRecord(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    date_recorded = models.DateField(auto_now_add=True)
    temperature = models.FloatField()
    symptoms = models.TextField()
    diagnosis = models.TextField()
    treatment = models.TextField()

    def __str__(self):
        return f"{self.animal.name} - {self.date_recorded}"

class Vaccination(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    vaccine_name = models.CharField(max_length=100)
    date_administered = models.DateField()
    next_due = models.DateField()

    def __str__(self):
        return f"{self.vaccine_name} for {self.animal.name}"
    
class VetVisit(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    visit_date = models.DateField()
    reason = models.CharField(max_length=200)
    attended = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.animal.name} on {self.visit_date}"

