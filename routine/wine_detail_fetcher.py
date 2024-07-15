from client.vivino_client import VivinoClient
from payload.wine_details import WineDetails


class WineDetailFetcher:

    def __init__(self):
        self.vivino_client = VivinoClient()

    def get_wine_details(self, input_wine):
        vivino_query_response = self.vivino_client.lookup_wine(input_wine)
        if not vivino_query_response:
            return

        wholesale_price = self.vivino_client.get_wholesale_price(vivino_query_response.vintage_id)

        wine = self.vivino_client.get_wine_by_vintage_id(vivino_query_response.vintage_id)

        flavor_profile = self.vivino_client.get_flavor_profile(wine["id"])

        return WineDetails(
            name=vivino_query_response.name,
            input_wine=input_wine,
            menu_price=input_wine.price,
            wine_type=wine["name"],
            flavor_profile=flavor_profile,
            online_price=wholesale_price,
            alcohol_content=vivino_query_response.alcohol_content,
            menu_year=input_wine.year,
            region=vivino_query_response.region,
            rating=vivino_query_response.rating,
            rating_count=vivino_query_response.rating_count
        )