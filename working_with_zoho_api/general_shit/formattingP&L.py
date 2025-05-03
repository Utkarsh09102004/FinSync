import json

def extract_pnl_data(pnl_json_data):
    """
    Extracts relevant Profit and Loss information from the provided JSON structure.

    Args:
        pnl_json_data (dict): A dictionary containing the P&L report JSON data.

    Returns:
        dict: A dictionary structured for potential AI analysis, containing:
              - report_metadata: Context about the report (dates, basis).
              - summary: Key P&L figures (Gross Profit, Operating Profit, Net Profit).
              - income_details: Breakdown of Operating Income.
              - cogs_details: Breakdown of Cost of Goods Sold.
              - expense_details: Breakdown of Operating Expenses.
              - non_operating_details: Breakdown of Non-Operating Income/Expense.
              - raw_sections: The main sections with their totals for reference.
    """
    if pnl_json_data.get("code") != 0 or not pnl_json_data.get("profit_and_loss"):
        print("Error or no P&L data found in JSON.")
        return None

    pnl_sections = pnl_json_data["profit_and_loss"]
    page_context = pnl_json_data.get("page_context", {})

    extracted_data = {
        "report_metadata": {
            "report_type": page_context.get("report_type", "profit_and_loss"),
            "from_date": page_context.get("from_date"),
            "to_date": page_context.get("to_date"),
            "report_basis": page_context.get("report_basis", "Unknown"),
            "currency": "Implicit (assumed from values, not specified)" # Assuming USD or similar, add if available
        },
        "summary": {},
        "income_details": {
            "total_operating_income": 0.0,
            "accounts": []
        },
        "cogs_details": {
            "total_cogs": 0.0,
            "accounts": []
        },
        "expense_details": {
            "total_operating_expense": 0.0,
            "accounts": []
        },
        "non_operating_details": {
            "total_non_operating_income": 0.0,
            "income_accounts": [],
            "total_non_operating_expense": 0.0,
            "expense_accounts": []
        },
        "raw_sections": [] # Store raw section totals if needed
    }

    def process_account_transactions(transactions):
        """Helper function to extract individual account details."""
        accounts_list = []
        for acc in transactions:
            accounts_list.append({
                "account_name": acc.get("name"),
                "account_code": acc.get("account_code", ""), # Handle missing code
                "total": acc.get("total", 0.0),
                "account_id": acc.get("account_id") # Keep ID if useful later
            })
        return accounts_list

    # --- Main Processing Logic ---
    for section in pnl_sections:
        section_name = section.get("name")
        section_total = section.get("total", 0.0)

        # Store raw section totals
        extracted_data["raw_sections"].append({
            "section_name": section_name,
            "total": section_total
        })

        # Extract Summary Figures
        if section_name == "Gross Profit":
            extracted_data["summary"]["gross_profit"] = section_total
        elif section_name == "Operating Profit":
            extracted_data["summary"]["operating_profit"] = section_total
        elif section_name == "Net Profit/Loss":
            extracted_data["summary"]["net_profit_loss"] = section_total

        # Extract Detailed Breakdowns
        for category in section.get("account_transactions", []):
            category_name = category.get("name")
            category_total = category.get("total", 0.0)
            category_accounts = category.get("account_transactions", [])

            if category_name == "Operating Income":
                extracted_data["income_details"]["total_operating_income"] = category_total
                extracted_data["income_details"]["accounts"] = process_account_transactions(category_accounts)
            elif category_name == "Cost of Goods Sold":
                 extracted_data["cogs_details"]["total_cogs"] = category_total
                 extracted_data["cogs_details"]["accounts"] = process_account_transactions(category_accounts)
            elif category_name == "Operating Expense":
                 extracted_data["expense_details"]["total_operating_expense"] = category_total
                 extracted_data["expense_details"]["accounts"] = process_account_transactions(category_accounts)
            elif category_name == "Non Operating Income":
                 extracted_data["non_operating_details"]["total_non_operating_income"] = category_total
                 extracted_data["non_operating_details"]["income_accounts"] = process_account_transactions(category_accounts)
            elif category_name == "Non Operating Expense":
                 extracted_data["non_operating_details"]["total_non_operating_expense"] = category_total
                 extracted_data["non_operating_details"]["expense_accounts"] = process_account_transactions(category_accounts)

    # --- Data Validation/Consistency Check (Optional but Recommended) ---
    # Check if calculated totals match summary figures (within a small tolerance for float math)
    calculated_gross_profit = extracted_data["income_details"]["total_operating_income"] - extracted_data["cogs_details"]["total_cogs"]
    calculated_operating_profit = calculated_gross_profit - extracted_data["expense_details"]["total_operating_expense"]
    calculated_net_profit = (calculated_operating_profit +
                             extracted_data["non_operating_details"]["total_non_operating_income"] -
                             extracted_data["non_operating_details"]["total_non_operating_expense"])

    tolerance = 0.01 # Allow for tiny floating point differences

    if abs(calculated_gross_profit - extracted_data["summary"].get("gross_profit", 0.0)) > tolerance:
        print(f"Warning: Calculated Gross Profit ({calculated_gross_profit}) does not match summary ({extracted_data['summary'].get('gross_profit')})")
    if abs(calculated_operating_profit - extracted_data["summary"].get("operating_profit", 0.0)) > tolerance:
         print(f"Warning: Calculated Operating Profit ({calculated_operating_profit}) does not match summary ({extracted_data['summary'].get('operating_profit')})")
    if abs(calculated_net_profit - extracted_data["summary"].get("net_profit_loss", 0.0)) > tolerance:
         print(f"Warning: Calculated Net Profit/Loss ({calculated_net_profit}) does not match summary ({extracted_data['summary'].get('net_profit_loss')})")


    return extracted_data

