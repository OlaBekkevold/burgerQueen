import sqlite3

con = sqlite3.connect('burgerQueen.db')
cursor = con.cursor()
         
def login():
     
     loginOption = input("1. Login\n2. Register\n")

     if loginOption == "1":

        print("Enter your account information to login\n")
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()
        role = int(input("Are you employed at Burger Queen? (1 for yes, 0 for no): "))

        cursor.execute("SELECT * FROM person WHERE Brukernavn = ? AND Passord = ? AND Ansatt = ?", (username, password, role))
        user = cursor.fetchone()
        

        if user is None:
            print("Incorrect information, please try again")

        else:
            print("Logged in successfully")
            return user
        
     elif loginOption == "2":

        print("Enter your details below to register a new account\n")
        
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()
        role = int(input("Are you employed at Burger Queen? (1 for yes, 0 for no): "))

        if not username or not password:
            print("A username and password is required")
            
        elif role not in [0, 1]:
            print("Please enter a valid role")
            
        else:
            cursor.execute("SELECT * FROM person WHERE Brukernavn = ?", (username,))
            user = cursor.fetchone()
            if user is not None:
                print("Username already exists, please try again")
            else:
                cursor.execute("INSERT INTO person (Brukernavn, Passord, Ansatt) VALUES (?, ?, ?)", (username, password, role))
                con.commit()
                print("Account created successfully")
                return user
            
            
            

     else:
        print("Please enter a valid option")



def customerMenu(username, password, role):
     print("Welcome to Burger Queen " + username + "!")


def main():
    user = None  
    while True:
        if user is None:
            user = login()  
        elif user[3] == 0: 
            customerMenu(user[1], user[2], user[3])  


if __name__ == "__main__":
    main()