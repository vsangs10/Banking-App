import sqlite3

# global variables for database access
connection = sqlite3.connect('vbank.sqlite')
cursor = connection.cursor()
totalaccount = 0

# initial setup - create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts 
(
  account_num INTEGER PRIMARY KEY,
  pin INTEGER,
  user_name TEXT,
  current_balance REAL
);
""")
#Create new Account with zero balance
def create_new_account(user_name,account_num, pin):
  """
  Create new account with zero balance.
  Return the account number just created.
  """
  cursor.execute("""
    INSERT INTO accounts (
       pin, user_name, account_num, current_balance
      ) 
    VALUES (?, ?,?, 0.0);
  """, (pin, user_name, account_num))
  # always call commit when updating table
  print("Your account details are: username is: " + str(user_name) + "Pin is: " + str(pin) +"Account number is: " +str(account_num))
  connection.commit()
  
  # to retreive the last inserted account number
  # MySQL has equivalent function: LAST_INSERT_ID()
  cursor.execute("SELECT last_insert_rowid();")
  last_id = cursor.fetchall()[0][0]
  
  return last_id
  
def check_balance(account_num, user_name, pin):
  """
  Check balance by account number and pin. 
  Return None if account_num + pin is invalid.
  """
  cursor.execute("""
    SELECT current_balance
    FROM accounts
    WHERE account_num = ? AND user_name = ? AND pin = ?
    ;
    """, (account_num, user_name, pin)
  )
  
  results = cursor.fetchall()
  if len(results) != 1:
    return None
  return results[0][0]

# to add deposit or withdrawal functionality
# read about UPDATE statement in SQL
def deposit_amount(new_amount, account_num, user_name, pin):
  cursor.execute("""
  UPDATE accounts SET current_balance = ?
  WHERE account_num = ? AND user_name = ? AND pin = ?
  """, (new_amount,account_num,user_name, pin)
  )
  connection.commit()
  results = cursor.fetchall()
  return

def withdrawal_amount(new_amount, account_num, user_name, pin):
  cursor.execute("""
  UPDATE accounts SET current_balance = ?
  WHERE account_num = ? AND user_name = ? AND pin = ?
  """, (new_amount,account_num,user_name, pin)
  )
  connection.commit()
  results = cursor.fetchall()
  return
# sample interaction with banking app:
# Find total number of accounts created in bank
def total_account():
  totalaccount = cursor.execute("Select count(user_name) from accounts group by user_name")
  return totalaccount
  
def login_check(checkuser, checkpin):
    cursor.execute("""
      SELECT user_name
      FROM accounts
      WHERE user_name = ? AND pin = ?
      ;""", (checkuser, checkpin))
    user_result = cursor.fetchall()
    if len(user_result)==1:
     # return user_result
      print ("Welcome to Vedant Bank " + checkuser)
      return 0
    else:
      print ("You have entered invalid account details. Please try again")
      return 1
  
print("Welcome to Vedant Bank \n")
num = int(input("Press 1 to login to your account, or Press 2 to Create a New account: "))
if (num == 1):
  #here we have to create a new function that loggs into the account by checkign if we are equal to any of the userId's and passwords
  valid_user=1
  while valid_user == 1:
    checkuser = input("What is your username: ")
    checkpin = input ("What is your pin: ")
    valid_user = login_check(checkuser,checkpin)
    trans = 'Y'
    while trans == 'Y':
      checkkval = 0
      checkkval = int(input("Please enter 10 to check your balance , 11 to deposit or 12 to withdraw: "))
      if checkkval == 10:
        account_num = input("Which account would you like to check the balance of: ")
        balance = check_balance(account_num,checkuser, checkpin)
        print ("Your balance is: ", balance)
      elif checkkval == 11:
        account_num = input("Which account would you like to deposit the amount into: ")
        d_amount = int(input("Enter the amount you would like to deposit: "))
        print ("So you want to deposit? $", d_amount)
        new_amount =check_balance(account_num,checkuser, checkpin) + d_amount
        print ("Your new balance would be: $", new_amount)
        deposit_amount(new_amount, account_num, checkuser, checkpin)
        print ("You deposited amount: $", d_amount)
      elif checkkval ==12:
        account_num = input("Which account would you like to withdraw the amount from: ")
        w_amount = int(input("Enter the amount you would like to withdraw: "))
        print ("So you want to withdraw? $", w_amount)
        new_amount =check_balance(account_num,checkuser, checkpin) - w_amount
        print ("Your new balance would be: $", new_amount)
        withdrawal_amount(new_amount, account_num, checkuser, checkpin)
        print ("You withdrew amount: $", w_amount)
      else:
        print ("Thank you for visting us today")
      trans = input("Would you like to do another transaction? Enter 'Y or 'N': ")
    else: print("Thank you for visiting us today")
else:
  username = input("Please enter a username: ")
  account_num = 0
  account_num += 1
  pin = int(input("Please enter a 4 digit pin: "))
  create_new_account(username, account_num, pin)  
connection.close()


#testing 12
