from flask import Flask, jsonify, request, send_from_directory
import sqlite3

app = Flask(__name__, static_folder='.')

def get_restaurants(limit=10, offset=0):
    conn = sqlite3.connect('zomato.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM restaurants LIMIT ? OFFSET ?", (limit, offset))
    restaurants = cursor.fetchall()
    conn.close()
    return restaurants

def get_restaurant_by_id(restaurant_id):
    conn = sqlite3.connect('zomato.db')
    conn.row_factory = sqlite3.Row  # This will allow us to access columns by name
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM restaurants WHERE Restaurant_ID = ?", (restaurant_id,))
    restaurant = cursor.fetchone()
    print(restaurant)
    new_votes=restaurant['Votes']+1
    conn.execute("UPDATE restaurants SET Votes= ? WHERE Restaurant_ID=?", (new_votes, restaurant_id))
    conn.commit()
    if restaurant:
        restaurant_dict = dict(restaurant)
        reviews = conn.execute('SELECT * FROM reviews WHERE Restaurant_ID = ? ORDER BY timestamp DESC', (restaurant_id,)).fetchall()
        reviews_list = [dict(review) for review in reviews]
        restaurant_dict['reviews'] = reviews_list
    else:
        restaurant_dict = None

    conn.close()
    print(restaurant_dict)
    return restaurant_dict
    # conn.close()
    # return restaurant

def get_restaurants_by_country(country_code, limit=10, offset=0):
    conn = sqlite3.connect('zomato.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.*, c.Country_Name 
        FROM restaurants r 
        JOIN country c ON r.Country_Code = c.Country_Code 
        WHERE r.Country_Code = ?
        LIMIT ? OFFSET ?
    """, (country_code, limit, offset))
    restaurants = cursor.fetchall()
    conn.close()
    return restaurants

def get_total_restaurants_by_country(country_code):
    conn = sqlite3.connect('zomato.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) 
        FROM restaurants 
        WHERE Country_Code = ?
    """, (country_code,))
    count = cursor.fetchone()[0]
    conn.close()
    return count


def get_restaurants_by_cost(cost, limit=10, offset=0):
    conn = sqlite3.connect('zomato.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.*, c.Country_Name 
        FROM restaurants r 
        JOIN country c ON r.Country_Code = c.Country_Code 
        WHERE r.Average_Cost_for_Two <= ?
        LIMIT ? OFFSET ?
    """, (cost, limit, offset))
    restaurants = cursor.fetchall()
    conn.close()
    return restaurants

def get_total_restaurants_by_cost(cost):
    conn = sqlite3.connect('zomato.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) 
        FROM restaurants 
        WHERE Average_Cost_for_Two <= ?
    """, (cost,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_countries():
    conn = sqlite3.connect('zomato.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM country")
    countries = cursor.fetchall()
    conn.close()
    return countries

def get_restaurants_by_cuisine(cuisine, limit=10, offset=0):
    conn = sqlite3.connect('zomato.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT r.*, c.Country_Name 
        FROM restaurants r 
        JOIN country c ON r.Country_Code = c.Country_Code 
        WHERE r.Cuisines LIKE ?
        LIMIT ? OFFSET ?
    """, (f'%{cuisine}%', limit, offset))
    restaurants = cursor.fetchall()
    conn.close()
    return restaurants

def get_total_restaurants_by_cuisine(cuisine):
    conn = sqlite3.connect('zomato.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) 
        FROM restaurants r 
        WHERE r.Cuisines LIKE ?
    """, (f'%{cuisine}%',))
    count = cursor.fetchone()[0]
    conn.close()
    return count



@app.route('/home.html')
def home():
    return send_from_directory('.', 'home.html')

@app.route('/index.html')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/restaurant.html')
def restaurant_detail():
    return send_from_directory('.', 'restaurant.html')

@app.route('/search.html')
def search_page():
    return send_from_directory('.', 'search.html')

@app.route('/search_by_country.html')
def search_by_country_page():
    return send_from_directory('.', 'search_by_country.html')

@app.route('/search_by_cost.html')
def search_by_cost_page():
    return send_from_directory('.', 'search_by_cost.html')

@app.route('/search_by_cuisine.html')
def search_by_cuisine_page():
    return send_from_directory('.', 'search_by_cuisine.html')

@app.route('/api/restaurants', methods=['GET'])
def get_restaurants_list():
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    restaurants = get_restaurants(limit, offset)
    return jsonify(restaurants)

# @app.route('/api/restaurants/<int:restaurant_id>', methods=['GET'])
# def get_restaurant_by_id_route(restaurant_id):
#     restaurant = get_restaurant_by_id(restaurant_id)
#     return jsonify(restaurant)

@app.route('/api/restaurants/<int:restaurant_id>', methods=['GET'])
def get_restaurant_by_id_route(restaurant_id):
    restaurant = get_restaurant_by_id(restaurant_id)
    if restaurant:
        return jsonify(restaurant)
    else:
        return jsonify({"error": "Restaurant not found"}), 404


@app.route('/api/restaurants/country/<int:country_code>', methods=['GET'])
def get_restaurants_by_country_route(country_code):
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    restaurants = get_restaurants_by_country(country_code, limit, offset)
    total_count = get_total_restaurants_by_country(country_code)
    return jsonify({
        'restaurants': restaurants,
        'total_count': total_count
    })


@app.route('/api/restaurants/cost/<int:cost>', methods=['GET'])
def get_restaurants_by_cost_route(cost):
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    restaurants = get_restaurants_by_cost(cost, limit, offset)
    total_count = get_total_restaurants_by_cost(cost)
    return jsonify({
        'restaurants': restaurants,
        'total_count': total_count
    })

@app.route('/api/countries', methods=['GET'])
def get_countries_route():
    countries = get_countries()
    return jsonify(countries)

@app.route('/api/restaurants/cuisine/<string:cuisine>', methods=['GET'])
def get_restaurants_by_cuisine_route(cuisine):
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    restaurants = get_restaurants_by_cuisine(cuisine, limit, offset)
    total_count = get_total_restaurants_by_cuisine(cuisine)
    return jsonify({
        'restaurants': restaurants,
        'total_count': total_count
    })

@app.route('/api/reviews', methods=['POST'])
def add_review():
    data = request.json
    restaurant_id = data.get('restaurant_id')
    username = data.get('username')
    review_text = data.get('review_text')
    rating = data.get('rating')
    
    if not all([restaurant_id, username, review_text, rating]):
        return jsonify({"error": "Missing required fields"}), 400
    
    try:
        conn = sqlite3.connect('zomato.db')
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO reviews (Restaurant_ID, username, review_text, rating)
            VALUES (?, ?, ?, ?)
        """, (restaurant_id, username, review_text, rating))
        
        conn.commit()
        conn.close()
        return jsonify({"message": "Review added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500




# @app.route('/api/restaurant_by_name/<string:name>', methods=['GET'])
# def get_restaurant_by_name_route(name):
#     restaurants = get_restaurants_by_cuisine(cuisine, limit, offset)
#     total_count = get_total_restaurants_by_cuisine(cuisine)
#     return jsonify({
#         'restaurants': restaurants,
#         'total_count': total_count
#     })

if __name__ == '__main__':
    app.run(debug=True)

# def get_restaurants_by_country(country_code):
#     conn = sqlite3.connect('zomato.db')
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT r.*, c.Country_Name 
#         FROM restaurants r 
#         JOIN country c ON r.Country_Code = c.Country_Code 
#         WHERE r.Country_Code = ?
#     """, (country_code,))
#     restaurants = cursor.fetchall()
#     conn.close()
#     return restaurants

# def get_restaurants_by_cost(cost):
#     conn = sqlite3.connect('zomato.db')
#     cursor = conn.cursor()
#     cursor.execute("""
#         SELECT r.*, c.Country_Name 
#         FROM restaurants r 
#         JOIN country c ON r.Country_Code = c.Country_Code 
#         WHERE r.Average_Cost_for_Two <= ?
#     """, (cost,))
#     restaurants = cursor.fetchall()
#     conn.close()
#     return restaurants

# @app.route('/api/restaurants/country/<int:country_code>', methods=['GET'])
# def get_restaurants_by_country_route(country_code):
#     restaurants = get_restaurants_by_country(country_code)
#     return jsonify(restaurants)

# @app.route('/api/restaurants/cost/<int:cost>', methods=['GET'])
# def get_restaurants_by_cost_route(cost):
#     restaurants = get_restaurants_by_cost(cost)
#     return jsonify(restaurants)


