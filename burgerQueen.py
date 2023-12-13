import sqlite3

con = sqlite3.connect('burgerQueen.db')
cursor = con.cursor()

def register():
    print("Enter your details below to register a new account")
    print("")
    username = input("Enter your username: ").strip()
    password = input("Enter your password: ").strip()
    role = int(input("Are you employed at Burger Queen? (1 for yes, 0 for no): "))
    if not username or not password:
        print("A username and password is required")
        
    elif role not in [0, 1]:
        print("Please enter a valid role")
        
    else:
         cursor.execute("INSERT INTO person (Brukernavn, Passord, Ansatt) VALUES (?, ?, ?)", (username, password, role))
         con.commit()
         

def login():
     print("Enter your account information to login\n")
     print("")

     username = input("Enter your username: ").strip()
     password = input("Enter your password: ").strip()
     role = int(input("Are you employed at Burger Queen? (1 for yes, 0 for no): "))

     cursor.execute("SELECT * FROM person WHERE Brukernavn = ? AND Passord = ? AND Ansatt = ?", (username, password, role))
     user = cursor.fetchone()

     if user is None:
          print("Incorrect information, please try again")

     else:
          print("Logged in successfully")
          return username, password, role

def customerMenu(username, password, role):
     print("Welcome to Burger Queen " + username + "!")





print("Welcome to Burger Queen!")
print("")
print("+++++++++++++++++++++++++")
print("+++++++++++++++++++++++++")
print("")



def main():
    while True:
        startOption = input("1. Login\n2. Register")
        if role == 0:
          customerMenu(username, password, role)       
        elif startOption == "1":
             username, password, role = login()
             
        elif startOption == "2":
             register()
        else:
              print("Please enter a valid option")

    


if __name__ == "__main__":
    main()


