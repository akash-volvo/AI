from gensim.models import KeyedVectors
from bs4 import BeautifulSoup

# Prompt the user to choose the type of element to search for.
def fetchInput():
    inp = input("1. Label\n2. Button\n3. Input\n4. Span\n5. H1\n6. A\n7. Select\n8. Img\n9. Lightning Icon\n10. Div (Recursion):\nYour choice: ")

    if inp == "1":
        dom_path = "dom-label.txt"
        input_path = "input-label.txt"
    elif inp == "2":
        dom_path = "dom-button.txt"
        input_path = "input-button.txt"
    elif inp == "3":
        dom_path = "dom-input.txt"
        input_path = "input-input.txt"
    elif inp == "4":
        dom_path = "dom-span.txt"
        input_path = "input-span.txt"
    elif inp == "5":
        dom_path = "dom-h1.txt"
        input_path = "input-h1.txt"
    elif inp == "6":
        dom_path = "dom-a.txt"
        input_path = "input-a.txt"
    elif inp == "7":
        dom_path = "dom-select.txt"
        input_path = "input-select.txt"
    elif inp == "8":
        dom_path = "dom-img.txt"
        input_path = "input-img.txt"
    elif inp == "9":
        dom_path = "dom-lightningicon.txt"
        input_path = "input-lightningicon.txt"
    elif inp == "10":
        dom_path = "dom-recursion.txt"
        input_path = "input-recursion.txt"
    elif inp == "11":
        dom_path = "dom-div.txt"
        input_path = "input-div.txt"
    else:
        print("Invalid input")
        exit()

    return dom_path, input_path

# Load the word2vec model from the given path.
def load_model(model_path):
    return KeyedVectors.load_word2vec_format(model_path, binary=True)

# Read and return the contents of an HTML file.
def read_html_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

# Parse the HTML content using BeautifulSoup.
def parse_html(html_content):
    return BeautifulSoup(html_content, "lxml")


# Read and return the contents of an input file.
def read_input_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

# Parse the HTML content to extract the first element and its attributes.
def parse_input_html(html_content):
    soup = BeautifulSoup(html_content, "lxml")
    
    # List of tag names to search for in order
    tags = [
        'div',
        'lightning-icon',
        'input',
        'h1',
        'h2',
        'h3',
        'h4',
        'h5',
        'h6',
        'a',
        'span',
        'label',
        'button',
        'select',
        'img'
        ]
    
    # Find the first matching tag
    input_element = None
    for tag_name in tags:
        input_element = soup.find(tag_name)
        if input_element:
            break

    print("Input Element: ", input_element)
    
    if input_element:
        # Get all attributes of the input element
        attributes = dict(input_element.attrs)
        attributes["tag"] = input_element.name
        attributes["text"] = input_element.get_text(strip=True)

        if input_element.name == "select":
            options = {option.get('value'): option.text for option in input_element.find_all('option')}
            attributes["options"] = options
            del attributes['text']

        print("Found attributes -------------------------")
        for attr, value in attributes.items():
            print(f"{attr}: {value}")
        
        return attributes
    
    return None

# Get the similarity score between two words using the word2vec model.
# Handle the case where a word might not be in the model's vocabulary.
def get_contextual_similarity(model, word1, word2):
    if word1 == word2:
        return 1.0
    try:
        return model.similarity(word1, word2)
    except KeyError:
        return 0.0

# Calculate the numeric similarity based on the minimum and maximum values.
def get_numeric_similarity(value1, value2, min_value, max_value):
    if value2 == "0" or min_value == max_value:
        return 0.0

    value1 = int((value1.split(":"))[0])
    value2 = int((value2.split(":"))[0])

    # Normalize the difference based on the range
    normalized_diff = abs(value1 - value2) / (max_value - min_value)

    return 1.0 - normalized_diff


