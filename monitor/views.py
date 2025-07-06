from datetime import date
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.dateformat import DateFormat
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User

from reportlab.pdfgen import canvas
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Animal, HealthRecord, Vaccination, VetVisit
from .serializers import AnimalSerializer, HealthRecordSerializer

# ---------------------- DASHBOARD ----------------------
@login_required(login_url='login')
def dashboard(request):
    animals = Animal.objects.all()
    records = HealthRecord.objects.order_by('-date_recorded')[:5]
    vaccinations = Vaccination.objects.order_by('-date_administered')[:5]
    upcoming = VetVisit.objects.filter(visit_date__gte=date.today(), attended=False)

    # Temperature chart data (for first animal)
    first_animal = Animal.objects.first()
    temp_labels, temp_data = [], []
    if first_animal:
        history = HealthRecord.objects.filter(animal=first_animal).order_by('-date_recorded')[:10][::-1]
        temp_labels = [DateFormat(r.date_recorded).format('M d') for r in history]
        temp_data = [r.temperature for r in history]

    return render(request, 'dashboard.html', {
        'animals': animals,
        'records': records,
        'vaccinations': vaccinations,
        'upcoming_visits': upcoming,
        'temp_labels': temp_labels,
        'temp_data': temp_data,
    })

# ---------------------- AUTH ----------------------
def login_view(request):
    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('dashboard')
        return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')

# ---------------------- CHART API ----------------------
@login_required(login_url='login')
def temperature_chart(request):
    animal = Animal.objects.first()
    if not animal:
        return JsonResponse({"labels": [], "data": []})
    records = HealthRecord.objects.filter(animal=animal).order_by('-date_recorded')[:10][::-1]
    labels = [DateFormat(r.date_recorded).format('M d') for r in records]
    data = [r.temperature for r in records]
    return JsonResponse({"labels": labels, "data": data})

# ---------------------- EXPORT PDF ----------------------
@login_required(login_url='login')
def export_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="health_records.pdf"'

    p = canvas.Canvas(response)
    p.setFont("Helvetica", 12)
    p.drawString(100, 800, "Animal Health Records")

    y = 770
    for record in HealthRecord.objects.all().order_by('-date_recorded')[:20]:
        p.drawString(50, y, f"{record.animal.name} | {record.date_recorded} | Temp: {record.temperature}°C")
        y -= 20
        if y < 100:
            p.showPage()
            y = 800

    p.save()
    return response

# ---------------------- REST API ----------------------
@api_view(['GET'])
def api_animals(request):
    animals = Animal.objects.all()
    return Response(AnimalSerializer(animals, many=True).data)

@api_view(['GET'])
def api_records(request):
    records = HealthRecord.objects.all()
    return Response(HealthRecordSerializer(records, many=True).data)



def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already taken'})

        user = User.objects.create_user(username=username, email=email, password=password1)
        login(request, user)
        return redirect('dashboard')

    return render(request, 'signup.html')
