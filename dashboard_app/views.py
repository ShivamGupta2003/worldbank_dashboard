import requests
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Country, EconomicIndicator
from datetime import datetime

def landing(request):
    return render(request, "landing.html")

def signup_view(request):
    """Handles user registration"""
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

@login_required
def dashboard(request):
    """Renders the main dashboard page."""
    countries = Country.objects.all()
    return render(request, 'dashboard/dashboard.html', {'countries': countries})

@login_required
def get_indicator_data(request):
    """Fetches economic data, first from local DB, then from World Bank API."""
    indicator_code = request.GET.get('indicator', 'NY.GDP.MKTP.CD')
    country_code = request.GET.get('country')
    
    current_year = datetime.now().year
    start_year = int(request.GET.get('start_year', current_year - 10))
    end_year = int(request.GET.get('end_year', current_year))
    
    if not country_code:
        return JsonResponse({'error': 'Country selection is required.'}, status=400)

    try:
        country = Country.objects.get(code=country_code)
        data = EconomicIndicator.objects.filter(
            country=country,
            indicator_code=indicator_code,
            year__gte=start_year,
            year__lte=end_year
        ).order_by('year')

        if data.exists():
            years_with_values = [d.year for d in data if d.value is not None]
            values = [d.value for d in data if d.value is not None]
            
            if values:
                return JsonResponse({
                    'years': years_with_values,
                    'values': values,
                    'indicator_name': data[0].get_indicator_code_display(),
                    'country_name': country.name
                })
    except Country.DoesNotExist:
        pass # If country is not in DB, World Bank fetch will create it

    return fetch_from_worldbank(indicator_code, country_code, start_year, end_year)

def fetch_from_worldbank(indicator_code, country_code, start_year, end_year):
    """Helper function to fetch data from World Bank API and save to DB."""
    try:
        url = (
            f"http://api.worldbank.org/v2/country/{country_code}/indicator/"
            f"{indicator_code}?format=json&date={start_year}:{end_year}&per_page=1000"
        )
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        api_data = response.json()

        if len(api_data) < 2 or not api_data[1]:
            return JsonResponse({'error': f'No data found for {country_code}. Try a different country or indicator.'}, status=404)

        country_data = api_data[1][0]['country']
        country, _ = Country.objects.get_or_create(
            code=country_data['id'],
            defaults={'name': country_data['value']}
        )

        raw_data = []
        for item in api_data[1]:
            if item.get('value') is not None:
                year = int(item['date'])
                value = float(item['value'])
                raw_data.append({'year': year, 'value': value})
                EconomicIndicator.objects.update_or_create(
                    country=country, indicator_code=indicator_code, year=year,
                    defaults={'value': value}
                )
        
        if not raw_data:
             return JsonResponse({'error': f'No valid data points found for the selected period.'}, status=404)

        sorted_data = sorted(raw_data, key=lambda x: x['year'])
        years = [item['year'] for item in sorted_data]
        values = [item['value'] for item in sorted_data]
        indicator_name = dict(EconomicIndicator.INDICATOR_CHOICES).get(indicator_code, indicator_code)

        return JsonResponse({
            'years': years,
            'values': values,
            'indicator_name': indicator_name,
            'country_name': country.name
        })
    except requests.exceptions.RequestException:
        return JsonResponse({'error': 'Could not connect to the World Bank API.'}, status=503)
    except Exception as e:
        return JsonResponse({'error': f'An unexpected error occurred: {e}'}, status=500)