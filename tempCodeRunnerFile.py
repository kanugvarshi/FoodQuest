import json

# Load data from the input JSON file
def load_data(input_file):
    with open(input_file, 'r', encoding='latin1') as file:
        data = json.load(file)
    return data

# Write extracted data to the output JSON file
def write_data_to_file(output_file, data):
    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)

def extract_data(input_file, output_file):
    # Load the data from the JSON file
    data = load_data(input_file)
    
    # Extract relevant information
    restaurants = data.get('restaurants', [])
    results = []
    
    for restaurant in restaurants:
        res_id = restaurant['restaurant'].get('R', {}).get('res_id', None)
        url = restaurant['restaurant'].get('url', None)
        
        if res_id and url:
            results.append({
                'res_id': res_id,
                'url': url
            })
    
    # Save the results to the new JSON file
    write_data_to_file(output_file, results)
    print(f'Data has been extracted and saved to {output_file}')

# Define file paths
input_file = 'static/data/file1_cleaned.json'
output_file = 'static/data/restaurant1_urls.json'

# Run the extraction
extract_data(input_file, output_file)