# Calculate the class similarity by comparing each class individually.
def get_class_similarity(model, class1, class2):
    if not class1 and not class2:
        return 1
    if not class1 or not class2:
        return 0.0

    class_list1 = class1 if isinstance(class1, list) else class1.split()
    class_list2 = class2 if isinstance(class2, list) else class2.split()

    if not class_list1 or not class_list2:
        return 0.0
    
    total_score = 0.0
    for cls1 in class_list1:
        max_score = max(get_contextual_similarity(model, cls1, cls2) for cls2 in class_list2)
        total_score += max_score

    return total_score / len(class_list1)


# Calculate the style similarity by comparing each style individually.
def get_style_similarity(input_style, actual_style):
    # Split styles into dictionary of style properties and their values
    def parse_style(style):
        style_dict = {}
        if style:
            for s in style.split(";"):
                if ":" in s:
                    key, value = s.split(":", 1)
                    style_dict[key.strip()] = value.strip()
        return style_dict
    
    input_style_dict = parse_style(input_style)
    actual_style_dict = parse_style(actual_style)
    
    if not input_style_dict and not actual_style_dict:
        return 1.0
    
    # Count total and matching style properties
    total_properties = len(input_style_dict)
    matching_properties = sum(1 for key, value in input_style_dict.items() if key in actual_style_dict and actual_style_dict[key] == value)
    
    if total_properties == 0:
        return 0.0

    return matching_properties / total_properties


# Calculate the attribute similarity based on the number and keys of attributes.
def get_attribute_similarity(input_attributes, element_attributes):
    input_keys = set(input_attributes.keys())
    if "text" in input_keys:
        input_keys.remove("text")
    element_keys = set(element_attributes.keys())

    common_keys = input_keys.intersection(element_keys)
    num_common_keys = len(common_keys)

    # Calculate reduction factor based on the number of common keys
    if len(element_keys) != 0:
        reduction_factor = num_common_keys / len(element_keys)
    elif num_common_keys != 0:
        reduction_factor = num_common_keys / len(element_keys)

    if num_common_keys == 0:
        return 0.0
    elif num_common_keys == len(input_keys) == len(element_keys):
        return 1.0
    else:
        return reduction_factor


# Calculate the 'options' similarity based on the keys and values.
def get_select_tag_similarity(input_attributes, element_attributes):
    input_keys = set(input_attributes.items())
    element_keys = set(element_attributes.items())

    common_keys = input_keys.intersection(element_keys)
    num_common_keys = len(common_keys)

    # Calculate reduction factor based on the number of common keys
    if len(element_keys) != 0:
        reduction_factor = num_common_keys / len(element_keys)
    elif num_common_keys != 0:
        reduction_factor = num_common_keys / len(element_keys)

    if num_common_keys == 0:
        return 0.0
    elif num_common_keys == len(input_keys) == len(element_keys):
        return 1.0
    else:
        return reduction_factor

# Clean the elements for 'select' tags by extracting the options.
def clean_elements(unformatted_elements):
    all_elements = []
    for index, value in enumerate(unformatted_elements):
        attributes = dict(unformatted_elements[index].attrs)
        attributes["tag"] = unformatted_elements[index].name
        attributes["text"] = unformatted_elements[index].get_text(strip=True)

        options = {option.get('value'): option.text for option in unformatted_elements[index].find_all('option')}
        attributes["options"] = options
        del attributes['text']

        all_elements.append(attributes)

    return all_elements    

