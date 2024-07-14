import json

import requests

from wine import Wine
from wine_details import WineDetails


class WineAPIClient():

    def __init__(self):
        self.url = 'https://9takgwjuxl-dsn.algolia.net/1/indexes/WINES_prod/query'
        self.algolia_key = '60c11b2f1068885161d95ca068d3a6ae'
        self.application_id = '9TAKGWJUXL'

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

        response = requests.request("POST", self.url, headers=headers, data=payload)

        if response.status_code != 200:
            return None

        response = response.json()

        if not response["hits"]:
            return None

        hit = response["hits"][0]
        if not hit["vintages"]:
            return None

        vintage = hit["vintages"][0]

        return WineDetails(
            name=vintage["name"],
            region=hit["region"]["name"],
            rating=vintage["statistics"]["ratings_average"],
            rating_count=vintage["statistics"]["ratings_count"]
        )


