from google.adk.tools import ToolContext
from typing import Dict, List, Optional, Union
from datetime import datetime, timedelta
import json


def calculate_cash_burn(
    financial_data: str,
    period: str,
    tool_context: ToolContext
) -> dict:
    """
    Calculates the net cash used by operating activities (cash burn rate).
    
    This tool analyzes cash flow data to determine how much cash the business
    is consuming during operations. A positive value indicates cash burn,
    while a negative value indicates cash generation.
    
    Args:
        financial_data (str): JSON string containing cash flow statement data
                             with operating, investing, and financing activities
        period (str): The time period for the calculation (e.g., "monthly", "quarterly")
    
    Returns:
        dict: A dictionary containing:
              - 'status': 'success' or 'error'
              - 'cash_burn': Net cash used (positive = burn, negative = generation)
              - 'breakdown': Detailed breakdown by activity type
              - 'period': The period analyzed
              - 'analysis': Text analysis of the cash burn
    
    Example:
        User asks: "What was my cash burn last month?"
        The tool receives cash flow data and calculates the net operating cash flow.
    """
    try:
        # Parse the financial data
        data = json.loads(financial_data)
        
        # Extract operating activities
        operating_activities = data.get('operating_activities', {})
        
        # Calculate total cash from operations
        cash_from_operations = 0
        breakdown = {}
        
        # Common operating cash flow items
        operating_items = {
            'net_income': operating_activities.get('net_income', 0),
            'depreciation': operating_activities.get('depreciation', 0),
            'accounts_receivable_change': -operating_activities.get('accounts_receivable_change', 0),
            'inventory_change': -operating_activities.get('inventory_change', 0),
            'accounts_payable_change': operating_activities.get('accounts_payable_change', 0),
            'other_operating': operating_activities.get('other_operating', 0)
        }
        
        for item, amount in operating_items.items():
            cash_from_operations += amount
            breakdown[item] = amount
        
        # Cash burn is negative of cash from operations
        # Positive = burning cash, Negative = generating cash
        cash_burn = -cash_from_operations
        
        # Generate analysis text
        if cash_burn > 0:
            analysis = f"The company burned ${cash_burn:,.2f} in cash during the {period}. "
            analysis += "This indicates the business is consuming cash in operations."
        else:
            analysis = f"The company generated ${-cash_burn:,.2f} in cash during the {period}. "
            analysis += "This indicates positive cash flow from operations."
        
        # Store result in context for potential future use
        tool_context.state['last_cash_burn_calculation'] = {
            'period': period,
            'cash_burn': cash_burn,
            'timestamp': datetime.now().isoformat()
        }
        
        return {
            'status': 'success',
            'cash_burn': cash_burn,
            'breakdown': breakdown,
            'period': period,
            'analysis': analysis
        }
        
    except json.JSONDecodeError:
        return {
            'status': 'error',
            'error_message': 'Invalid financial data format. Expected JSON string.'
        }
    except Exception as e:
        return {
            'status': 'error',
            'error_message': f'Error calculating cash burn: {str(e)}'
        }


def calculate_profit_margins(
    financial_data: str,
    period: str,
    tool_context: ToolContext
) -> dict:
    """
    Calculates Gross and Net Profit Margins from income statement data.
    
    This tool computes key profitability metrics that indicate how efficiently
    the business converts revenue into profits at different levels.
    
    Args:
        financial_data (str): JSON string containing income statement data
                             including revenue, COGS, and expenses
        period (str): The time period for the calculation (e.g., "Q1 2024", "March 2024")
    
    Returns:
        dict: A dictionary containing:
              - 'status': 'success' or 'error'
              - 'gross_margin': Gross profit margin percentage
              - 'net_margin': Net profit margin percentage
              - 'gross_profit': Absolute gross profit amount
              - 'net_profit': Absolute net profit amount
              - 'revenue': Total revenue for the period
              - 'analysis': Text analysis of the margins
              - 'period': The period analyzed
    
    Example:
        User asks: "What was our net margin in Q2?"
        The tool receives income statement data and calculates both margins.
    """
    try:
        # Parse the financial data
        data = json.loads(financial_data)
        
        # Extract key financial metrics
        revenue = data.get('revenue', 0)
        cogs = data.get('cost_of_goods_sold', 0)
        operating_expenses = data.get('operating_expenses', 0)
        other_expenses = data.get('other_expenses', 0)
        taxes = data.get('taxes', 0)
        
        # Validate revenue
        if revenue <= 0:
            return {
                'status': 'error',
                'error_message': 'Revenue must be greater than zero to calculate margins.'
            }
        
        # Calculate gross profit and margin
        gross_profit = revenue - cogs
        gross_margin = (gross_profit / revenue) * 100
        
        # Calculate net profit and margin
        total_expenses = cogs + operating_expenses + other_expenses + taxes
        net_profit = revenue - total_expenses
        net_margin = (net_profit / revenue) * 100
        
        # Generate analysis
        analysis = f"For {period}:\n"
        analysis += f"- Gross Margin: {gross_margin:.1f}% "
        
        if gross_margin > 50:
            analysis += "(Excellent - strong pricing power)\n"
        elif gross_margin > 30:
            analysis += "(Good - healthy markup over costs)\n"
        elif gross_margin > 20:
            analysis += "(Moderate - room for improvement)\n"
        else:
            analysis += "(Low - consider pricing or cost strategies)\n"
            
        analysis += f"- Net Margin: {net_margin:.1f}% "
        
        if net_margin > 20:
            analysis += "(Excellent profitability)\n"
        elif net_margin > 10:
            analysis += "(Good profitability)\n"
        elif net_margin > 5:
            analysis += "(Moderate profitability)\n"
        elif net_margin > 0:
            analysis += "(Low but positive profitability)\n"
        else:
            analysis += "(Loss - operational improvements needed)\n"
        
        # Compare margins
        if gross_margin - net_margin > 40:
            analysis += "\nHigh operating expenses are significantly impacting profitability."
        
        # Store result in context
        tool_context.state['last_margin_calculation'] = {
            'period': period,
            'gross_margin': gross_margin,
            'net_margin': net_margin,
            'timestamp': datetime.now().isoformat()
        }
        
        return {
            'status': 'success',
            'gross_margin': round(gross_margin, 2),
            'net_margin': round(net_margin, 2),
            'gross_profit': gross_profit,
            'net_profit': net_profit,
            'revenue': revenue,
            'analysis': analysis,
            'period': period
        }
        
    except json.JSONDecodeError:
        return {
            'status': 'error',
            'error_message': 'Invalid financial data format. Expected JSON string.'
        }
    except Exception as e:
        return {
            'status': 'error',
            'error_message': f'Error calculating profit margins: {str(e)}'
        }