# Calculate the similarity score for a given element based on its type.
def calculate_element_score(input_element, element, model, min_render_value, max_render_value):
    score = 0.0

    # Extract attributes from the input element and the element being compared
    input_attributes = {
        key: input_element.get(key) for key in input_element.keys() if key != 'tag'
    }
    element_attributes = {
        key: element.attrs.get(key) for key in element.attrs.keys() if key != 'tag'
    }

    # Calculate the similarity of attributes
    attribute_similarity = get_attribute_similarity(input_attributes, element_attributes)


    if input_element["tag"] == "input":
        weights = {"attribute_similarity": 0.1, "id": 0.3, "tag": 0.2, "type": 0.4}
        
        element_id = element.get("id", "")
        element_type = element.get("type", "")
        element_tag = element.name

        score_id = get_contextual_similarity(model, input_element["id"], element_id)
        score_type = get_contextual_similarity(model, input_element["type"], element_type)
        score_tag = get_contextual_similarity(model, input_element["tag"], element_tag)

        score = (weights["id"] * score_id) + (weights["type"] * score_type) + (weights["tag"] * score_tag) + (weights["attribute_similarity"] * attribute_similarity)
        
    elif input_element["tag"] == "span" or input_element["tag"] == "h1" or input_element["tag"] == "h2" or input_element["tag"] == "h3" or input_element["tag"] == "h4" or input_element["tag"] == "h5" or input_element["tag"] == "h6":
        weights = {"attribute_similarity": 0.25, "text": 0.4, "class": 0.35}

        element_text = element.get_text(strip=True)
        element_class = element.get("class", "")

        score_text = get_contextual_similarity(model, input_element.get("text", ""), element_text)
        score_class = get_class_similarity(model, input_element.get("class", ""), element_class)

        score = (weights["text"] * score_text) + (weights["class"] * score_class) + (weights["attribute_similarity"] * attribute_similarity)

    elif input_element["tag"] == "label":
        weights = {"attribute_similarity": 0.3, "for": 0.4, "text": 0.3}
        
        element_for = element.get("for", "")
        element_text = element.get_text(strip=True)

        score_for = get_contextual_similarity(model, input_element.get("for", ""), element_for)
        score_text = get_contextual_similarity(model, input_element.get("text", ""), element_text)

        score = (weights["for"] * score_for) + (weights["text"] * score_text) + (weights["attribute_similarity"] * attribute_similarity)

    elif input_element["tag"] == "a":
        weights = {"attribute_similarity": 0.1, "href": 0.3, "data-aura-rendered-by": 0.4, "text": 0.2}
        
        element_href = element.get("href", "")
        element_render = element.get("data-aura-rendered-by", "0")
        element_text = element.get_text(strip=True)

        score_href = get_contextual_similarity(model, input_element.get("href", ""), element_href)
        score_render = get_numeric_similarity(input_element.get("data-aura-rendered-by", "0"), element_render, min_render_value, max_render_value)
        score_text = get_contextual_similarity(model, input_element.get("text", ""), element_text)

        score = (weights["href"] * score_href) + (weights["data-aura-rendered-by"] * score_render) + (weights["text"] * score_text) + (weights["attribute_similarity"] * attribute_similarity)

    elif input_element["tag"] == "button":
        weights = {"attribute_similarity": 0.4, "class": 0.3, "text": 0.2}

        element_text = element.get_text(strip=True)
        element_class = element.get("class", "")

        score_text = get_contextual_similarity(model, input_element.get("text", ""), element_text)
        score_class = get_class_similarity(model, input_element.get("class", ""), element_class)

        score = (weights["class"] * score_class) + (weights["text"] * score_text) + (weights["attribute_similarity"] * attribute_similarity)

    elif input_element["tag"] == "select":
        weights = {"attribute_similarity": 0.2, "class": 0.1, "select": 0.7}

        element_class = element.get("class", "")
        score_class = get_class_similarity(model, input_element.get("class", ""), element_class)

        options = {option.get('value'): option.text for option in element.find_all('option')}
        score_select = get_select_tag_similarity(input_element['options'], options)

        score = (weights["class"] * score_class) + (weights["select"] * score_select) + (weights["attribute_similarity"] * attribute_similarity)

    elif input_element["tag"] == "img":
        weights = {"attribute_similarity": 0.2, "data-aura-rendered-by": 0.2, "class": 0.2, "alt": 0.4}
        
        element_alt = element.get_text(strip=True)
        element_class = element.get("class", "")
        element_render = element.get("data-aura-rendered-by", "0")

        score_alt = get_contextual_similarity(model, input_element.get("alt", ""), element_alt)
        score_class = get_class_similarity(model, input_element.get("class", ""), element_class)
        score_render = get_numeric_similarity(input_element.get("data-aura-rendered-by", "0"), element_render, min_render_value, max_render_value)

        score = (weights["class"] * score_class) + (weights["alt"] * score_alt) + (weights["data-aura-rendered-by"] * score_render) + (weights["attribute_similarity"] * attribute_similarity)

    elif input_element["tag"] == "lightning-icon":
        weights = {"attribute_similarity": 0.25, "data-aura-rendered-by": 0.2, "class": 0.55}
        
        element_render = element.get("data-aura-rendered-by", "0")
        element_class = element.get("class", "")

        score_render = get_numeric_similarity(input_element.get("data-aura-rendered-by", "0"), element_render, min_render_value, max_render_value)
        score_class = get_class_similarity(model, input_element.get("class", ""), element_class)

        score = (weights["class"] * score_class) + (weights["data-aura-rendered-by"] * score_render) + (weights["attribute_similarity"] * attribute_similarity)

    elif input_element["tag"] == "div":
        weights = {"attribute_similarity": 0.25, "class": 0.55, "style": 0.2}
            
        element_class = element.get("class", "")
        element_style = element.get("style", "")

        score_class = get_class_similarity(model, input_element.get("class", ""), element_class)
        score_style = get_style_similarity(input_element.get("style", ""), element_style)

        score = (weights["class"] * score_class) + (weights["style"] * score_style) + (weights["attribute_similarity"] * attribute_similarity)

    return score



