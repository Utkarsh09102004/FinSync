# cash flow statement
https://www.zohoapis.in/books/api/v3/reports/cashflow?filter_by=TransactionDate.ThisMonth&select_columns=%5B%7B%22field%22%3A%22name%22%2C%22group%22%3A%22report%22%7D%2C%7B%22field%22%3A%22account_code%22%2C%22group%22%3A%22report%22%7D%2C%7B%22field%22%3A%22total%22%2C%22group%22%3A%22report%22%7D%5D&sort_column=name&sort_order=A&usestate=true&is_response_new_flow=true&is_new_flow=true&is_ytd_compare_column=false&response_option=1&organization_id=60040042565


# sales by customer
https://www.zohoapis.in/books/api/v3/reports/salesbycustomer?page=1&per_page=200&sort_order=A&sort_column=customer_name&filter_by=TransactionDate.PreviousYear&entity_list=invoice%2Ccreditnote&select_columns=%5B%7B%22field%22%3A%22customer_name%22%2C%22group%22%3A%22report%22%7D%2C%7B%22field%22%3A%22count%22%2C%22group%22%3A%22report%22%7D%2C%7B%22field%22%3A%22sales%22%2C%22group%22%3A%22report%22%7D%2C%7B%22field%22%3A%22sales_with_tax%22%2C%22group%22%3A%22report%22%7D%5D&usestate=true&is_new_flow=true&response_option=1&organization_id=60040042565
Request Method
GET

# sales by item
https://www.zohoapis.in/books/api/v3/reports/salesbyitem?page=1&per_page=200&sort_order=A&sort_column=item_name&filter_by=TransactionDate.PreviousYear&select_columns=%5B%7B%22field%22%3A%22item_name%22%2C%22group%22%3A%22report%22%7D%2C%7B%22field%22%3A%22quantity_sold%22%2C%22group%22%3A%22report%22%7D%2C%7B%22field%22%3A%22amount%22%2C%22group%22%3A%22report%22%7D%2C%7B%22field%22%3A%22average_price%22%2C%22group%22%3A%22report%22%7D%5D&group_by=%5B%7B%22field%22%3A%22none%22%2C%22group%22%3A%22report%22%7D%5D&usestate=true&entity_list=invoice%2Ccreditnote&response_option=1&organization_id=60040042565
Request Method
GET


# ar aging summary
https://www.zohoapis.in/books/api/v3/reports/aragingsummary?page=1&per_page=500&sort_order=A&sort_column=customer_name&show_by=overdueamount&group_by=none&interval_type=days&number_of_columns=4&interval_range=15&select_columns=%5B%7B%22field%22%3A%22customer_name%22%2C%22group%22%3A%22report%22%7D%2C%7B%22field%22%3A%22current%22%2C%22group%22%3A%22report%22%7D%2C%7B%22field%22%3A%22intervals%22%2C%22group%22%3A%22report%22%7D%2C%7B%22field%22%3A%22total%22%2C%22group%22%3A%22report%22%7D%2C%7B%22field%22%3A%22fcy_total%22%2C%22group%22%3A%22report%22%7D%5D&filter_by=InvoiceDueDate.Today&entity_list=invoice&is_new_flow=true&rule=%7B%22columns%22%3A%5B%7B%22index%22%3A1%2C%22field%22%3A%22customer_id%22%2C%22value%22%3A%5B%222538476000000032433%22%5D%2C%22comparator%22%3A%22in%22%2C%22group%22%3A%22report%22%7D%5D%2C%22criteria_string%22%3A%221%22%7D&usestate=true&is_new_group_by=true&response_option=1&organization_id=60040042565
Request Method
GET

# ap aging summary

https://www.zohoapis.in/books/api/v3/reports/apagingsummary?page=1&per_page=500&sort_order=A&sort_column=vendor_name&aging_by=billduedate&show_by=overdueamount&group_by=vendor&include_vendor_credit_notes=false&interval_type=days&number_of_columns=4&interval_range=15&select_columns=%5B%7B%22field%22%3A%22vendor_name%22%2C%22group%22%3A%22report%22%7D%2C%7B%22field%22%3A%22current%22%2C%22group%22%3A%22report%22%7D%2C%7B%22field%22%3A%22intervals%22%2C%22group%22%3A%22report%22%7D%2C%7B%22field%22%3A%22total%22%2C%22group%22%3A%22report%22%7D%2C%7B%22field%22%3A%22fcy_total%22%2C%22group%22%3A%22report%22%7D%5D&to_date=2025-03-31&include_manual_journals=false&response_option=1&organization_id=60040042565
Request Method
GET


# expenses by category

https://www.zohoapis.in/books/api/v3/reports/expensesbycategory?page=1&per_page=500&sort_column=account_name&sort_order=A&filter_by=ExpenseDate.PreviousYear&transaction_type=All&account_type=expense&response_option=1&organization_id=60040042565
Request Method
GET


# expense details


https://www.zohoapis.in/books/api/v3/reports/expensedetails?page=1&per_page=500&sort_column=date&sort_order=A&filter_by=ExpenseDate.PreviousQuarter&select_columns=%5B%7B%22field%22%3A%22status%22%2C%22group%22%3A%22report%22%7D%2C%7B%22field%22%3A%22date%22%2C%22group%22%3A%22report%22%7D%2C%7B%22field%22%3A%22transaction_type%22%2C%22group%22%3A%22report%22%7D%2C%7B%22field%22%3A%22transaction_number%22%2C%22group%22%3A%22report%22%7D%2C%7B%22field%22%3A%22vendor_name%22%2C%22group%22%3A%22report%22%7D%2C%7B%22field%22%3A%22account_name%22%2C%22group%22%3A%22report%22%7D%2C%7B%22field%22%3A%22customer_name%22%2C%22group%22%3A%22report%22%7D%2C%7B%22field%22%3A%22amount%22%2C%22group%22%3A%22report%22%7D%2C%7B%22field%22%3A%22amount_with_tax%22%2C%22group%22%3A%22report%22%7D%5D&group_by=%5B%7B%22field%22%3A%22none%22%2C%22group%22%3A%22report%22%7D%5D&entity_list=expense&response_option=1&organization_id=60040042565
GET

