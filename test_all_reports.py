#!/usr/bin/env python3
"""
Test script to verify all Zoho Books report implementations
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from zoho_books_mcp_server.src.zoho.api.reports import (
    fetch_profit_and_loss,
    fetch_balance_sheet,
    fetch_cash_flow,
    fetch_sales_by_customer,
    fetch_sales_by_item,
    fetch_ar_aging_summary,
    fetch_ap_aging_summary,
    fetch_expenses_by_category,
    fetch_expense_details,
    fetch_invoice_details,
    fetch_payments_made,
    fetch_payments_received
)

def test_report(report_name, fetch_function, **kwargs):
    """Test a single report"""
    print(f"\n{'='*60}")
    print(f"Testing {report_name}")
    print('='*60)
    
    try:
        result = fetch_function(**kwargs)
        if result:
            print(f"✓ {report_name} - SUCCESS")
            print(f"  - Metadata: {result.get('report_metadata', {}).get('report_type', 'N/A')}")
            if 'summary' in result:
                summary = result['summary']
                for key, value in list(summary.items())[:3]:  # Show first 3 summary items
                    print(f"  - {key}: {value}")
        else:
            print(f"✗ {report_name} - FAILED (No data returned)")
    except Exception as e:
        print(f"✗ {report_name} - ERROR: {str(e)}")

def main():
    """Test all reports"""
    print("Testing all Zoho Books report implementations")
    
    # Define test parameters
    fiscal_year_start = "2024-04-01"
    fiscal_year_end = "2025-03-31"
    
    # Test financial reports
    test_report("Profit and Loss", fetch_profit_and_loss, 
                from_date=fiscal_year_start, to_date=fiscal_year_end)
    
    test_report("Balance Sheet", fetch_balance_sheet,
                as_of_date=fiscal_year_end)
    
    test_report("Cash Flow", fetch_cash_flow,
                from_date=fiscal_year_start, to_date=fiscal_year_end)
    
    # Test sales reports
    test_report("Sales by Customer", fetch_sales_by_customer,
                from_date=fiscal_year_start, to_date=fiscal_year_end)
    
    test_report("Sales by Item", fetch_sales_by_item,
                from_date=fiscal_year_start, to_date=fiscal_year_end)
    
    # Test aging reports
    test_report("AR Aging Summary", fetch_ar_aging_summary)
    
    test_report("AP Aging Summary", fetch_ap_aging_summary)
    
    # Test expense reports
    test_report("Expenses by Category", fetch_expenses_by_category,
                from_date=fiscal_year_start, to_date=fiscal_year_end)
    
    test_report("Expense Details", fetch_expense_details,
                from_date=fiscal_year_start, to_date=fiscal_year_end)
    
    # Test invoice report
    test_report("Invoice Details", fetch_invoice_details,
                from_date=fiscal_year_start, to_date=fiscal_year_end)
    
    # Test payment reports
    test_report("Payments Made", fetch_payments_made,
                from_date=fiscal_year_start, to_date=fiscal_year_end)
    
    test_report("Payments Received", fetch_payments_received,
                from_date=fiscal_year_start, to_date=fiscal_year_end)
    
    print(f"\n{'='*60}")
    print("Test completed!")
    print('='*60)

if __name__ == "__main__":
    main()