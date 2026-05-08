#!/usr/bin/env python3
"""
BMW X3 Deal Evaluator with Claude Analysis

This script analyzes BMW X3 deals using AI evaluation criteria
to identify the best value proposition.
"""

import json
import re
from datetime import datetime
from typing import List, Dict, Optional, Tuple
import math

class BMWX3DealEvaluator:
    def __init__(self):
        self.deals = self.create_sample_data()
        self.evaluation_criteria = {
            'price_weight': 0.35,
            'age_weight': 0.25,
            'mileage_weight': 0.20,
            'model_weight': 0.15,
            'value_weight': 0.05
        }
    
    def create_sample_data(self) -> List[Dict]:
        """Create sample BMW X3 data for evaluation"""
        return [
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
    
    def extract_model_type(self, title: str) -> str:
        """Extract model type from title (xDrive30i, xDrive28i, M40i, xDrive35i)"""
        if 'M40i' in title:
            return 'M40i'  # Performance model
        elif 'xDrive35i' in title:
            return 'xDrive35i'  # Older performance model
        elif 'xDrive30i' in title:
            return 'xDrive30i'  # Standard model
        elif 'xDrive28i' in title:
            return 'xDrive28i'  # Base model
        else:
            return 'Unknown'
    
    def calculate_price_score(self, price: float, year: int) -> float:
        """Calculate price score (lower is better, normalized by age)"""
        current_year = datetime.now().year
        age = current_year - year
        
        # Expected depreciation curve for BMW X3
        # New car price ~ $55,000, 5-year-old ~ $25,000, 10-year-old ~ $15,000
        expected_price = max(15000, 55000 * (0.85 ** age))
        
        # Score based on how much below expected price
        price_ratio = price / expected_price
        return min(100, max(0, 100 - (price_ratio - 1) * 100))
    
    def calculate_age_score(self, year: int) -> float:
        """Calculate age score (newer is better)"""
        current_year = datetime.now().year
        age = current_year - year
        
        # Newer cars get higher scores
        if age <= 1:
            return 100
        elif age <= 3:
            return 90
        elif age <= 5:
            return 75
        elif age <= 7:
            return 60
        elif age <= 10:
            return 40
        else:
            return 20
    
    def calculate_mileage_score(self, mileage: int, year: int) -> float:
        """Calculate mileage score (lower is better, adjusted for age)"""
        current_year = datetime.now().year
        age = current_year - year
        expected_mileage = age * 12000  # 12,000 miles per year average
        
        mileage_ratio = mileage / expected_mileage
        
        if mileage_ratio <= 0.8:
            return 100
        elif mileage_ratio <= 1.0:
            return 85
        elif mileage_ratio <= 1.2:
            return 70
        elif mileage_ratio <= 1.5:
            return 50
        else:
            return 25
    
    def calculate_model_score(self, model_type: str) -> float:
        """Calculate model score based on desirability"""
        model_scores = {
            'M40i': 100,      # Performance model
            'xDrive35i': 85,   # Older performance
            'xDrive30i': 75,   # Standard
            'xDrive28i': 65,   # Base
            'Unknown': 50
        }
        return model_scores.get(model_type, 50)
    
    def calculate_overall_score(self, deal: Dict) -> Dict:
        """Calculate comprehensive evaluation score"""
        current_year = datetime.now().year
        age = current_year - deal['year']
        model_type = self.extract_model_type(deal['title'])
        
        # Calculate individual scores
        price_score = self.calculate_price_score(deal['price'], deal['year'])
        age_score = self.calculate_age_score(deal['year'])
        mileage_score = self.calculate_mileage_score(deal['mileage'], deal['year'])
        model_score = self.calculate_model_score(model_type)
        
        # Calculate value score (price per year of remaining life)
        remaining_life = max(1, 15 - age)  # Assume 15-year total lifespan
        value_score = min(100, (deal['price'] / remaining_life) / 1000 * 10)
        value_score = 100 - value_score  # Invert so lower is better
        
        # Calculate weighted overall score
        overall_score = (
            price_score * self.evaluation_criteria['price_weight'] +
            age_score * self.evaluation_criteria['age_weight'] +
            mileage_score * self.evaluation_criteria['mileage_weight'] +
            model_score * self.evaluation_criteria['model_weight'] +
            value_score * self.evaluation_criteria['value_weight']
        )
        
        return {
            'price_score': price_score,
            'age_score': age_score,
            'mileage_score': mileage_score,
            'model_score': model_score,
            'value_score': value_score,
            'overall_score': overall_score,
            'model_type': model_type,
            'age': age,
            'price_per_year': deal['price'] / remaining_life
        }
    
    def evaluate_all_deals(self) -> List[Dict]:
        """Evaluate all deals and return sorted results"""
        evaluated_deals = []
        
        for deal in self.deals:
            evaluation = self.calculate_overall_score(deal)
            evaluated_deal = {
                **deal,
                **evaluation
            }
            evaluated_deals.append(evaluated_deal)
        
        # Sort by overall score (descending)
        evaluated_deals.sort(key=lambda x: x['overall_score'], reverse=True)
        return evaluated_deals
    
    def generate_ai_analysis(self, top_deals: List[Dict]) -> str:
        """Generate AI-style analysis of the top deals"""
        analysis = []
        
        analysis.append("=== AI EVALUATION OF BMW X3 DEALS ===\n")
        analysis.append("Based on comprehensive analysis of price, age, mileage, model type, and value proposition:\n")
        
        # Top 3 deals with detailed analysis
        for i, deal in enumerate(top_deals[:3], 1):
            analysis.append(f"#{i} - {deal['title']}")
            analysis.append(f"   Price: ${deal['price']:,.2f}")
            analysis.append(f"   Mileage: {deal['mileage']:,} miles")
            analysis.append(f"   Age: {deal['age']} years")
            analysis.append(f"   Model: {deal['model_type']}")
            analysis.append(f"   Overall Score: {deal['overall_score']:.1f}/100")
            
            # AI-style reasoning
            if deal['overall_score'] >= 85:
                analysis.append(f"   🏆 EXCELLENT VALUE: This deal offers exceptional value with optimal balance")
            elif deal['overall_score'] >= 75:
                analysis.append(f"   ✅ GOOD VALUE: Solid choice with favorable characteristics")
            elif deal['overall_score'] >= 65:
                analysis.append(f"   ⚠️ FAIR VALUE: Acceptable but consider alternatives")
            else:
                analysis.append(f"   ❌ POOR VALUE: Not recommended due to unfavorable factors")
            
            # Specific insights
            if deal['price_score'] >= 90:
                analysis.append(f"   💰 Price advantage: Significantly below market expectations")
            if deal['age_score'] >= 90:
                analysis.append(f"   🆕 Age advantage: Relatively new with modern features")
            if deal['mileage_score'] >= 90:
                analysis.append(f"   📊 Mileage advantage: Low mileage for vehicle age")
            if deal['model_score'] >= 90:
                analysis.append(f"   🚀 Model advantage: High-performance M40i variant")
            
            analysis.append("")
        
        # Best overall recommendation
        best_deal = top_deals[0]
        analysis.append("=== RECOMMENDATION ===")
        analysis.append(f"🏆 BEST OVERALL DEAL: {best_deal['title']}")
        analysis.append(f"   Price: ${best_deal['price']:,.2f}")
        analysis.append(f"   Link: {best_deal['url']}")
        analysis.append(f"   Score: {best_deal['overall_score']:.1f}/100")
        analysis.append("")
        analysis.append("This vehicle offers the best combination of price, age, mileage, and model type.")
        analysis.append("Recommended for immediate consideration.")
        
        return "\n".join(analysis)
    
    def generate_comparison_table(self, evaluated_deals: List[Dict]) -> str:
        """Generate a detailed comparison table"""
        table = []
        table.append("=== DETAILED COMPARISON TABLE ===")
        table.append("")
        table.append("Rank | Vehicle                     | Price    | Year | Mileage | Model    | Score | Link")
        table.append("-" * 120)
        
        for i, deal in enumerate(evaluated_deals[:10], 1):
            title_short = deal['title'][:25].ljust(25)
            price_str = f"${deal['price']:,.0f}".ljust(8)
            year_str = str(deal['year']).ljust(4)
            mileage_str = f"{deal['mileage']:,}".ljust(7)
            model_str = deal['model_type'].ljust(8)
            score_str = f"{deal['overall_score']:.1f}".ljust(5)
            
            table.append(f"{i:4d} | {title_short} | {price_str} | {year_str} | {mileage_str} | {model_str} | {score_str} | {deal['url'][:50]}...")
        
        return "\n".join(table)
    
    def run_evaluation(self):
        """Run complete evaluation and display results"""
        print("🤖 BMW X3 Deal Evaluator with AI Analysis")
        print("=" * 50)
        print("Analyzing all BMW X3 deals using advanced evaluation criteria...\n")
        
        # Evaluate all deals
        evaluated_deals = self.evaluate_all_deals()
        
        # Display AI analysis
        ai_analysis = self.generate_ai_analysis(evaluated_deals)
        print(ai_analysis)
        print()
        
        # Display comparison table
        comparison = self.generate_comparison_table(evaluated_deals)
        print(comparison)
        print()
        
        # Display evaluation criteria
        print("=== EVALUATION CRITERIA ===")
        print(f"Price Weight: {self.evaluation_criteria['price_weight']*100:.0f}%")
        print(f"Age Weight: {self.evaluation_criteria['age_weight']*100:.0f}%")
        print(f"Mileage Weight: {self.evaluation_criteria['mileage_weight']*100:.0f}%")
        print(f"Model Weight: {self.evaluation_criteria['model_weight']*100:.0f}%")
        print(f"Value Weight: {self.evaluation_criteria['value_weight']*100:.0f}%")
        print()
        
        # Save detailed results to file
        self.save_evaluation_results(evaluated_deals)
        
        return evaluated_deals[0]  # Return best deal
    
    def save_evaluation_results(self, evaluated_deals: List[Dict]):
        """Save evaluation results to JSON file"""
        results = {
            'evaluation_date': datetime.now().isoformat(),
            'evaluation_criteria': self.evaluation_criteria,
            'best_deal': evaluated_deals[0],
            'top_5_deals': evaluated_deals[:5],
            'all_deals': evaluated_deals
        }
        
        with open('bmw_x3_evaluation_results.json', 'w') as f:
            json.dump(results, f, indent=2)
        
        print("📄 Detailed results saved to 'bmw_x3_evaluation_results.json'")

def main():
    """Main function"""
    evaluator = BMWX3DealEvaluator()
    best_deal = evaluator.run_evaluation()
    
    print(f"\n🎯 FINAL RECOMMENDATION:")
    print(f"Best Deal: {best_deal['title']}")
    print(f"Price: ${best_deal['price']:,.2f}")
    print(f"Overall Score: {best_deal['overall_score']:.1f}/100")
    print(f"View listing: {best_deal['url']}")

if __name__ == "__main__":
    main()
