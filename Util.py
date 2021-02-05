from Operation import Operation

operation = Operation()


def get_customer_id(mobile_number):
    select_query = f'SELECT customerId FROM nubari.customer where mobileNumber = {mobile_number}'
    result = operation.perform_query_single(select_query)
    return result[0]


def create_new_account():
    firstname = input("Enter Your Firstname ")
    lastname = input("Enter Your Lastname ")
    middle_name = input("Enter Your middle name ")
    date_of_birth = input("Enter your date of birth in YYYY-MM-DD ")
    occupation = input("Enter your occupation ")
    mobile_number = input("Enter your phone number ")
    if firstname == "":
        raise ValueError("firstname cannot be empty")
    if lastname == "":
        raise ValueError("lastname cannot be empty")
    if mobile_number == "":
        raise ValueError("Mobile Number cannot be empty")

    insert_query_customer = 'insert into nubari.customer (firstName, lastname, middlename, mobileNumber, occupation, ' \
                            'date_of_birth)' \
                            ' values(%s,%s, %s, %s,%s, %s )'
    values = (firstname, lastname, middle_name, mobile_number, occupation, date_of_birth)
    operation.perform_insert(insert_query_customer, values)
    customer_id = get_customer_id(mobile_number)

    insert_query_account = 'insert into nubari.account(customerId, accountType, accountStatus) ' \
                           'values (%s, %s, %s)'
    print()
    account_type = int(
        input("Would you like to create a savings or current account, enter 1 for savings, 2 for current "))
    print()

    if account_type == 1:
        account_type = 'savings'
    else:
        account_type = 'current'
    values = (customer_id, account_type, 'active')
    operation.perform_insert(insert_query_account, values)
    get_customer_account_number_query = f'select accountNumber from nubari.account where customerId = {customer_id}'
    customer_account_number = operation.perform_query_single(get_customer_account_number_query)[0]
    print()
    print(f"Your account number is {customer_account_number} ")
    print()


def get_account_details(account_number):
    customer_query = 'select * from nubari.customer join nubari.account  ' \
                     'on nubari.customer.customerId = nubari.account.customerId ' \
                     f'where nubari.account.accountNumber = {account_number}'
    result = operation.perform_query_single(customer_query)
    user_details = {
        "firstname ": result[1],
        "lastname ": result[2],
        "middle name ": result[3],
        "mobile number ": result[4],
        "occupation ": result[5],
        "date of birth ": result[6],
        "account number ": result[7],
        "account type ": result[9],
        "account status ": result[10],
        "account opening date ": result[11]
    }

    print()
    for key, value in user_details.items():
        print(f"{key} : {value}")
    print()


def update_account_details(account_number):
    loop_control = 1
    updated_values = {}
    while loop_control != -1:
        user_input_str = input("""
        Enter 1 to change your firstname
        Enter 2 to change your lastname
        Enter 3 to change your middle name
        Enter 4 to change your mobileNumber
        Enter 5 to change your occupation
        Enter 6 to change your date of birth
        Enter 7 to quit update Menu
        """)
        user_input_int = int(user_input_str)
        if user_input_int == 1:
            updated_values["firstname"] = input("Enter your new firstname: ")
        elif user_input_int == 2:
            updated_values["lastname"] = input("Enter your new lastname: ")
        elif user_input_int == 3:
            updated_values["middlename"] = input("Enter your new middle name: ")
        elif user_input_int == 4:
            updated_values["mobileNumber"] = input("Enter your new mobile number: ")
        elif user_input_int == 5:
            updated_values["occupation"] = input("Enter your new occupation: ")
        elif user_input_int == 6:
            updated_values["date_of_birth"] = input("Enter your new date of birth in YYYY-MM-DD format: ")
        elif user_input_int == 7:
            loop_control = -1
        # print(updated_values)
    query = 'select nubari.customer.customerId from nubari.customer join nubari.account  ' \
            'on nubari.customer.customerId = nubari.account.customerId ' \
            f'where nubari.account.accountNumber = {account_number}'
    customer_id = operation.perform_query_single(query)[0]
    for key, value in updated_values.items():
        # print("key is ", key)
        # print("Value is ", value)
        update_query = f"update nubari.customer set {key} = %s where customerId = {customer_id}"
        val = (value,)
        print(update_query)
        operation.perform_update(update_query, val)


def make_transaction(account_number):
    insert_transaction_query = 'Insert into nubari.transactions(accountNumber, transactionType, transactionAmount, ' \
                               'transactionMedium) ' \
                               'values (%s, %s, %s, %s)'
    transaction_type = input("Enter 1 for a withdraw transaction, Enter 2 for a deposit ")
    if int(transaction_type) == 1:
        transaction_type = 'debit'
    else:
        transaction_type = 'credit'
    transaction_amount = int(input("Enter the amount "))

    values = (account_number, transaction_type, transaction_amount, 'web')
    operation.perform_insert(insert_transaction_query, values)


def get_transaction_history(account_number):
    query = 'select * from nubari.transactions ' \
            f'where accountNumber = {account_number}'
    query_results = operation.perform_group_query(query)
    for record in query_results:
        transaction_details = {
            "transaction account number ": record[1],
            "transaction date ": record[2].__str__(),
            "transaction type ": record[3],
            "transaction Amount": record[4],
            "transaction medium ": record[5]
        }
        print()
        for key, value in transaction_details.items():
            print(f"{key} : {value}")
        print()


def delete_account(account_number):
    get_customer_id_query = f"Select customerId from nubari.account where accountNumber = {account_number}"
    customer_id = operation.perform_query_single(get_customer_id_query)[0]
    delete_account_query = f"Delete from nubari.account where accountNumber = %s"
    delete_customer_details = f"Delete from nubari.customer where customerId = %s"
    val = (account_number,)
    print()
    print(f"deleting account with account number {account_number} .....")
    operation.perform_delete(delete_account_query, val)
    print("Account deleted")
    print()
    print(f"Deleting customer details .....")
    operation.perform_delete(delete_customer_details, (customer_id,))
    print("customer details deleted successfully ")
    print()