# Find the minimum and maximum values of the 'data-aura-rendered-by' attribute.
def find_min_max_render_values(all_elements):
    min_value = float('inf')
    max_value = float('-inf')
    for element in all_elements:
        value = element.get("data-aura-rendered-by", "0")
        if value != "0":
            numeric_value = int((value.split(":"))[0])
            if numeric_value < min_value:
                min_value = numeric_value
            if numeric_value > max_value:
                max_value = numeric_value
    return min_value, max_value

# Find the best matching element based on the calculated similarity scores.
# Print all matches and return the best match and its score.
def find_best_match(all_elements, input_element, model, render_value=None):
    best_match = None
    best_score = float("-inf")
    matches = []

    if not render_value:
        # Calculate min and max values for normalization
        min_render_value, max_render_value = find_min_max_render_values(all_elements)
    else:
        max_render_value = render_value[0]
        min_render_value = render_value[1]

    for element in all_elements:
        score = calculate_element_score(input_element, element, model, min_render_value, max_render_value)

        matches.append({
            "id": element.get("id", ""),
            "tag": element.name,
            "type": element.get("type", ""),
            "href": element.get("href", ""),
            "data-aura-rendered-by": element.get("data-aura-rendered-by", ""),
            "score": score
        })

        if score > best_score:
            best_match = element
            best_score = score

    return best_match, best_score

from collections import defaultdict

def find_best_match_recursive(dom_elements, all_elements, model):
    # Dictionary to store scores for each input element
    input_scores = defaultdict(dict)
    print("INPUT: ", all_elements)

    # Calculate min and max values for normalization
    min_render_value, max_render_value = find_min_max_render_values(dom_elements)

    for input_element in all_elements:
        print(f"Processing input element: {input_element}")
        
        # Find all all_elements in the DOM with the same tag as the input element
        for element in dom_elements:
            score = calculate_element_score(input_element, element, model, min_render_value, max_render_value)

            # Store the score in the input_scores dictionary
            input_scores[input_element].append({
                "element": element,
                "score": score
            })

    print("Scores for each input element:")
    for input_element, scores in input_scores.items():
        print(f"Input Element: {input_element}")
        for score_data in scores:
            print(f"  Element: {score_data['element']}, Score: {score_data['score']}")

    return input_scores