# --- Load your JSON data here ---
# Assuming your JSON is in a file named 'pnl_data.json'
# with open('pnl_data.json', 'r') as f:
#     pnl_json = json.load(f)

# Or, if you have it as a string literal like in the prompt:
pnl_json_string = """
{
  "code": 0,
  "message": "success",
  "profit_and_loss": [
    {
      "total": 1272500.0,
      "previous_values": [],
      "account_transactions": [
        {
          "total": 1272500.0,
          "total_label": "Total Operating Income",
          "previous_values": [],
          "account_transactions": [
            {
              "total_sub_account": 0.0,
              "total": 446500.0,
              "account_id": "2538476000000000486",
              "depth": 0,
              "previous_values": [],
              "is_child_present": false,
              "name": "Sales",
              "previous_total_sub_account": [],
              "account_code": "",
              "is_collapsed_view": false,
              "previous_total": []
            },
            {
              "total_sub_account": 0.0,
              "total": 826000.0,
              "account_id": "2538476000000032099",
              "depth": 0,
              "previous_values": [],
              "is_child_present": false,
              "name": "Service Revenue",
              "previous_total_sub_account": [],
              "account_code": "4010",
              "is_collapsed_view": false,
              "previous_total": []
            }
          ],
          "name": "Operating Income",
          "previous_total": []
        },
        {
          "total": 0.0,
          "total_label": "Total Cost of Goods Sold",
          "previous_values": [],
          "account_transactions": [],
          "name": "Cost of Goods Sold",
          "previous_total": []
        }
      ],
      "name": "Gross Profit",
      "previous_total": []
    },
    {
      "total": -1274875.0,
      "previous_values": [],
      "account_transactions": [
        {
          "total": 2547375.0,
          "total_label": "Total Operating Expense",
          "previous_values": [],
          "account_transactions": [
            {
              "total_sub_account": 0.0,
              "total": 887300.0,
              "account_id": "2538476000000032103",
              "depth": 0,
              "previous_values": [],
              "is_child_present": false,
              "name": "Purchases",
              "previous_total_sub_account": [],
              "account_code": "5000",
              "is_collapsed_view": false,
              "previous_total": []
            },
            {
              "total_sub_account": 0.0,
              "total": 788000.0,
              "account_id": "2538476000000032109",
              "depth": 0,
              "previous_values": [],
              "is_child_present": false,
              "name": "Salaries Expense",
              "previous_total_sub_account": [],
              "account_code": "6010",
              "is_collapsed_view": false,
              "previous_total": []
            },
            {
              "total_sub_account": 0.0,
              "total": 406000.0,
              "account_id": "2538476000000000528",
              "depth": 0,
              "previous_values": [],
              "is_child_present": false,
              "name": "Rent Expense",
              "previous_total_sub_account": [],
              "account_code": "",
              "is_collapsed_view": false,
              "previous_total": []
            },
            {
              "total_sub_account": 0.0,
              "total": 186475.0,
              "account_id": "2538476000000032115",
              "depth": 0,
              "previous_values": [],
              "is_child_present": false,
              "name": "Office Supplies Expense",
              "previous_total_sub_account": [],
              "account_code": "6020",
              "is_collapsed_view": false,
              "previous_total": []
            },
            {
              "total_sub_account": 0.0,
              "total": 178000.0,
              "account_id": "2538476000000032133",
              "depth": 0,
              "previous_values": [],
              "is_child_present": false,
              "name": "Consulting Fees",
              "previous_total_sub_account": [],
              "account_code": "6100",
              "is_collapsed_view": false,
              "previous_total": []
            },
            {
              "total_sub_account": 0.0,
              "total": 61500.0,
              "account_id": "2538476000000032121",
              "depth": 0,
              "previous_values": [],
              "is_child_present": false,
              "name": "Utilities Expense",
              "previous_total_sub_account": [],
              "account_code": "6040",
              "is_collapsed_view": false,
              "previous_total": []
            },
            {
              "total_sub_account": 0.0,
              "total": 37600.0,
              "account_id": "2538476000000000516",
              "depth": 0,
              "previous_values": [],
              "is_child_present": false,
              "name": "Travel Expense",
              "previous_total_sub_account": [],
              "account_code": "",
              "is_collapsed_view": false,
              "previous_total": []
            },
            {
              "total_sub_account": 0.0,
              "total": 2500.0,
              "account_id": "2538476000000032127",
              "depth": 0,
              "previous_values": [],
              "is_child_present": false,
              "name": "Bank Charges",
              "previous_total_sub_account": [],
              "account_code": "6050",
              "is_collapsed_view": false,
              "previous_total": []
            }
          ],
          "name": "Operating Expense",
          "previous_total": []
        }
      ],
      "name": "Operating Profit",
      "previous_total": []
    },
    {
      "total": -1274875.0,
      "previous_values": [],
      "account_transactions": [
        {
          "total": 0.0,
          "total_label": "Total Non Operating Income",
          "previous_values": [],
          "account_transactions": [],
          "name": "Non Operating Income",
          "previous_total": []
        },
        {
          "total": 0.0,
          "total_label": "Total Non Operating Expense",
          "previous_values": [],
          "account_transactions": [],
          "name": "Non Operating Expense",
          "previous_total": []
        }
      ],
      "name": "Net Profit/Loss",
      "previous_total": []
    }
  ],
  "page_context": {
    "can_show_reports_banner": false,
    "can_schedule": true,
    "is_inv_txn_job_in_progress": false,
    "report_basis": "Accrual",
    "is_already_scheduled": false,
    "report_type": "profit_and_loss",
    "applied_filter": "TransactionDate.CustomDate",
    "from_date": "2024-04-01",
    "to_date": "2025-02-03",
    "previous_date_range": [],
    "cash_based": "false",
    "chart_type": [],
    "show_rows": "non_zero",
    "last_accessed_time_formatted": "18/04/2025 04:07 AM",
    "filter_by": "TransactionDate.CustomDate",
    "select_columns": [],
    "group_by": [],
    "date_range_label": "",
    "fifo_scheduler_status": {
      "is_queue_entry_present": false,
      "is_job_status_completed": true
    },
    "date_range_list": [
      {
        "date_range_label": "01 Apr 2024 - 03 Feb 2025",
        "from_date": "2024-04-01",
        "to_date": "2025-02-03"
      }
    ],
    "sort_column": "total",
    "sort_order": "A"
  }
}
"""

