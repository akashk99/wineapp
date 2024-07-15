import json
from typing import List

import requests

from payload.flavor_profile import Structure, FlavorProfile
from payload.vivino_query_response import VivinoQueryResponse
from payload.wine_details import WineDetails


class VivinoClient():

    def __init__(self):
        self.query_url = 'https://9takgwjuxl-dsn.algolia.net/1/indexes/WINES_prod/query'
        self.base_url = 'https://www.vivino.com/api'
        self.algolia_key = '60c11b2f1068885161d95ca068d3a6ae'
        self.application_id = '9TAKGWJUXL'

        self.session = requests.Session()
        self.session.headers.update({
            'authority': 'www.vivino.com',
            'accept': 'application/json',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/json',
            'if-none-match': 'W/"e69f582bd76c4c6221640acac3bd41f7"',
            'referer': 'https://www.vivino.com/US-CA/en/rombauer-vineyards-chardonnay/w/5602',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def lookup_wine(self, wine):
        payload = json.dumps({
            "query": wine.name + " " + str(wine.year),
            "hitsPerPage": 1
        })
        headers = {
            'x-algolia-application-id': self.application_id,
            'x-algolia-api-key': self.algolia_key,
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", self.query_url, headers=headers, data=payload)

        if response.status_code != 200:
            return None

        response = response.json()

        if not response["hits"]:
            return None

        hit = response["hits"][0]
        if not hit["vintages"]:
            return None

        vintage = hit["vintages"][0]

        return VivinoQueryResponse(
            name=vintage["name"],
            vintage_id=vintage["id"],
            menu_price=wine.price,
            alcohol_content=hit["alcohol"],
            menu_year=wine.year,
            region=hit["region"]["name"],
            rating=vintage["statistics"]["ratings_average"],
            rating_count=vintage["statistics"]["ratings_count"]
        )

    def get_wholesale_price(self, vintage_id):
        response = self.session.get(f"{self.base_url}/checkout_prices?vintage_id={vintage_id}&language=en")
        if response.status_code != 200:
            return None

        response = response.json()

        if not response["prices"]:
            return None

        if response["prices"]["availability"]:
            return response["prices"]["availability"]["median"]["amount"]
        else:
            return None

    def get_wine_by_vintage_id(self, vintage_id):
        response = self.session.get(f"{self.base_url}/vintages/{vintage_id}")
        if response.status_code != 200:
            return None

        response = response.json()
        return response["vintage"]["wine"]

    def get_flavor_profile(self, wine_id):
        response = self.session.get(f"{self.base_url}/wines/{wine_id}/tastes")
        if response.status_code != 200:
            return None

        json_data = response.json()

        tastes = json_data["tastes"]
        if not tastes:
            return None

        structure_data = tastes["structure"]

        structure = None
        if structure_data:
            structure = Structure(
                acidity=structure_data["acidity"],
                fizziness=structure_data["fizziness"],
                intensity=structure_data["intensity"],
                sweetness=structure_data["sweetness"],
                tannin=structure_data["tannin"],
            )

        top_flavors = []
        if json_data["tastes"]["flavor"]:
            top_flavors = self.parse_flavors(json_data["tastes"]["flavor"])

        return FlavorProfile(structure=structure, top_flavors=top_flavors)

    def parse_flavors(self,flavor_data: List[dict]) -> List[str]:
        # Extract the primary keywords from each flavor group and return as a list of strings
        flavors = []
        for flavor_group in flavor_data[:3]:
            flavors.append(flavor_group["group"])

        return flavors



