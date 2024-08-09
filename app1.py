
#WEB API THAT SUPPORTS PAGINAITION

from flask import Flask, jsonify
import sqlite3

app1 = Flask(__name__)

PER_PAGE = 10

def get_restaurants(page=1):
    """
    Retrieves restaurants with pagination.

    Args:
        page (int, optional): The current page number. Defaults to 1.

    Returns:
        list: A list of restaurants for the requested page.
        int: The total number of restaurants.
    """
    conn = sqlite3.connect('zomato.db')
    cursor = conn.cursor()

    # Calculate offset based on page number
    offset = (page - 1) * PER_PAGE

    # Get the total number of restaurants
    cursor.execute("SELECT COUNT(*) FROM restaurants")
    total_restaurants = cursor.fetchone()[0]

    # Get restaurants for the current page
    cursor.execute("SELECT * FROM restaurants LIMIT ? OFFSET ?", (PER_PAGE, offset))
    restaurants = cursor.fetchall()

    conn.close()
    return restaurants, total_restaurants

def get_restaurant_by_id(restaurant_id):
    """
    Retrieves a restaurant by its ID.

    Args:
        restaurant_id (int): The ID of the restaurant to retrieve.

    Returns:
        dict: A dictionary containing the restaurant details, or None if not found.
    """
    conn = sqlite3.connect('zomato.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM restaurants WHERE Restaurant_ID = ?", (restaurant_id,))
    restaurant = cursor.fetchone()
    conn.close()
    return restaurant

@app1.route('/api/restaurants/page=<int:page>')
def get_restaurants_list(page):
    """
    Returns a paginated list of restaurants.

    Args:
        page (int): The requested page number.

    Returns:
        JSON: A JSON object containing restaurants and pagination information.
    """
    restaurants, total_restaurants = get_restaurants(page)

    # Calculate total number of pages
    total_pages = (total_restaurants + PER_PAGE - 1) // PER_PAGE

    # Calculate next page
    next_page = page + 1 if page < total_pages else None
    

    return jsonify({
        'restaurants': restaurants,
        'total_restaurants': total_restaurants,
        'current_page': page,
        'total_pages': total_pages,
        'next_page' : next_page
    })

@app1.route('/api/restaurants/<int:restaurant_id>')
def get_restaurant_by_id_route(restaurant_id):
    """
    Endpoint for retrieving a restaurant by ID.

    Args:
        restaurant_id (int): The ID of the restaurant to retrieve.

    Returns:
        JSON: A JSON object containing the restaurant details, or an error message if not found.
    """
    restaurant = get_restaurant_by_id(restaurant_id)
    if restaurant:
        return jsonify(restaurant)
    else:
        return jsonify({'error': 'Restaurant not found'}), 404

if __name__ == '__main__':
    app1.run(debug=True)