pnl_json = json.loads(pnl_json_string)

# --- Extract the data ---
extracted_pnl = extract_pnl_data(pnl_json)

# --- Print the result (nicely formatted) ---
if extracted_pnl:
    print(json.dumps(extracted_pnl, indent=2))

# --- How to potentially feed this to an AI ---
# You could convert the dictionary to a string or keep it as a structured input.
# Example prompt for an AI model:

"""
Analyze the following Profit and Loss data and provide key insights:

Report Metadata:
Start Date: {from_date}
End Date: {to_date}
Accounting Basis: {report_basis}

Summary Figures:
Gross Profit: {gross_profit}
Operating Profit: {operating_profit}
Net Profit/Loss: {net_profit_loss}

Income Breakdown (Total: {total_operating_income}):
{income_accounts_formatted}

Cost of Goods Sold Breakdown (Total: {total_cogs}):
{cogs_accounts_formatted}

Operating Expense Breakdown (Total: {total_operating_expense}):
{expense_accounts_formatted}

Non-Operating Income (Total: {total_non_operating_income}):
{non_op_income_accounts_formatted}

Non-Operating Expense (Total: {total_non_operating_expense}):
{non_op_expense_accounts_formatted}

Focus on major revenue drivers, significant expense categories, overall profitability trends (or lack thereof), and any potential areas of concern or strength based on this snapshot.
"""