def parse_input_html_list(html_content):
    soup = BeautifulSoup(html_content, "lxml")
    elements_list = []
    parents_list = []

    def collect_elements(element, parent_html):
        for child in element.find_all(recursive=False):
            attributes = dict(child.attrs)
            attributes["tag"] = child.name
            if child.name not in [
                    'lightning-icon',
                    'input',
                    'h1',
                    'h2',
                    'h3',
                    'h4',
                    'h5',
                    'h6',
                    'a',
                    'span',
                    'label',
                    'button',
                    'select',
                    'img'
                ]:
                elements_list.append(attributes)  # Append before collecting children
                parents_list.append(parent_html)
                collect_elements(child, str(child))
            else:
                put = parse_input_html(str(child))
                elements_list.append(put)
                parents_list.append(parent_html)

    main_div = soup.find("div")
    if main_div:
        collect_elements(main_div, str(main_div))

    return elements_list, parents_list



# Main function to run the algorithm.
def main():
    # Path to the locally saved model file
    model_path = "../word2vec-google-news-300.bin"

    # Fetch the paths to the DOM and input files
    dom, error = fetchInput()
    
    # Load the word2vec model
    model = load_model(model_path)

    # Read and parse the HTML content (DOM Tree)
    dom_tree = read_html_file(dom)
    soup = parse_html(dom_tree)

    # Read and parse the input element from the input file
    error_log = read_input_file(error)
    input_element = parse_input_html(error_log)

    # Finding best match for a single element
    if input_element["tag"] != "div":
        all_elements = soup.find_all(input_element["tag"])
        best_match_input, probability = find_best_match(all_elements, input_element, model)

    # IGNORE THIS BLOCK (Under Development) -------------------------------------------
    # Finding best match recursively for multiple elements
    else:
        input_elements, parent_elements = parse_input_html_list(error_log)
        probability = -1
        
        min_max_scores = dict()
        for item in input_elements:
            if item['tag'] not in min_max_scores:
                all_elements = soup.find_all(item['tag'])
                min_max_scores[item['tag']] = find_min_max_render_values(all_elements)

        parent_scores = defaultdict(list)
        
        for index, value in enumerate(input_elements):
            soup = parse_html(parent_elements[index])
            all_elements = soup.find_all(value["tag"])

            match, score = find_best_match(all_elements, value, model, min_max_scores[value['tag']])
            
            parent_scores[parent_elements[index]].append(score)

        for key in parent_scores:
            if len(parent_scores[key]) >= 2*len(input_elements):
                parent_scores[key] = 0
                continue
            elif len(parent_scores[key]) > len(input_elements):
                parent_scores[key].sort(reversed=True)
                parent_scores[key] = parent_scores[key][:len(parent_scores[key]) - len(input_elements)]

            parent_scores[key] = sum(parent_scores[key]) / len(input_elements)

        for key, value in parent_scores.items():
            if value > probability:
                probability = value
                best_match_input = key
    # IGNORE THIS BLOCK (Under Development) -------------------------------------------

    # Print the final choice and its probability
    if best_match_input: 
        if input_element["tag"] == "div":
            print("\nBest Match -------------------------")
            print(f"Accuracy: v{probability:.2f}")
            # print(f"Division: {best_match_input}")
            print("End --------------------------------")
        else:
            print("\nBest Match -------------------------")
            print(f"Accuracy: {probability:.2f}")
            print(f"Tag: {best_match_input.name}")
            print(f"Text: {best_match_input.text}")
            for attr, value in best_match_input.attrs.items():
                print(f"{attr}: {value}")
            print("End --------------------------------")

    else:
        print("\nNo matching element found.")

if __name__ == "__main__":
    main()

