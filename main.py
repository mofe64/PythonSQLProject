from Connection import Connection

from Util import *

userChoice_str = input("""Welcome to Nubari Bank 
Enter 1 To Create a new Account
Enter 2 To Check your Account details
Enter 3 To Update your Account Details
Enter 4 To Make A New Transaction
Enter 5 To View Your Transaction History
Enter 6 To Delete Your Account
Enter 7 to Quit  
""")

userChoice_int = int(userChoice_str)

if userChoice_int == 1:
    create_new_account()
if userChoice_int == 2:
    account_number = int(input("Enter account number"))
    get_account_details(account_number)
if userChoice_int == 3:
    account_number = int(input("Enter account number"))
    get_account_details(account_number)
