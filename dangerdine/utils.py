import requests


def all_businesses() -> list[dict[str, str|float]]:
    """Very epic method. Uses the food ratings
    API to get a list of all businesses rated 0 or 1,
    then selects only the specific business types needed,
    and finally gets the correct geo-coordinates using another API.
    Returns the full list. CAN BE OPTIMISED MORE (will do Soon^TM)"""

    request = "https://api1-ratings.food.gov.uk/enhanced-search/en-GB/^/^/alpha/0/england/LessThanOrEqual1/1/1/1/json"

    response = requests.get(request)

    response_dict = response.json()

    number_of_places = int(response_dict["FHRSEstablishment"]["Header"]["ItemCount"])

    print(number_of_places)

    number_remaining = number_of_places

    if number_of_places > 5000:
        number_of_places = 5000

    all_shit = []

    loops = 0

    valid_categories = ["Takeaway/sandwich shop", "Retailers - other", "Retailers - supermarkets/hypermarkets",
                        "Restaurant/Cafe/Canteen", "Pub/bar/nightclub"]

    while number_remaining > 0:

        loops += 1

        request = "https://api1-ratings.food.gov.uk/enhanced-search/en-GB/^/^/alpha/0/england/LessThanOrEqual1/1/" + str(
            loops) + "/" + str(number_of_places) + "/json"

        response = requests.get(request)

        response_dict = response.json()

        for i in range(number_of_places):

            try:

                if response_dict["FHRSEstablishment"]["EstablishmentCollection"]["EstablishmentDetail"][i][
                    "BusinessType"] in valid_categories:

                    valid = True

                    temp_dict = {
                        "Name": response_dict["FHRSEstablishment"]["EstablishmentCollection"]["EstablishmentDetail"][i][
                            "BusinessName"],
                        "Rating":
                            response_dict["FHRSEstablishment"]["EstablishmentCollection"]["EstablishmentDetail"][i][
                                "RatingValue"],
                        "Longitude": 0.0,
                        "Latitude": 0.0}

                    full_address = ""
                    if response_dict["FHRSEstablishment"]["EstablishmentCollection"]["EstablishmentDetail"][i][
                        "AddressLine1"] != None:
                        full_address = full_address + " " + \
                                       response_dict["FHRSEstablishment"]["EstablishmentCollection"][
                                           "EstablishmentDetail"][i]["AddressLine1"]
                    if response_dict["FHRSEstablishment"]["EstablishmentCollection"]["EstablishmentDetail"][i][
                        "AddressLine2"] != None:
                        full_address = full_address + " " + \
                                       response_dict["FHRSEstablishment"]["EstablishmentCollection"][
                                           "EstablishmentDetail"][i]["AddressLine2"]
                    if response_dict["FHRSEstablishment"]["EstablishmentCollection"]["EstablishmentDetail"][i][
                        "AddressLine3"] != None:
                        full_address = full_address + " " + \
                                       response_dict["FHRSEstablishment"]["EstablishmentCollection"][
                                           "EstablishmentDetail"][i]["AddressLine3"]
                    if response_dict["FHRSEstablishment"]["EstablishmentCollection"]["EstablishmentDetail"][i][
                        "AddressLine4"] != None:
                        full_address = full_address + " " + \
                                       response_dict["FHRSEstablishment"]["EstablishmentCollection"][
                                           "EstablishmentDetail"][i]["AddressLine4"]

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

                            temp_dict["Longitude"] = float(
                                response_dict["FHRSEstablishment"]["EstablishmentCollection"]["EstablishmentDetail"][i][
                                    "Geocode"]["Longitude"])
                            temp_dict["Latitude"] = float(
                                response_dict["FHRSEstablishment"]["EstablishmentCollection"]["EstablishmentDetail"][i][
                                    "Geocode"]["Longitude"])

                    except:

                        valid = False

                    if valid == True:
                        all_shit.append(temp_dict)

            except:
                print(response_dict["FHRSEstablishment"]["EstablishmentCollection"]["EstablishmentDetail"][i])
                print(number_remaining)
                break

        number_remaining -= number_of_places

        number_of_places = number_remaining

        if number_of_places > 5000:
            number_of_places = 5000

    return all_shit
