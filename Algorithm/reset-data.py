from authenticate import *

# Function to delete the entire 'weights' collection
def delete_weights_collection():
    try:
        # Drop the collections
        db['weights'].drop()
        db['results'].drop()

        print("Deleted the 'weights' and 'results' collections from MongoDB")
    except Exception as e:
        print(f"Error deleting data from MongoDB: {e}")
    finally:
        client.close()

# Call the function to delete the 'weights' collection
delete_weights_collection()
