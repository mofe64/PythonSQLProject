from Operation import Operation

operation = Operation()


def get_customer_id(mobile_number):
    select_query = f'SELECT customerId FROM nubari.customer where mobileNumber = {mobile_number}'
    result = operation.perform_query_single(select_query)
    return result[0][0]


def create_new_account():
    firstname = input("Enter Your Firstname ")
    lastname = input("Enter Your Lastname ")
    middle_name = input("Enter Your middle name ")
    date_of_birth = input("Enter your date of birth in YYYY-MM-DD ")
    occupation = input("Enter your occupation ")
    mobile_number = input("Enter your phone number ")
    print("MO ", mobile_number)
    if firstname == "":
        raise ValueError("firstname cannot be empty")
    if lastname == "":
        raise ValueError("lastname cannot be empty")
    if mobile_number == "":
        raise ValueError("Mobile Number cannot be empty")

    insert_query_customer = 'insert into nubari.customer (firstName, lastname, middlename, mobileNumber, occupation, ' \
                            'date_of_birth)' \
                            ' values(%s,%s, %s, %s,%s, %s )'
    values = [(firstname, lastname, middle_name, int(mobile_number), occupation, date_of_birth)]
    operation.perform_insert(insert_query_customer, values)
    customer_id = get_customer_id(mobile_number)

    insert_query_account = 'insert into nubari.account(customerId, accountType, accountStatus) ' \
                           'values (%s, %s, %s)'
    account_type = int(
        input("Would you like to create a savings or current account, enter 1 for savings, 2 for current"))
    if account_type == 1:
        account_type = 'savings'
    else:
        account_type = 'current'
    values = [(customer_id, account_type, 'active')]
    operation.perform_insert(insert_query_account, values)


def get_account_details(account_number):
    customer_query = 'select * from nubari.customer join nubari.account  ' \
                     'on nubari.customer.customerId = nubari.account.customerId ' \
                     f'where nubari.account.accountNumber = {account_number}'
    result = operation.perform_query_single(customer_query)
    print(result[0])


def update_account_details():
    pass
