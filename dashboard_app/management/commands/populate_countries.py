import requests
from django.core.management.base import BaseCommand
from dashboard_app.models import Country

class Command(BaseCommand):
    help = 'Populates the Country database with a list of countries from the World Bank API'

    def handle(self, *args, **options):
        self.stdout.write('Fetching countries from World Bank API...')
        url = "http://api.worldbank.org/v2/country?format=json&per_page=350"
        
        try:
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            data = response.json()
            
            if len(data) < 2:
                self.stdout.write(self.style.ERROR('Could not parse API response.'))
                return

            countries_api = data[1]
            created_count = 0
            updated_count = 0
            for country_data in countries_api:
                if country_data.get('region', {}).get('value') != 'Aggregates':
                    code = country_data['id']
                    name = country_data['name']
                    
                    obj, created = Country.objects.update_or_create(
                        code=code,
                        defaults={'name': name}
                    )
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1
            
            self.stdout.write(self.style.SUCCESS(f'Operation complete. Added: {created_count}. Updated: {updated_count}.'))

        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'API request failed: {e}'))