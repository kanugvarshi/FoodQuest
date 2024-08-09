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
    restaurants = data[0].get('restaurants')
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
input_file = 'static/data/file4.json'
output_file = 'static/data/restaurant4_urls.json'

# Run the extraction
extract_data(input_file, output_file)

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Restaurant Detail</title>
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body{
            /* background-color:cornsilk; */
            background-image: url('https://wallpapers.com/downloads/high/restaurant-in-park-hyatt-tokyo-japan-a3r62zoiuwz7uhra.webp');
            background-size: cover; 
            background-position: center; 
        }
        .jumbotron{
            background-image: url('https://as1.ftcdn.net/v2/jpg/05/04/19/00/1000_F_504190003_lC3anwzZyEvJPmtGbTC5XgL5fmoS9XHB.jpg');
            background-size: cover; 
            background-position: center; 
        }
        .container {
            margin-top: 50px;
        }
        .card {
            background-image: url('https://images.pexels.com/photos/616401/pexels-photo-616401.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1');
            background-size: cover; 
            background-position: center; 
            border-radius: 0.5rem;
            padding-left: 150px;
        }
        .btn-secondary {
            background-color: #6c757d;
            border: none;
        }
        .btn-secondary:hover {
            background-color: #5a6268;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="jumbotron text-center">
            <h1 class="display-4" id="restaurant-name">Restaurant Detail</h1>
            <p class="lead">Find out more about this restaurant.</p>
        </div>

        <!-- Restaurant Detail Card -->
        <div id="restaurant-detail" class="card mb-4">
            <div class="card-body">
                <p><strong>Address:</strong> <span id="restaurant-address"></span></p>
                <p><strong>Cuisines:</strong> <span id="restaurant-cuisines"></span></p>
                <p><strong>Average Cost for Two:</strong> <span id="restaurant-cost"></span></p>
                <p><strong>Locality Verbose:</strong> <span id="locality"></span></p>
                <p><strong>Longitude:</strong> <span id="longitude"></span></p>
                <p><strong>Latitude:</strong> <span id="latitude"></span></p>
                <p><strong>Aggregate Rating:</strong> <span id="restaurant-rating"></span></p>
                <p><strong>Votes:</strong> <span id="restaurant-votes"></span></p>
            </div>
        </div>

        <!-- Review Section -->
        <div id="review-section" class="card mb-4">
            <div class="card-body">
                <h5 class="card-title">Reviews</h5>
                <div id="reviews-list"></div>
            </div>
        </div>

        <!-- Review Form -->
        <div class="card mb-4">
            <div class="card-body">
                <h5 class="card-title">Add a Review</h5>
                <form id="review-form">
                    <div class="form-group">
                        <label for="username">Name:</label>
                        <input type="text" class="form-control" id="username" required>
                    </div>
                    <div class="form-group">
                        <label for="review_text">Review:</label>
                        <textarea class="form-control" id="review_text" rows="3" required></textarea>
                    </div>
                    <div class="form-group">
                        <label for="rating">Rating:</label>
                        <select class="form-control" id="rating" required>
                            <option value="1">1</option>
                            <option value="2">2</option>
                            <option value="3">3</option>
                            <option value="4">4</option>
                            <option value="5">5</option>
                        </select>
                    </div>
                    <button type="submit" class="btn btn-primary">Submit Review</button>
                </form>
            </div>
        </div>

        <!-- Back to Index Button -->
        <div class="text-center mt-4">
            <a href="index.html" class="btn btn-secondary">Back to Restaurant List</a>
        </div>
    </div>

    <!-- JavaScript Libraries -->
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script>
        function getQueryParameter(name) {
            const urlParams = new URLSearchParams(window.location.search);
            return urlParams.get(name);
        }

        $(document).ready(function() {
            const restaurantId = getQueryParameter('id');
            if (restaurantId) {
                $.ajax({
                    url: `/api/restaurants/${restaurantId}`,
                    method: 'GET',
                    success: function(data) {
                        if (data) {
                            $('#restaurant-name').text(data.Restaurant_Name);
                            $('#restaurant-address').text(`${data.City},${data.Address}`);
                            $('#restaurant-cuisines').text(data.Cuisines);
                            $('#locality').text(data.Locality_Verbose);
                            $('#longitude').text(data.Longitude);
                            $('#latitude').text(data.Latitude);
                            $('#restaurant-cost').text(`${data.Average_Cost_for_two} ${data.Currency}`);
                            $('#restaurant-rating').text(`${data.Aggregate_rating} (${data.Rating_text})`);
                            $('#restaurant-votes').text(data.Votes);
                            // Display reviews
                            const reviewsList = $('#reviews-list');
                                reviewsList.empty();
                                data.reviews.forEach(review => {
                                    const reviewItem = `
                                        <div class="review">
                                            <p><strong>${review.username}</strong> (${review.rating} stars):</p>
                                            <p>${review.review_text}</p>
                                            <hr>
                                        </div>
                                    `;
                                    reviewsList.append(reviewItem);
                                });
                            }
                        else {
                            $('#restaurant-detail').html('<p class="text-danger">No details found for this restaurant.</p>');
                        }
                    },
                    error: function() {
                        $('#restaurant-detail').html('<p class="text-danger">Error fetching restaurant details.</p>');
                    }
                });
            }
        });
    </script>
</body>
</html>
