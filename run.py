# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high
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
    print("Please enter sales data for the last market")
    print("Data should be 6 figures seperated by commas")
    print("Example: 10,20,30,40,50,60\n")

    data_str = input("Enter your data here: ")

    sales_data = data_str.split(",")
    validate_data(sales_data)


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


get_sales_data()
