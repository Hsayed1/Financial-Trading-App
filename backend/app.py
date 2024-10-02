# app.py
from flask import Flask, request, jsonify
import yfinance as yf
from flask_cors import CORS
import sqlite3
from database import get_db_connection

app = Flask(__name__)
CORS(app)  

# Endpoint to query stock ticker
@app.route('/stocks/<ticker>', methods=['GET'])
def query_stock(ticker):  # The ticker is passed as a URL parameter
    try:
        # Query stock information using yfinance
        print(ticker)
        stock = yf.Ticker(ticker)
        stock_info = stock.info
        
        # Prepare the response with relevant information
        response = {
            'name': stock_info.get('shortName', 'N/A'),
            'price': round(stock_info.get('currentPrice', 0), 3),
        }
        
        return jsonify(response), 200 
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500  

# Endpoint to buy stock
@app.route('/buy', methods=['POST'])
def buy_stock():
    stock_name = request.json.get('stock_name')
    count = request.json.get('count')

    if stock_name and isinstance(count, int) and count > 0:
        stock = yf.Ticker(stock_name)
        current_price = stock.info.get('currentPrice')

        if current_price is None:
            return jsonify({'error': 'Stock not found!'}), 404

        with get_db_connection() as conn:
            conn.execute('INSERT INTO portfolio (stock_name, purchase_price, count) VALUES (?, ?, ?)',
                         (stock_name, current_price, count))
            conn.commit()
        return jsonify({'message': 'Stock purchased successfully!'}), 201

    return jsonify({'error': 'Invalid data!'}), 400

# Endpoint to retrieve portfolio
@app.route('/portfolio', methods=['GET'])
def get_portfolio():
    with get_db_connection() as conn:
        portfolio = conn.execute('SELECT * FROM portfolio').fetchall()
        return jsonify([dict(row) for row in portfolio]), 200

if __name__ == '__main__':
    app.run(debug=True)