# You would then format the lists of accounts into readable strings
# for the placeholders above before sending to the AI.
# For example:
def format_accounts_for_prompt(accounts_list):
    if not accounts_list:
        return "  - None"
    return "\n".join([f"  - {acc['account_name']} ({acc.get('account_code', 'N/A')}): {acc['total']}" for acc in accounts_list])

if extracted_pnl:
    prompt_data = {
        "from_date": extracted_pnl["report_metadata"]["from_date"],
        "to_date": extracted_pnl["report_metadata"]["to_date"],
        "report_basis": extracted_pnl["report_metadata"]["report_basis"],
        "gross_profit": extracted_pnl["summary"].get("gross_profit", "N/A"),
        "operating_profit": extracted_pnl["summary"].get("operating_profit", "N/A"),
        "net_profit_loss": extracted_pnl["summary"].get("net_profit_loss", "N/A"),
        "total_operating_income": extracted_pnl["income_details"]["total_operating_income"],
        "income_accounts_formatted": format_accounts_for_prompt(extracted_pnl["income_details"]["accounts"]),
        "total_cogs": extracted_pnl["cogs_details"]["total_cogs"],
        "cogs_accounts_formatted": format_accounts_for_prompt(extracted_pnl["cogs_details"]["accounts"]),
        "total_operating_expense": extracted_pnl["expense_details"]["total_operating_expense"],
        "expense_accounts_formatted": format_accounts_for_prompt(extracted_pnl["expense_details"]["accounts"]),
        "total_non_operating_income": extracted_pnl["non_operating_details"]["total_non_operating_income"],
        "non_op_income_accounts_formatted": format_accounts_for_prompt(extracted_pnl["non_operating_details"]["income_accounts"]),
        "total_non_operating_expense": extracted_pnl["non_operating_details"]["total_non_operating_expense"],
        "non_op_expense_accounts_formatted": format_accounts_for_prompt(extracted_pnl["non_operating_details"]["expense_accounts"]),
    }

    # Example of how you might format the prompt string
    ai_prompt = """
Analyze the following Profit and Loss data and provide key insights:

Report Metadata:
Start Date: {from_date}
End Date: {to_date}
Accounting Basis: {report_basis}

Summary Figures:
Gross Profit: {gross_profit}
Operating Profit: {operating_profit}
Net Profit/Loss: {net_profit_loss}

Income Breakdown (Total: {total_operating_income}):
{income_accounts_formatted}

Cost of Goods Sold Breakdown (Total: {total_cogs}):
{cogs_accounts_formatted}

Operating Expense Breakdown (Total: {total_operating_expense}):
{expense_accounts_formatted}

Non-Operating Income (Total: {total_non_operating_income}):
{non_op_income_accounts_formatted}

Non-Operating Expense (Total: {total_non_operating_expense}):
{non_op_expense_accounts_formatted}

Focus on major revenue drivers, significant expense categories, overall profitability (or loss) situation, and any potential areas of concern or strength based on this snapshot for the period {from_date} to {to_date}.
""".format(**prompt_data)

    # print("\n--- Example AI Prompt ---")
    # print(ai_prompt) # You would send this prompt to your AI model