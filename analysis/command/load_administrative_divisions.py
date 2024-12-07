"""Allow loading the administrative divisions manually"""

import csv
from datetime import datetime

from rest_framework.decorators import api_view

from common.helpers.api_responses import api_response_error, api_response_success

from ..models.administrative_division import AdministrativeDivision


def create_country(row) -> AdministrativeDivision:
    """Create a new country"""
    new_country = AdministrativeDivision(
        p_code=row["Location"],
        country_code=row["Location"],
        admin_level=0,
        name=row["Location"],
    )
    new_country.save()
    return new_country


def create_finish_message(
    message: str,
    rows_inserted,
    countries_created,
    rows_duplicated,
    rows_parent_not_found,
):
    """Create the ending message with a summary"""
    message = f"""
\n{message}\n
"\tRows inserted: {str(rows_inserted)}\n"
"\tCountries created: {str(countries_created)}\n"
"\tErrors by duplications: {str(rows_duplicated)}\n"
"\tErrors by parent not existing: {str(rows_parent_not_found)}"
    """
    return message


@api_view(["POST"])
def load_administrative_divisions(request):
    """Loads the administrative divisions of the csv path passed as parameter"""
    with open("global_pcodes(1).csv", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        rows_inserted = 0
        rows_duplicated = 0
        rows_parent_not_found = 0
        countries_created = 0
        try:
            for row in reader:
                row_existing = AdministrativeDivision.objects.filter(
                    p_code=row["P-Code"]
                ).first()
                if row_existing:
                    rows_duplicated += 1
                    print(
                        f"({row["Location"]}) "
                        + row["Name"]
                        + " Not inserted because a location with the same pcode ("
                        + row_existing.name
                        + ") was already loaded",
                        flush=True,
                    )
                    continue
                valid_from_date = None
                if row["Valid from date"]:
                    valid_from_date = datetime.strptime(
                        row["Valid from date"], "%Y-%m-%d"
                    ).date()

                parent_p_code = None
                if row["Parent P-Code"]:
                    try:
                        parent_p_code = AdministrativeDivision.objects.get(
                            p_code=row["Parent P-Code"]
                        )
                    except AdministrativeDivision.DoesNotExist:
                        if row["Admin Level"] == "1":
                            new_country = create_country(row)
                            countries_created += 1
                            rows_inserted += 1
                            parent_p_code = new_country
                        else:
                            rows_parent_not_found += 1
                            print(
                                row["Name"]
                                + " Not inserted because the parent "
                                + row["Parent P-Code"]
                                + " is not existing"
                            )
                            continue

                division = AdministrativeDivision(
                    p_code=row["P-Code"],
                    country_code=row["Location"],
                    admin_level=int(row["Admin Level"]),
                    name=row["Name"],
                    parent_p_code=parent_p_code,
                    valid_from_date=valid_from_date,
                )
                division.save()
                rows_inserted += 1
            message = create_finish_message(
                "Finish succesfully",
                rows_inserted,
                countries_created,
                rows_duplicated,
                rows_parent_not_found,
            )
        except Exception as e:
            message = create_finish_message(
                f"Load interrumped by the following error: {str(e)}",
                rows_inserted,
                countries_created,
                rows_duplicated,
                rows_parent_not_found,
            )
            return api_response_error("Error", message, 500)
    return api_response_success(
        "Success", message, 201
    )
