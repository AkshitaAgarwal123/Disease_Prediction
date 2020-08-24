from django.shortcuts import render


def nearestHospitals(request):
    # Create your tests here.
    # Importing required libraries 
    from googleplaces import GooglePlaces, types, lang 
    import requests 
    import json  
    API_KEY = 'Your_API_Key'
    google_places = GooglePlaces(API_KEY) 
    query_result = google_places.nearby_search(  
            lat_lng ={'lat': 28.4089, 'lng': 77.3178}, 
            radius = 5000,
            types =[types.TYPE_HOSPITAL]) 
    
    # If any attributions related  
    # with search results print them 
    if query_result.has_attributions: 
        print (query_result.html_attributions) 
    
    
    # Iterate over the search results 
    for place in query_result.places: 
        # print(type(place)) 
        # place.get_details() 
        print (place.name) 
        print("Latitude", place.geo_location['lat']) 
        print("Longitude", place.geo_location['lng']) 
        print() 
        print(place)
