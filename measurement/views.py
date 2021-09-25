from django.shortcuts import render, get_object_or_404
from .models import Measurement
from .forms import MeasurementModelForm
from geopy .geocoders import nominatim
from .utils import get_geo,get_center_coordinates,get_zoom
from geopy.distance import geodesic
import folium
# Create your views here.
def calculate_distance_view(request):
    #initial value
    distance= None
    destination= None

    obj = get_object_or_404(Measurement, id = 1)
    forms = MeasurementModelForm(request.POST or None)
    geolocator = nominatim(user_agent = 'measurement')

    ip = '72.14.207.99'
    country ,city , lat,lon = get_geo(ip)
    
    location =geolocator.geocode(city)
    #location coordinates
    l_lat= lat
    l_lon= lon
    pointA=(l_lat,l_lon)
    m = folium.map(width=800, height= 500, location =get_center_coordinates(l_lat, l_lon), zoom_start = 8)
    #location marker
    folium.Marker([l_lat,l_lon], tooltip='click here for more', popup= city[city], 
                    icon=folium.Icon(color='purple')).add_to(m)

    if forms.is_valid():
        instance =  forms.save(commit=False)
        destination_=forms.cleaned_data.get('destination')
        destination = geolocator.geocode(destination_)

        #destination coordinate
        d_lat=destination.latitude
        d_lon=destination.longitude
        pointB = (d_lat,d_lon)

        #distance calculations
        distance = round(geodesic(pointA,pointB).km ,2)

        m = folium.map(width=800, height= 500, location =get_center_coordinates(l_lat, l_lon,d_lat,d_lon),zoom_start= get_zoom(distance))
        #location marker
        folium.Marker([l_lat,l_lon], tooltip='click here for more', popup= city[city], 
                    icon=folium.Icon(color='purple')).add_to(m)
        
        #destination marker
        folium.Marker([d_lat,d_lon], tooltip='click here for more', popup= destination, 
                    icon=folium.Icon(color='red',icon='cloud')).add_to(m)
        
        #draw the line between location and destination
        line = folium.PolyLine(locations=[pointA,pointB],weight = 2, color='blue')
        m.add_child(line)


        instance.location = location
        instance.distance= distance
        instance.save()

    m = m._repr_html_()

    context = {
        'distance' : distance,
        'destination': destination,
        'form': forms,
        'm':m,
    }
    return render(request, 'measurement/main.html',context)