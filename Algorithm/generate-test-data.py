import random
from authenticate import *

collection = db['results']

# Define tags and their associated attributes with random weights that sum to 1
tags_data = {
    "label": {
        "text": None,
        "for": None,
        "attribute": None
    },
    "input": {
        "attribute": None,
        "id": None,
        "type": None
    },
    "span": {
        "attribute": None,
        "text": None,
        "class": None
    },
    "h1": {
        "attribute": None,
        "text": None,
        "class": None
    },
    "h2": {
        "attribute": None,
        "text": None,
        "class": None
    },
    "h3": {
        "attribute": None,
        "text": None,
        "class": None
    },
    "h4": {
        "attribute": None,
        "text": None,
        "class": None
    },
    "h5": {
        "attribute": None,
        "text": None,
        "class": None
    },
    "h6": {
        "attribute": None,
        "text": None,
        "class": None
    },
    "a": {
        "attribute": None,
        "href": None,
        "data-aura-rendered-by": None,
        "text": None
    },
    "button": {
        "attribute": None,
        "class": None,
        "text": None
    },
    "select": {
        "attribute": None,
        "class": None,
        "select": None
    },
    "img": {
        "attribute": None,
        "data-aura-rendered-by": None,
        "class": None,
        "alt": None
    },
    "lightning-icon": {
        "attribute": None,
        "data-aura-rendered-by": None,
        "class": None
    },
    "div": {
        "attribute": None,
        "class": None,
        "style": None
    }
}

# Generate random weights that sum to 1 for each tag
for tag, attributes in tags_data.items():
    # Generate random weights for attributes
    weights = {attr: random.uniform(0, 1) for attr in attributes.keys()}
    
    # Normalize weights so they sum to 1
    total_weight = sum(weights.values())
    normalized_weights = {attr: weight / total_weight for attr, weight in weights.items()}
    
    # Update tags_data with normalized weights
    tags_data[tag] = normalized_weights

# Insert random data into MongoDB for each tag
for tag, weights in tags_data.items():
    # Insert 2-5 rows per tag
    for _ in range(random.randint(2, 5)):
        pass_fail = random.choice(['n', 'y'])
        document = {
            'old': {'tag': tag},
            'weights': weights,
            'correct_prediction': pass_fail
        }
        collection.insert_one(document)
        print(f"Inserted random data for tag '{tag}': {document}")

# Close the MongoDB client when done
client.close()
