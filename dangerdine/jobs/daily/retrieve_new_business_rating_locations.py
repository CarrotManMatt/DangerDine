from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django_extensions.management.jobs import DailyJob

import dangerdine.utils
from dangerdine.models import BusinessRatingLocation


class Job(DailyJob):
    help = "Retrieve any new Business Rating Locations from FSA."  # noqa: A003

    def execute(self) -> None:
        raw_business_rating_location: dict[str, str | float]
        for count, raw_business_rating_location in enumerate(dangerdine.utils.all_businesses()):  # type: ignore[attr-defined] # noqa: E501
            print(f"Trying {raw_business_rating_location['Name']!r} ({count})")  # noqa: T201

            try:
                BusinessRatingLocation.objects.get_or_create(
                    name=str(raw_business_rating_location["Name"]).strip(r"' &").replace(
                        r"//",
                        ""
                    ).replace(r"\\", "").replace(r"\&", "&").replace(
                        r"''",
                        "'"
                    ),
                    food_hygiene_rating=BusinessRatingLocation.FoodHygieneRating(
                        int(raw_business_rating_location["Rating"])
                    ),
                    location=Point(
                        raw_business_rating_location["Longitude"],
                        raw_business_rating_location["Latitude"]
                    )
                )
            except ValidationError:
                print(f"Failed! {raw_business_rating_location['Name']!r}")  # noqa: T201

            print()  # noqa: T201
