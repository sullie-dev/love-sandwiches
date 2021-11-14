# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
from pprint import pprint
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("love_sandwiches")


def get_sales_data():
    """
    Get sales figures input from the user.
    """

    while True:
        print("Please enter sales data for the last market")
        print("Data should be 6 figures seperated by commas")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")

        sales_data = data_str.split(",")

        if validate_data(sales_data):
            print("Data is valid")
            break
    return sales_data


def validate_data(sales_data):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        if len(sales_data) != 6:
            [int(value) for value in sales_data]
            raise ValueError(
                f"There should be 6 values, you enereted {len(sales_data)}"
            )
    except ValueError as err:
        print(f"Invalid data: {err}, please try again")
        return False

    return True


def calculate_surplus_data(sales_data):
    """
    Calculate surplus data from the sales data.
    """
    print("Calculating surplus data...\n")
    stock_data = SHEET.worksheet("stock").get_all_values()
    stock_row = stock_data[-1]

    surplus_data = []
    for stock_value, sale_value in zip(stock_row, sales_data):
        surplus_value = int(stock_value) - sale_value
        surplus_data.append(surplus_value)

    return surplus_data


def update_worksheets(sheet, data):
    print(f"Updating {sheet} worksheet...\n")
    worksheet = SHEET.worksheet(sheet)
    worksheet.append_row(data)
    print(f"{sheet.capitalize()} worksheet updated successfully\n")


def get_last_5_enteries_sales():
    """Collect columns of datafrom the sales worksheet,collecting the last 5 enteries for each sandwhich and returns the data as a lists of lists"""
    sales = SHEET.worksheet("sales")
    columns = []

    for indx in range(1, 7):
        column = sales.col_values(indx)
        columns.append(column[-5:])
    return columns


def main():
    """Run all program fucntions"""
    data = get_sales_data()
    sale_data = [int(value) for value in data]
    update_worksheets("sales", sale_data)
    new_surplus_data = calculate_surplus_data(sale_data)
    update_worksheets("surplus", new_surplus_data)


print("Welcome to the Love Sandwich Sales Data Automation\n")
sales_columns = get_last_5_enteries_sales()
