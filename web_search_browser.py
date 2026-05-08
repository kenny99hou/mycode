#!/usr/bin/env python3
"""
BMW X3 Used Car Deal Finder - Web Version

This Flask web application displays BMW X3 deals in a browser interface
with sorting, filtering, and detailed car information.
"""

from flask import Flask, render_template_string, request, jsonify
import json
import time
import re
from datetime import datetime
from typing import List, Dict, Optional
import csv

app = Flask("BMW_X3_Deal_Finder")

class BMWX3DealFinder:
    def __init__(self):
        self.deals = []
    
    def clean_price(self, price_text: str) -> Optional[float]:
        """Extract and clean price from text"""
        if not price_text:
            return None
        
        price_text = re.sub(r'[^\d.,]', '', price_text)
        price_text = price_text.replace(',', '.')
        
        try:
            match = re.search(r'\d+\.?\d*', price_text)
            if match:
                return float(match.group())
        except ValueError:
            pass
        
        return None
    
    def clean_year(self, year_text: str) -> Optional[int]:
        """Extract year from text"""
        if not year_text:
            return None
        
        try:
            match = re.search(r'\b(20\d{2})\b', year_text)
            if match:
                return int(match.group())
        except ValueError:
            pass
        
        return None
    
    def clean_mileage(self, mileage_text: str) -> Optional[int]:
        """Extract mileage from text"""
        if not mileage_text:
            return None
        
        mileage_text = re.sub(r'[^\d.,]', '', mileage_text).replace(',', '')
        
        try:
            match = re.search(r'\d+', mileage_text)
            if match:
                return int(match.group())
        except ValueError:
            pass
        
        return None
    
    def create_sample_data(self) -> List[Dict]:
        """Create sample BMW X3 data for demonstration"""
        sample_deals = [
            {
                'title': '2018 BMW X3 xDrive30i',
                'price': 28995.00,
                'year': 2018,
                'mileage': 45000,
                'source': 'AutoTrader',
                'url': 'https://www.autotrader.com/cars-for-sale/used/2018/bmw/x3/vehicleid/538724234',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': '2019 BMW X3 xDrive28i',
                'price': 32450.00,
                'year': 2019,
                'mileage': 38000,
                'source': 'Cars.com',
                'url': 'https://www.cars.com/vehicledetail/detail/362849342/2019/bmw/x3/28i',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': '2020 BMW X3 M40i',
                'price': 42500.00,
                'year': 2020,
                'mileage': 28000,
                'source': 'CarGurus',
                'url': 'https://www.cargurus.com/Cars/inventorylisting/viewListing.action?sourceId=1&listingId=308234567',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': '2017 BMW X3 xDrive35i',
                'price': 24995.00,
                'year': 2017,
                'mileage': 62000,
                'source': 'AutoTrader',
                'url': 'https://www.autotrader.com/cars-for-sale/used/2017/bmw/x3/vehicleid/538724235',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': '2021 BMW X3 xDrive30i',
                'price': 38995.00,
                'year': 2021,
                'mileage': 22000,
                'source': 'Cars.com',
                'url': 'https://www.cars.com/vehicledetail/detail/362849343/2021/bmw/x3/30i',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': '2016 BMW X3 xDrive28i',
                'price': 19995.00,
                'year': 2016,
                'mileage': 85000,
                'source': 'CarGurus',
                'url': 'https://www.cargurus.com/Cars/inventorylisting/viewListing.action?sourceId=1&listingId=308234568',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': '2022 BMW X3 xDrive30i',
                'price': 45995.00,
                'year': 2022,
                'mileage': 15000,
                'source': 'AutoTrader',
                'url': 'https://www.autotrader.com/cars-for-sale/used/2022/bmw/x3/vehicleid/538724236',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': '2015 BMW X3 xDrive35i',
                'price': 16995.00,
                'year': 2015,
                'mileage': 95000,
                'source': 'Cars.com',
                'url': 'https://www.cars.com/vehicledetail/detail/362849344/2015/bmw/x3/35i',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': '2019 BMW X3 M40i',
                'price': 39995.00,
                'year': 2019,
                'mileage': 35000,
                'source': 'CarGurus',
                'url': 'https://www.cargurus.com/Cars/inventorylisting/viewListing.action?sourceId=1&listingId=308234569',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': '2020 BMW X3 xDrive28i',
                'price': 35995.00,
                'year': 2020,
                'mileage': 30000,
                'source': 'AutoTrader',
                'url': 'https://www.autotrader.com/cars-for-sale/used/2020/bmw/x3/vehicleid/538724237',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': '2018 BMW X3 M40i',
                'price': 32995.00,
                'year': 2018,
                'mileage': 42000,
                'source': 'Cars.com',
                'url': 'https://www.cars.com/vehicledetail/detail/362849345/2018/bmw/x3/m40i',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': '2021 BMW X3 M40i',
                'price': 48995.00,
                'year': 2021,
                'mileage': 18000,
                'source': 'CarGurus',
                'url': 'https://www.cargurus.com/Cars/inventorylisting/viewListing.action?sourceId=1&listingId=308234570',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': '2017 BMW X3 xDrive30i',
                'price': 22995.00,
                'year': 2017,
                'mileage': 68000,
                'source': 'AutoTrader',
                'url': 'https://www.autotrader.com/cars-for-sale/used/2017/bmw/x3/vehicleid/538724238',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': '2019 BMW X3 xDrive30i',
                'price': 34995.00,
                'year': 2019,
                'mileage': 40000,
                'source': 'Cars.com',
                'url': 'https://www.cars.com/vehicledetail/detail/362849346/2019/bmw/x3/30i',
                'scraped_at': datetime.now().isoformat()
            },
            {
                'title': '2016 BMW X3 xDrive30i',
                'price': 18995.00,
                'year': 2016,
                'mileage': 89000,
                'source': 'CarGurus',
                'url': 'https://www.cargurus.com/Cars/inventorylisting/viewListing.action?sourceId=1&listingId=308234571',
                'scraped_at': datetime.now().isoformat()
            }
        ]
        
        return sample_deals
    
    def calculate_value_score(self, deal: Dict) -> float:
        """Calculate a value score for each deal (lower is better)"""
        price = deal['price']
        year = deal['year']
        mileage = deal.get('mileage', 100000)
        current_year = datetime.now().year
        
        age_penalty = (current_year - year) * 500
        mileage_penalty = (mileage / 10000) * 200
        value_score = price + age_penalty + mileage_penalty
        
        return value_score
    
    def get_deals(self) -> List[Dict]:
        """Get all deals with value scores"""
        deals = self.create_sample_data()
        for deal in deals:
            deal['value_score'] = self.calculate_value_score(deal)
        return deals

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BMW X3 Used Car Deal Finder</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
        }
        
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
        }
        
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #2a5298;
            margin-bottom: 5px;
        }
        
        .stat-label {
            color: #6c757d;
            font-size: 0.9em;
        }
        
        .filters {
            padding: 20px 30px;
            background: #fff;
            border-bottom: 1px solid #e9ecef;
            display: flex;
            gap: 20px;
            align-items: center;
            flex-wrap: wrap;
        }
        
        .filter-group {
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .filter-group label {
            font-weight: 600;
            color: #495057;
        }
        
        .filter-group select,
        .filter-group input {
            padding: 8px 12px;
            border: 2px solid #e9ecef;
            border-radius: 5px;
            font-size: 14px;
            transition: border-color 0.3s ease;
        }
        
        .filter-group select:focus,
        .filter-group input:focus {
            outline: none;
            border-color: #2a5298;
        }
        
        .sort-buttons {
            display: flex;
            gap: 10px;
            margin-left: auto;
        }
        
        .sort-btn {
            padding: 8px 16px;
            background: #6c757d;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            transition: background 0.3s ease;
            font-size: 14px;
        }
        
        .sort-btn:hover {
            background: #5a6268;
        }
        
        .sort-btn.active {
            background: #2a5298;
        }
        
        .car-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
            padding: 30px;
        }
        
        .car-card {
            background: white;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 1px solid #e9ecef;
        }
        
        .car-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }
        
        .car-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            position: relative;
        }
        
        .car-title {
            font-size: 1.3em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .car-year {
            font-size: 1.1em;
            opacity: 0.9;
        }
        
        .car-badge {
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(255,255,255,0.2);
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.8em;
            font-weight: bold;
        }
        
        .car-body {
            padding: 20px;
        }
        
        .car-price {
            font-size: 2em;
            font-weight: bold;
            color: #2a5298;
            margin-bottom: 15px;
        }
        
        .car-details {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-bottom: 15px;
        }
        
        .detail-item {
            display: flex;
            align-items: center;
            gap: 5px;
            font-size: 0.9em;
            color: #6c757d;
        }
        
        .detail-label {
            font-weight: 600;
        }
        
        .car-link {
            display: block;
            width: 100%;
            padding: 12px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            text-align: center;
            border-radius: 5px;
            font-weight: bold;
            transition: opacity 0.3s ease;
        }
        
        .car-link:hover {
            opacity: 0.9;
        }
        
        .value-score {
            background: #28a745;
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.8em;
            font-weight: bold;
            display: inline-block;
            margin-bottom: 10px;
        }
        
        .no-results {
            text-align: center;
            padding: 40px;
            color: #6c757d;
            font-size: 1.2em;
        }
        
        @media (max-width: 768px) {
            .car-grid {
                grid-template-columns: 1fr;
            }
            
            .filters {
                flex-direction: column;
                align-items: stretch;
            }
            
            .sort-buttons {
                margin-left: 0;
                justify-content: center;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚗 BMW X3 Used Car Deal Finder</h1>
            <p>Find the best BMW X3 deals sorted by price and year</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number" id="total-deals">0</div>
                <div class="stat-label">Total Deals</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="price-range">$0</div>
                <div class="stat-label">Price Range</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="year-range">0</div>
                <div class="stat-label">Year Range</div>
            </div>
            <div class="stat-card">
                <div class="stat-number" id="avg-price">$0</div>
                <div class="stat-label">Average Price</div>
            </div>
        </div>
        
        <div class="filters">
            <div class="filter-group">
                <label>Min Year:</label>
                <select id="min-year">
                    <option value="">All</option>
                </select>
            </div>
            <div class="filter-group">
                <label>Max Year:</label>
                <select id="max-year">
                    <option value="">All</option>
                </select>
            </div>
            <div class="filter-group">
                <label>Max Price:</label>
                <input type="number" id="max-price" placeholder="No limit">
            </div>
            <div class="filter-group">
                <label>Max Mileage:</label>
                <input type="number" id="max-mileage" placeholder="No limit">
            </div>
            <div class="sort-buttons">
                <button class="sort-btn active" data-sort="price-year">Price ↓ Year ↓</button>
                <button class="sort-btn" data-sort="price">Price ↑</button>
                <button class="sort-btn" data-sort="year">Year ↓</button>
                <button class="sort-btn" data-sort="value">Best Value</button>
            </div>
        </div>
        
        <div class="car-grid" id="car-grid">
            <!-- Car cards will be inserted here -->
        </div>
    </div>
    
    <script>
        let allDeals = [];
        let currentSort = 'price-year';
        
        // Fetch deals from server
        fetch('/api/deals')
            .then(response => response.json())
            .then(data => {
                allDeals = data.deals;
                populateYearFilters();
                updateStats();
                renderDeals();
            });
        
        function populateYearFilters() {
            const years = [...new Set(allDeals.map(deal => deal.year))].sort();
            const minYearSelect = document.getElementById('min-year');
            const maxYearSelect = document.getElementById('max-year');
            
            years.forEach(year => {
                minYearSelect.innerHTML += `<option value="${year}">${year}</option>`;
                maxYearSelect.innerHTML += `<option value="${year}">${year}</option>`;
            });
        }
        
        function updateStats() {
            const filteredDeals = getFilteredDeals();
            const prices = filteredDeals.map(deal => deal.price);
            const years = filteredDeals.map(deal => deal.year);
            
            document.getElementById('total-deals').textContent = filteredDeals.length;
            document.getElementById('price-range').textContent = 
                prices.length > 0 ? `$${Math.min(...prices).toLocaleString()} - $${Math.max(...prices).toLocaleString()}` : '$0';
            document.getElementById('year-range').textContent = 
                years.length > 0 ? `${Math.min(...years)} - ${Math.max(...years)}` : '0';
            document.getElementById('avg-price').textContent = 
                prices.length > 0 ? `$${Math.round(prices.reduce((a, b) => a + b, 0) / prices.length).toLocaleString()}` : '$0';
        }
        
        function getFilteredDeals() {
            let filtered = [...allDeals];
            
            const minYear = document.getElementById('min-year').value;
            const maxYear = document.getElementById('max-year').value;
            const maxPrice = document.getElementById('max-price').value;
            const maxMileage = document.getElementById('max-mileage').value;
            
            if (minYear) filtered = filtered.filter(deal => deal.year >= parseInt(minYear));
            if (maxYear) filtered = filtered.filter(deal => deal.year <= parseInt(maxYear));
            if (maxPrice) filtered = filtered.filter(deal => deal.price <= parseFloat(maxPrice));
            if (maxMileage) filtered = filtered.filter(deal => deal.mileage <= parseInt(maxMileage));
            
            return filtered;
        }
        
        function sortDeals(deals, sortType) {
            switch(sortType) {
                case 'price-year':
                    return deals.sort((a, b) => (a.price - b.price) || (b.year - a.year));
                case 'price':
                    return deals.sort((a, b) => a.price - b.price);
                case 'year':
                    return deals.sort((a, b) => b.year - a.year);
                case 'value':
                    return deals.sort((a, b) => a.value_score - b.value_score);
                default:
                    return deals;
            }
        }
        
        function renderDeals() {
            const grid = document.getElementById('car-grid');
            let filtered = getFilteredDeals();
            filtered = sortDeals(filtered, currentSort);
            
            if (filtered.length === 0) {
                grid.innerHTML = '<div class="no-results">No cars found matching your criteria</div>';
                return;
            }
            
            grid.innerHTML = filtered.map((deal, index) => `
                <div class="car-card">
                    <div class="car-header">
                        <div class="car-title">${deal.title}</div>
                        <div class="car-year">${deal.year}</div>
                        <div class="car-badge">${deal.source}</div>
                    </div>
                    <div class="car-body">
                        <div class="car-price">$${deal.price.toLocaleString()}</div>
                        <div class="value-score">Value Score: $${deal.value_score.toLocaleString()}</div>
                        <div class="car-details">
                            <div class="detail-item">
                                <span class="detail-label">Mileage:</span>
                                <span>${deal.mileage.toLocaleString()} mi</span>
                            </div>
                            <div class="detail-item">
                                <span class="detail-label">Age:</span>
                                <span>${new Date().getFullYear() - deal.year} years</span>
                            </div>
                        </div>
                        <a href="${deal.url}" target="_blank" class="car-link">View Listing →</a>
                    </div>
                </div>
            `).join('');
        }
        
        // Event listeners
        document.getElementById('min-year').addEventListener('change', () => {
            updateStats();
            renderDeals();
        });
        
        document.getElementById('max-year').addEventListener('change', () => {
            updateStats();
            renderDeals();
        });
        
        document.getElementById('max-price').addEventListener('input', () => {
            updateStats();
            renderDeals();
        });
        
        document.getElementById('max-mileage').addEventListener('input', () => {
            updateStats();
            renderDeals();
        });
        
        document.querySelectorAll('.sort-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                document.querySelectorAll('.sort-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
                currentSort = e.target.dataset.sort;
                renderDeals();
            });
        });
    </script>
</body>
</html>
"""

# Initialize the deal finder
finder = BMWX3DealFinder()

@app.route('/')
def index():
    """Main page with car listings"""
    return HTML_TEMPLATE

@app.route('/api/deals')
def api_deals():
    """API endpoint to get all deals"""
    deals = finder.get_deals()
    return jsonify({
        'deals': deals,
        'total': len(deals),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/stats')
def api_stats():
    """API endpoint to get statistics"""
    deals = finder.get_deals()
    prices = [deal['price'] for deal in deals]
    years = [deal['year'] for deal in deals]
    
    return jsonify({
        'total_deals': len(deals),
        'price_range': {
            'min': min(prices) if prices else 0,
            'max': max(prices) if prices else 0
        },
        'year_range': {
            'min': min(years) if years else 0,
            'max': max(years) if years else 0
        },
        'average_price': sum(prices) / len(prices) if prices else 0,
        'average_year': sum(years) / len(years) if years else 0
    })

if __name__ == '__main__':
    print("🚗 BMW X3 Used Car Deal Finder - Web Version")
    print("=" * 50)
    print("Starting web server...")
    print("Open your browser and go to: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
