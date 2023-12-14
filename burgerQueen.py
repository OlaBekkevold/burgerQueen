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

def order(user):
    cursor.execute("SELECT * from burger")
    burger = cursor.fetchall()
    print("1. " + burger[0][1] + "\n2. " + burger[1][1] + "\n3. " + burger[2][1])
    item = input("What would you like to order? ")
    quantity = int(input("How many would you like? "))

    for i in range(quantity):

        if item == "1":
            print("You have ordered a " + burger[0][1] + "\n")
            cursor.execute("INSERT INTO ordre (Produsert, personID, burgerID) VALUES (0, ?, ?)", (user[0], burger[0][0]))
            con.commit()
            print("Your order has been placed")
        elif item == "2":
            print("You have ordered a " + burger[1][1] + "\n")
            cursor.execute("INSERT INTO ordre (Produsert, personID, burgerID) VALUES (0, ?, ?)", (user[0], burger[1][0]))
            con.commit()
            print("Your order has been placed")
        elif item == "3":
            print("You have ordered a " + burger[2][1] + "\n")
            cursor.execute("INSERT INTO ordre (Produsert, personID, burgerID) VALUES (0, ?, ?)", (user[0], burger[2][0]))
            con.commit()
            print("Your order has been placed")
        else:
            print("Please enter a valid option")





def customerMenu(user):
     print("Welcome to Burger Queen " + user[1] + "!\n")
     print("1. Order\n2. View your orders\n3. Logout\n")
     option = input("Select an option: ")

     if option == "1":
         order(user)
     elif option == "2":
         cursor.execute("""SELECT o."Ordrenummer", p."Brukernavn" AS "PersonName", b."Navn" AS "BurgerName", o."Produsert" FROM "ordre" o JOIN "person" p ON o."personID" = p."ID" JOIN "burger" b ON o."burgerID" = b."ID" WHERE p."ID" = ?;""", (user[0],))
         print(cursor.fetchall())
         

def main():
    user = None  
    while True:
        if user is None:
            user = login()  
        elif user[3] == 0: 
            customerMenu(user)  


if __name__ == "__main__":
    main()