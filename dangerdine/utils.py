# type: ignore
import requests
import openrouteservice
from openrouteservice import convert


def all_businesses() -> list[dict[str, str | float]]:
    """Very epic method. Uses the food ratings
    API to get a list of all businesses rated 0 or 1,
    then selects only the specific business types needed,
    and finally gets the correct geo-coordinates using another API.
    Returns the full list of 5951~ businesses, where each business
    is a dictionary with four keys: the 'Name', the 'Rating', the
    'Longitude', and the 'Latitude'.
    Written by Donian of donian.itch.io fame (Also Matt is Cringe)"""

    needed_business_types = ["7844", "4613", "7840", "1", "7843"]

    all_shit = []

    for bus_type in needed_business_types:

        request = "https://api1-ratings.food.gov.uk/enhanced-search/en-GB/^/^/alpha/"+ bus_type +"/england/LessThanOrEqual1/1/1/1/json"

        response = requests.get(request)

        response_dict = response.json()

        number_of_places = int(response_dict["FHRSEstablishment"]["Header"]["ItemCount"])

        number_remaining = number_of_places

        if number_of_places > 5000:
            number_of_places = 5000

        loops = 0

        valid_categories = ["Takeaway/sandwich shop", "Retailers - other", "Retailers - supermarkets/hypermarkets", "Restaurant/Cafe/Canteen", "Pub/bar/nightclub"]

        while number_remaining > 0:

            loops += 1

            request = "https://api1-ratings.food.gov.uk/enhanced-search/en-GB/^/^/alpha/"+ bus_type +"/england/LessThanOrEqual1/1/"+ str(loops) +"/"+ str(number_of_places) +"/json"

            response = requests.get(request)

            response_dict = response.json()

            for i in range(number_of_places):

                try:

                    if response_dict["FHRSEstablishment"]["EstablishmentCollection"]["EstablishmentDetail"][i]["BusinessType"] in valid_categories:

                        valid = True

                        temp_dict = {"Name": response_dict["FHRSEstablishment"]["EstablishmentCollection"]["EstablishmentDetail"][i]["BusinessName"],
                                     "Rating": response_dict["FHRSEstablishment"]["EstablishmentCollection"]["EstablishmentDetail"][i]["RatingValue"],
                                     "Longitude": 0.0,
                                     "Latitude": 0.0}

                        full_address = ""
                        if response_dict["FHRSEstablishment"]["EstablishmentCollection"]["EstablishmentDetail"][i]["AddressLine1"] != None:
                            full_address = full_address + " " + response_dict["FHRSEstablishment"]["EstablishmentCollection"]["EstablishmentDetail"][i]["AddressLine1"]
                        if response_dict["FHRSEstablishment"]["EstablishmentCollection"]["EstablishmentDetail"][i]["AddressLine2"] != None:
                            full_address = full_address + " " + response_dict["FHRSEstablishment"]["EstablishmentCollection"]["EstablishmentDetail"][i]["AddressLine2"]
                        if response_dict["FHRSEstablishment"]["EstablishmentCollection"]["EstablishmentDetail"][i]["AddressLine3"] != None:
                            full_address = full_address + " " + response_dict["FHRSEstablishment"]["EstablishmentCollection"]["EstablishmentDetail"][i]["AddressLine3"]
                        if response_dict["FHRSEstablishment"]["EstablishmentCollection"]["EstablishmentDetail"][i]["AddressLine4"] != None:
                            full_address = full_address + " " + response_dict["FHRSEstablishment"]["EstablishmentCollection"]["EstablishmentDetail"][i]["AddressLine4"]

                        try:

                            while full_address[0] == " ":
                                full_address = full_address[1:]

                            temp = full_address.replace(" ", "+")

                            request = "https://geocode.maps.co/search?q=" + temp

                            new_request = requests.get(request)

                            new_request_dict = new_request.json()

                            if new_request_dict != []:

                                temp_dict["Longitude"] = float(new_request_dict[0]["lon"])
                                temp_dict["Latitude"] = float(new_request_dict[0]["lat"])

                            else:

                                temp_dict["Longitude"] = float(response_dict["FHRSEstablishment"]["EstablishmentCollection"]["EstablishmentDetail"][i]["Geocode"]["Longitude"])
                                temp_dict["Latitude"] = float(response_dict["FHRSEstablishment"]["EstablishmentCollection"]["EstablishmentDetail"][i]["Geocode"]["Longitude"])

                        except:

                            valid = False

                        if valid == True:

                            all_shit.append(temp_dict)

                except:
                    break

            number_remaining -= number_of_places

            number_of_places = number_remaining

            if number_of_places > 5000:
                number_of_places = 5000

    return all_shit


def getPolyLinePoints(coords: list[tuple[int, int]]) -> list[list[float]]:

    i = 0
    while i < len(coords):
        coords[i] = (coords[i][1], coords[i][0])
        i += 1


    numcoords = len(coords)
    # Tests all possible end points to find the most optimal
    j = 1
    smallestlist = []
    while j < (numcoords - 1):
        tempcoords = coords
        tempcoords[numcoords - 1], tempcoords[j] = tempcoords[j], tempcoords[numcoords - 1]
        client = openrouteservice.Client(key='5b3ce3597851110001cf6248dd014f6c26da4099a9ef15690af0e722')
        trythisone = client.directions(tempcoords, optimize_waypoints=True)['routes'][0]['summary']['distance']
        smallestlist.append(trythisone)
        j += 1

    j = smallestlist.index(min(smallestlist)) + 1

    coords[numcoords - 1], coords[j] = coords[j], coords[numcoords - 1]
    client = openrouteservice.Client(key='5b3ce3597851110001cf6248dd014f6c26da4099a9ef15690af0e722')
    geometry = client.directions(coords, optimize_waypoints=True)['routes'][0]['geometry']

    ## print(geometry)

    geometry = (convert.decode_polyline(geometry))['coordinates']

    i = 0
    while i < len(geometry):
        geometry[i][1], geometry[i][0] = geometry[i][0], geometry[i][1]
        i += 1

    return geometry
