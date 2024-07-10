from bs4 import BeautifulSoup
from authenticate import *

# Fetch weights from MongoDB for a given tag
def fetch_weights(tag):
    try:
        result = weights_collection.find_one({"tag": tag})
        if result:
            return result['weights']
        else:
            print(f"No weights found for tag '{tag}' in MongoDB.")
            return None
    except errors.ServerSelectionTimeoutError as err:
        print(f"Error fetching weights from MongoDB: {err}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

# Store prediction result in MongoDB
def store_prediction_result(type_tag, predicted_score, weights, error_log, best_match_input, correct_element=None):
    try:
        # If correct_element is None, use best_match_input as correct (assuming prediction is correct)
        if correct_element is None:
            correct_element = best_match_input

        # Create document for 'old', 'prediction', and 'actual' elements
        def create_element_document(name, html_string):
            try:
                element = html_string  
                if name == 'old':
                    soup = BeautifulSoup(html_string, "lxml")
                    element = soup.find(type_tag)
                
                element_document = {
                    'raw element': str(element),
                    'tag': element.name,
                }

                # Extract all attributes of the element
                for key, value in element.attrs.items():
                    # Skip 'score' and 'name' attributes
                    if key == 'score' or key == 'name':
                        continue
                    
                    # Handle 'class' attribute to store as a single string
                    if key == 'class':
                        value = ' '.join(value)

                    # Check if value is not None before adding to element_document
                    if value is not None:
                        element_document[key] = value
                
                # Extract text content of the element
                element_document['text'] = element.get_text(strip=True)

                return element_document
            
            except Exception as e:
                print(f"Error processing '{name}' element: {e}")
                return None

        # Create documents for 'old', 'prediction', and 'actual' elements
        old_doc = create_element_document('old', error_log)
        predicted_doc = create_element_document('prediction', best_match_input)

        # If correct_element is provided, create document for 'actual' element
        if correct_element is not None:
            actual_doc = create_element_document('actual', correct_element)
        else:
            actual_doc = predicted_doc

        # Store the prediction result in MongoDB
        correct_prediction = "y" if actual_doc == predicted_doc else "n"

        # Construct the result document
        result_document = {
            'old': old_doc,
            'prediction': predicted_doc,
            'actual': actual_doc,
            'correct_prediction': correct_prediction,
            'prediction_probability': predicted_score,
            'weights': weights
        }

        # Insert the result document into the 'results' collection
        results_collection.insert_one(result_document)
        print("Stored prediction result in MongoDB.")

    except errors.ServerSelectionTimeoutError as err:
        print(f"Error storing prediction result in MongoDB: {err}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    finally:
        client.close()

# Close the MongoDB client when the module is not in use
def close_client():
    client.close()
