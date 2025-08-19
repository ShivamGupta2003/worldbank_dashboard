import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Country, EconomicIndicator



def landing(request):
    return render(request, "landing.html")


def signup_view(request):
    """Handles user registration"""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login after signup
            return redirect("dashboard")  # redirect to dashboard
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})



@login_required
def dashboard(request):
    countries = Country.objects.all()
    return render(request, 'dashboard/dashboard.html', {'countries': countries})



@login_required
def get_indicator_data(request):
    """Fetch data from DB if available, else fallback to World Bank API"""
    indicator_code = request.GET.get('indicator', 'NY.GDP.MKTP.CD')
    country_code = request.GET.get('country', 'USA')
    start_year = int(request.GET.get('start_year', 2010))
    end_year = int(request.GET.get('end_year', 2020))

    try:
        country = Country.objects.get(code=country_code)
        data = EconomicIndicator.objects.filter(
            country=country,
            indicator_code=indicator_code,
            year__gte=start_year,
            year__lte=end_year
        ).order_by('year')

        if data.exists():
            years = [d.year for d in data]
            values = [d.value for d in data]
            return JsonResponse({
                'years': years,
                'values': values,
                'indicator_name': data[0].get_indicator_code_display(),
                'country_name': country.name
            })

  
        return fetch_from_worldbank(indicator_code, country_code, start_year, end_year)

    except Country.DoesNotExist:
        return fetch_from_worldbank(indicator_code, country_code, start_year, end_year)


# ----------------- WORLD BANK FETCH -----------------
def fetch_from_worldbank(indicator_code, country_code, start_year, end_year):
    """Fetch data from World Bank API and save to DB"""
    try:
        url = (
            f"http://api.worldbank.org/v2/country/{country_code}/indicator/"
            f"{indicator_code}?format=json&date={start_year}:{end_year}&per_page=100"
        )
        response = requests.get(url, timeout=10)
        data = response.json()

        if len(data) < 2 or not data[1]:
            return JsonResponse({'error': 'No data available'}, status=404)

        # Country info
        country_data = data[1][0]['country']
        country, _ = Country.objects.get_or_create(
            code=country_data['id'],
            defaults={'name': country_data['value']}
        )

        years, values = [], []
        for item in data[1]:
            if item['value'] is not None:
                year = int(item['date'])
                value = float(item['value'])

                EconomicIndicator.objects.update_or_create(
                    country=country,
                    indicator_code=indicator_code,
                    year=year,
                    defaults={'value': value}
                )

                years.append(year)
                values.append(value)

        indicator_name = dict(EconomicIndicator.INDICATOR_CHOICES).get(indicator_code, indicator_code)

        return JsonResponse({
            'years': years[::-1],   
            'values': values[::-1],
            'indicator_name': indicator_name,
            'country_name': country.name
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
