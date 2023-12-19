import sqlite3
con = sqlite3.connect('burgerQueen.db')
cursor = con.cursor()
         

def login():
     
     loginOption = input("1. Login\n2. Register\n3. Exit\n")

     if loginOption == "1":

        print("Enter your account information to login\n")
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()

        cursor.execute("SELECT * FROM person WHERE Brukernavn = ? AND Passord = ?", (username, password,))
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
                user = cursor.execute("INSERT INTO person (Brukernavn, Passord, Ansatt) VALUES (?, ?, ?)", (username, password, role))
                con.commit()
                cursor.execute("SELECT * FROM person WHERE Brukernavn = ?", (username,))
                user = cursor.fetchone()
                print("Account created successfully")
                return user
            
     elif loginOption == "3":
        exit()
            
     else:
        print("Please enter a valid option")

def order(user):
    cursor.execute("SELECT * from burger")
    burger = cursor.fetchall()
    print("1. " + burger[0][1] + "\n2. " + burger[1][1] + "\n3. " + burger[2][1])
    item = int(input("What would you like to order? "))
    quantity = int(input("How many would you like? "))

    if item == 1:
        item = 0
        for i in range(quantity):
            cursor.execute("INSERT INTO ordre (Produsert, personID, burgerID) VALUES (0, ?, ?)", (user[0], burger[item][0]))
            con.commit()
            
    elif item == 2:
        item = 1
        for i in range(quantity):
            cursor.execute("INSERT INTO ordre (Produsert, personID, burgerID) VALUES (0, ?, ?)", (user[0], burger[item][0]))
            con.commit()

    elif item == 3:
        item = 2
        for i in range(quantity):
            cursor.execute("INSERT INTO ordre (Produsert, personID, burgerID) VALUES (0, ?, ?)", (user[0], burger[item][0]))
            con.commit()

    else:
        print("Please enter a valid option")
        
    print("You have ordered " + str(quantity) + " " + burger[item][1] + "\n")



def viewOrder(user):
    cursor.execute("""SELECT o."Ordrenummer", p."Brukernavn" AS "PersonName", b."Navn" AS "BurgerName", o."Produsert" FROM "ordre" o JOIN "person" p ON o."personID" = p."ID" JOIN "burger" b ON o."burgerID" = b."ID" WHERE p."ID" = ?;""", (user[0],))
    orders = cursor.fetchall()
    for order in orders:
        print(order)


def manageOrders():
    cursor.execute("""SELECT o."Ordrenummer", p."Brukernavn" AS "PersonName", b."Navn" AS "BurgerName", o."Produsert" FROM "ordre" o JOIN "person" p ON o."personID" = p."ID" JOIN "burger" b ON o."burgerID" = b."ID";""")
    orders = cursor.fetchall()

    for i in orders:
        print(i)

    order = int(input("Which order do you want to manage? "))
    cursor.execute("SELECT * FROM ordre WHERE Ordrenummer = ?", (order,))
    selectedOrder = cursor.fetchone()

    if selectedOrder is None:
        print("Order does not exist")

    else:
        print("What do you want to do with this order? ")
        option = input("1. Mark as produced\n2. Cancel order\n")

        if option == "1":
            cursor.execute("UPDATE ordre SET Produsert = 1 WHERE Ordrenummer = ?", (order,))
            con.commit()
            print("Order has been marked as produced")

            cursor.execute("""SELECT b."Navn" AS "BurgerName",
            GROUP_CONCAT(i."Navn", ', ') AS "Ingredients"
            FROM "burger" AS b
            JOIN
                "BurgerIngrediens" AS bi ON b."ID" = bi."burgerID"
            JOIN
                "ingrediens" AS i ON bi."ingrediensID" = i."ID"
            WHERE
                b."ID" = ?""", (selectedOrder[3],))
            
            ingredients = cursor.fetchall()
            ingredientList = ingredients[0][1].split(",")
            ingredientList = [x.strip() for x in ingredientList]
            
            for ingredient in ingredientList:

                cursor.execute("""UPDATE ingrediens SET Antall = Antall - 1 WHERE Navn = ?;""", (ingredient,))
            
            con.commit()
            
            
        elif option == "2":
            cursor.execute("DELETE FROM ordre WHERE Ordrenummer = ?", (order,))
            con.commit()
            print("Order has been deleted")

        else:
            print("Please enter a valid option")

def manageIngredients():
    cursor.execute("SELECT * FROM ingrediens")
    ingredients = cursor.fetchall()
    for i in ingredients:
        print(i)

    option = input("Do you want to add ingredients? (y/n) ")

    if option == "y":
        ingredient = input("Enter the name of the ingredient: ")
        quantity = int(input("How many?: "))

        cursor.execute("SELECT * FROM ingrediens WHERE Navn = ?", (ingredient,))
        selectedIngredient = cursor.fetchone()

        if selectedIngredient is None:
            print("Ingredient does not exist in the database")

        else:
            cursor.execute("UPDATE ingrediens SET Antall = Antall + ? WHERE Navn = ?", (quantity, ingredient,))
            con.commit()
            print("Ingredient has been added/n")
    

def menu(user):
     if user[3] == 0:
        print("Welcome to Burger Queen " + user[1] + "!\n")
        print("1. Order\n2. View your orders\n3. Logout\n")

     elif user[3] == 1:
         print("Have a nice day at work " + user[1] + "!\n")
         print("1. Order\n2. View your orders\n3. Logout\n4. Manage orders\n5. Manage ingredients\n")
    
     else:
         print("Invalid role")
         
     option = input("Select an option: ")
     return option
         

def main():
    user = None
    option = None  
    while True:
        if user is None:
            user = login()  

        elif user is not None and option == None: 
           option = menu(user)

        elif option == "1":
            order(user)
            option = None

        elif option == "2":
            viewOrder(user)
            option = None

        elif option == "3":
            main()
        
        elif option == "4":
            manageOrders()
            option = None

        elif option == "5":
            manageIngredients()
            option = None


if __name__ == "__main__":
    main()