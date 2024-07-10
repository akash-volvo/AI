from authenticate import *

# Define the weights for each tag type
tag_weights = {
    "label": {
        "text": 0.3,
        "for": 0.4,
        "attribute": 0.3
    },
    "input": {
        "attribute": 0.15,
        "id": 0.4,
        "type": 0.45
    },
    "span": {
        "attribute": 0.25,
        "text": 0.4,
        "class": 0.35
    },
    "h1": {
        "attribute": 0.25,
        "text": 0.4,
        "class": 0.35
    },
    "h2": {
        "attribute": 0.25,
        "text": 0.4,
        "class": 0.35
    },
    "h3": {
        "attribute": 0.25,
        "text": 0.4,
        "class": 0.35
    },
    "h4": {
        "attribute": 0.25,
        "text": 0.4,
        "class": 0.35
    },
    "h5": {
        "attribute": 0.25,
        "text": 0.4,
        "class": 0.35
    },
    "h6": {
        "attribute": 0.25,
        "text": 0.4,
        "class": 0.35
    },
    "a": {
        "attribute": 0.1,
        "href": 0.3,
        "data-aura-rendered-by": 0.4,
        "text": 0.2
    },
    "button": {
        "attribute": 0.4,
        "class": 0.3,
        "text": 0.2
    },
    "select": {
        "attribute": 0.2,
        "class": 0.1,
        "select": 0.7
    },
    "img": {
        "attribute": 0.2,
        "data-aura-rendered-by": 0.2,
        "class": 0.2,
        "alt": 0.4
    },
    "lightning-icon": {
        "attribute": 0.25,
        "data-aura-rendered-by": 0.2,
        "class": 0.55
    },
    "div": {
        "attribute": 0.25,
        "class": 0.55,
        "style": 0.2
    }
}

# Function to insert tag weights into MongoDB
def insert_tag_weights(tag, weights):
    try:
        # Construct document to insert
        document = {
            'tag': tag,
            'weights': weights
        }

        # Insert document into MongoDB
        weights_collection.insert_one(document)
        print(f"Inserted weights for tag '{tag}' into MongoDB")
    except Exception as e:
        print(f"Error inserting weights into MongoDB: {e}")

# Iterate over each tag and insert its weights into MongoDB
for tag, weights in tag_weights.items():
    insert_tag_weights(tag, weights)

# Close MongoDB connection
client.close()