# invoice details

https://www.zohoapis.in/books/api/v3/reports/invoicedetails?page=1&per_page=200&sort_column=date&sort_order=A&filter_by=InvoiceDate.PreviousYear&select_columns=%5B%7B%22field%22%3A%22status%22%2C%22group%22%3A%22invoice%22%7D%2C%7B%22field%22%3A%22date%22%2C%22group%22%3A%22invoice%22%7D%2C%7B%22field%22%3A%22due_date%22%2C%22group%22%3A%22invoice%22%7D%2C%7B%22field%22%3A%22invoice_number%22%2C%22group%22%3A%22invoice%22%7D%2C%7B%22field%22%3A%22reference_number%22%2C%22group%22%3A%22invoice%22%7D%2C%7B%22field%22%3A%22customer_name%22%2C%22group%22%3A%22invoice%22%7D%2C%7B%22field%22%3A%22bcy_total%22%2C%22group%22%3A%22invoice%22%7D%2C%7B%22field%22%3A%22bcy_balance%22%2C%22group%22%3A%22invoice%22%7D%5D&group_by=%5B%7B%22field%22%3A%22none%22%2C%22group%22%3A%22report%22%7D%5D&usestate=true&response_option=1&organization_id=60040042565
Request Method
GET


# payments made

https://www.zohoapis.in/books/api/v3/reports/vendorpayments?page=1&per_page=500&sort_column=date&sort_order=A&filter_by=PaymentDate.PreviousYear&select_columns=%5B%7B%22field%22%3A%22date%22%2C%22group%22%3A%22vendor_payment%22%7D%2C%7B%22field%22%3A%22reference_number%22%2C%22group%22%3A%22vendor_payment%22%7D%2C%7B%22field%22%3A%22bill_numbers%22%2C%22group%22%3A%22vendor_payment%22%7D%2C%7B%22field%22%3A%22vendor_name%22%2C%22group%22%3A%22vendor_payment%22%7D%2C%7B%22field%22%3A%22payment_mode%22%2C%22group%22%3A%22vendor_payment%22%7D%2C%7B%22field%22%3A%22description%22%2C%22group%22%3A%22vendor_payment%22%7D%2C%7B%22field%22%3A%22paid_through_account_name%22%2C%22group%22%3A%22vendor_payment%22%7D%2C%7B%22field%22%3A%22paymentstatus%22%2C%22group%22%3A%22vendor_payment%22%7D%2C%7B%22field%22%3A%22bcy_amount%22%2C%22group%22%3A%22vendor_payment%22%7D%2C%7B%22field%22%3A%22amount%22%2C%22group%22%3A%22vendor_payment%22%7D%2C%7B%22field%22%3A%22bcy_unused_amount%22%2C%22group%22%3A%22vendor_payment%22%7D%2C%7B%22field%22%3A%22unused_amount%22%2C%22group%22%3A%22vendor_payment%22%7D%5D&usestate=true&group_by=%5B%7B%22field%22%3A%22none%22%2C%22group%22%3A%22report%22%7D%5D&response_option=1&organization_id=60040042565
Request Method
GET



# payments received 
https://www.zohoapis.in/books/api/v3/reports/customerpayments?page=1&per_page=500&sort_column=date&sort_order=D&filter_by=PaymentDate.PreviousYear%2CPaymentType.All&select_columns=%5B%7B%22field%22%3A%22payment_number%22%2C%22group%22%3A%22customer_payment%22%7D%2C%7B%22field%22%3A%22date%22%2C%22group%22%3A%22customer_payment%22%7D%2C%7B%22field%22%3A%22reference_number%22%2C%22group%22%3A%22customer_payment%22%7D%2C%7B%22field%22%3A%22customer_name%22%2C%22group%22%3A%22customer_payment%22%7D%2C%7B%22field%22%3A%22payment_mode%22%2C%22group%22%3A%22customer_payment%22%7D%2C%7B%22field%22%3A%22description%22%2C%22group%22%3A%22customer_payment%22%7D%2C%7B%22field%22%3A%22invoice_number%22%2C%22group%22%3A%22customer_payment%22%7D%2C%7B%22field%22%3A%22account_name%22%2C%22group%22%3A%22customer_payment%22%7D%2C%7B%22field%22%3A%22amount%22%2C%22group%22%3A%22customer_payment%22%7D%2C%7B%22field%22%3A%22unused_amount%22%2C%22group%22%3A%22customer_payment%22%7D%2C%7B%22field%22%3A%22bcy_amount%22%2C%22group%22%3A%22customer_payment%22%7D%2C%7B%22field%22%3A%22bcy_unused_amount%22%2C%22group%22%3A%22customer_payment%22%7D%5D&group_by=%5B%7B%22field%22%3A%22none%22%2C%22group%22%3A%22report%22%7D%5D&usestate=true&response_option=1&organization_id=60040042565
Request Method
GET



these are some other endpoints, first understand the balance sheet and profit_loss endpoint, how i have constructed them, for the above endpoints I want you to do the same, but for each time first see the raw api response, (for example by printing on the terminal) and then think about what are the essential information in the raw endpoints, and the create the function to format the raw response. after that is done add it to the mcp server, in the same way balance sheet and p & l is done