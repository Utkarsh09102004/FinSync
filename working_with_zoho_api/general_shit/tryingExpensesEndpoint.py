import os
import requests
import json
from dotenv import load_dotenv
import sys
import os.path

# Add parent directory to path to import get_access_token
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from auth.get_access_token import get_valid_access_token

def fetch_expenses():
    # Load environment variables
    load_dotenv()
    
    # Get organization ID from environment variables
    organization_id = os.getenv("ZOHO_ORGANIZATION_ID")
    if not organization_id:
        print("Error: ZOHO_ORGANIZATION_ID not found in environment variables")
        return
    
    # Get valid access token
    access_token = get_valid_access_token()
    print(access_token)
    if not access_token:
        print("Error: Failed to obtain a valid access token")
        return
    
    
    
    # Prepare request headers
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}"
    }
    
    # Define API endpoint
    # url = f"https://www.zohoapis.in/books/v3/expenses"

    # url = f"https://www.zohoapis.in/books/v3/reports/trialbalance"
    
    url = "https://www.zohoapis.in/books/v3/reports/profitandloss?cash_based=false&filter_by=TransactionDate.CustomDate&from_date=2024-11-01&to_date=2026-02-24&select_columns=%5B%7B%22field%22%3A%22name%22%2C%22group%22%3A%22report%22%7D%2C%7B%22field%22%3A%22total%22%2C%22group%22%3A%22report%22%7D%5D&show_rows=non_zero&sort_column=total&sort_order=A&usestate=true&is_response_new_flow=true&is_new_flow=true&is_ytd_compare_column=false&response_option=1"

    params = {
        "organization_id": organization_id
    }
    
    try:    
        # Make the API request
        response = requests.get(url, headers=headers, params=params)
        
        # Check response status
        if response.status_code == 200:
            expenses_data = response.json()
            print("Successfully fetched expenses:")
            print(json.dumps(expenses_data, indent=5))
            
            # Save response to file
            with open("generated_shit/p&l_response.json", "w") as f:
                json.dump(expenses_data, f, indent=2)
                print("Response saved to p&l_response.json")
        else:
            print(f"API request failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
    
    except Exception as e:
        print(f"Error fetching expenses: {str(e)}")

if __name__ == "__main__":
    fetch_expenses()
