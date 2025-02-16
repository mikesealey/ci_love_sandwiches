import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def get_sales_data():
    """
    Get sales figires input from the user
    """

    while True:
        print ("please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")
        sales_data = data_str.split(",")
        validate_data(sales_data)

        if validate_data(sales_data):
            print("Data is valid")
            break

    return sales_data

def update_worksheet(data, worksheet):
    """
    Recieves a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} updated successfully...\n")

def validate_data(values):
    """
    Inside the try, converts all string values into integers
    Raises ValueError is strings cannot be converted into int
    or if there aren't 6 values in the list
    """
    try:
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values expected - you provided {len(values)}"
            )
        [int(value) for value in values]
    except ValueError as e:
        print(f"Invalid data: {e}, please try again. \n")
        return False

    return True

def calculate_surplus_data(sales_row):
    """
    Compare sales wwith stock and calculate the surplus for each item type.

    The surplus is defined as the sales figure subtracted from the stock:
    - positive surplus indicates waste
    - negative surplus indicates extra sandwiches made when stocks ran out.
    """
    print("Claculating surpluse data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)
    
    return surplus_data

def calculate_stock_data(data):
    """
    Caclculae the average stcok for each tiem type, adding 10%
    """
    print("Calculating the stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))
    
    return new_stock_data

def get_last_5_entries_sales():
    """
    Collects collumns of data from sales worksheet, collecting
    the last 5 entries for each sandiwch and returns the data
    as a list of lists
    """
    sales = SHEET.worksheet("sales")
    # column = sales.col_values(3)
    # print(column)
    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    return columns

def get_stock_values(data):
    """
    Gets stock values
    """
    sheet = SHEET.worksheet("stock").get_all_values()
    sandwiches = sheet[0]
    quantities = sheet[-1]

    tomorrow_list = dict(zip(sandwiches, quantities))
    print(f"Make the following numbers of sandwiches for the next market: \n\n{tomorrow_list}")

def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    new_surplus_data = calculate_surplus_data(sales_data)
    update_worksheet(new_surplus_data, "surplus")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")
    sales_columns = get_last_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    print(stock_data)
    stock_values = get_stock_values(stock_data)
    print (stock_values)



print("Welcome to Love Sandwiches Data Automation")
main()
