class CustomFunctions:
    extract_wine_function = {
        'name': 'extract_wine_information',
        'description': 'Extracts wine information from the input text and returns an array of wines with fields name, year, and price.',
        'parameters': {
            'type': 'object',
            'properties': {
                'wines': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'name': {
                                'type': 'string',
                                'description': 'Name of the wine'
                            },
                            'year': {
                                'type': 'integer',
                                'description': 'Year of the wine in 4 digits, otherwise null',
                                "pattern": "^(19|20)\\d{2}$"
                            },
                            'price': {
                                'type': 'number',
                                'description': 'Price of the wine, otherwise null'
                            }
                        },
                        'required': ['name', 'price', 'year']
                    }
                },
                'count': {
                    'type': 'integer',
                    'description': 'The total number of wines extracted'
                }
            },
            'required': ['wines', 'count']
        }
    }
