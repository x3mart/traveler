from django.template.loader import render_to_string
import gzip
from django.http import FileResponse
from traveler.settings import BASE_DIR
from geoplaces.models import Destination
from tours.models import Tour


def make_retailrocket_yml():
    tours = Tour.objects.in_sale().prefetched().with_discounted_price()
    destinations = Destination.objects.filter(tours_by_start_destination__in=tours).distinct().prefetch_related('region').order_by('name').distinct()
    content = render_to_string('traveler.yml', {'tours':tours, 'destinations':destinations})
    with gzip.open(f'{BASE_DIR}/django-media/traveler.yml.gz', 'wb') as file:
        file.write(content.encode('utf-8'))
    # with gzip.open(f'{BASE_DIR}/django-media/traveler.yml.gz', 'wb') as file:
    #     file.write(f'{BASE_DIR}/django-media/traveler.yml') 
    # return FileResponse(open(f'{BASE_DIR}/django-media/traveler.yml'),)