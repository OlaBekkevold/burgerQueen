import sqlite3
con = sqlite3.connect('burgerQueen.db')
cursor = con.cursor()
         
# Function to login with an existing account or add a new on to the database
def login():
     
     loginOption = input("1. Login\n2. Register\n3. Exit\n")
    # The user logs in to an existing account
     if loginOption == "1":

        print("Enter your account information to login\n")
        username = input("Enter your username: ").strip() # Use strip to prevent empty usernames and passwords
        password = input("Enter your password: ").strip()

        # Check if the username and password exists in the database
        cursor.execute("SELECT * FROM person WHERE Brukernavn = ? AND Passord = ?", (username, password,))
        user = cursor.fetchone()

        if user is None:
            print("Incorrect information, please try again")

        else:
            print("Logged in successfully")
            return user # Return information about the user to be used in other functions
        
     # The user registers a new account   
     elif loginOption == "2":

        print("Enter your details below to register a new account\n")
        
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()
        role = int(input("Are you employed at Burger Queen? (1 for yes, 0 for no): ")) # role decides if the user will have access to employee functions

        # Check if the user input is valid
        if not username or not password:
            print("A username and password is required")
            
        elif role not in [0, 1]:
            print("Please enter a valid role")
            
        else:
            cursor.execute("SELECT * FROM person WHERE Brukernavn = ?", (username,)) # Try to find the username in the database
            user = cursor.fetchone()
            # Make sure the username is not already in use
            if user is not None:
                print("Username already exists, please try again")

            else:
                # Add the new user to the database and return information about the user to be used in other functions
                user = cursor.execute("INSERT INTO person (Brukernavn, Passord, Ansatt) VALUES (?, ?, ?)", (username, password, role))
                con.commit()
                cursor.execute("SELECT * FROM person WHERE Brukernavn = ?", (username,))
                user = cursor.fetchone()
                print("Account created successfully")
                return user
    # Stops the running of the code
     elif loginOption == "3":
        exit()
            
     else:
        print("Please enter a valid option")

# Function to order a burger
def order(user):
    # Get all the burgers from the database
    cursor.execute("SELECT * from burger")
    burger = cursor.fetchall()
    print("1. " + burger[0][1] + "\n2. " + burger[1][1] + "\n3. " + burger[2][1])

    # Ask the user what burger they want to order and how many
    item = int(input("What would you like to order? "))
    quantity = int(input("How many would you like? "))

    if item == 1:
        # item is turned into the correct index according to the database for better code readability
        item = 0
        # Add order as many times as the user wants
        for i in range(quantity):
            cursor.execute("INSERT INTO ordre (Produsert, personID, burgerID) VALUES (0, ?, ?)", (user[0], burger[item][0])) # Add the order with correct user ID and burger ID and set Produsert to 0
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


# Function to view all the orders a user has made
def viewOrder(user):
    # Joins the ordre, person and burger tables to get easy to read information about the orders according to the ID of the logged in user
    cursor.execute("""SELECT o."Ordrenummer", p."Brukernavn" AS "PersonName", b."Navn" AS "BurgerName", o."Produsert" FROM "ordre" o JOIN "person" p ON o."personID" = p."ID" JOIN "burger" b ON o."burgerID" = b."ID" WHERE p."ID" = ?;""", (user[0],))
    orders = cursor.fetchall()
    print(" ID  |  Person  |  Burger  |  Produced")
    # Print each order in it's own line
    for order in orders:
        print(order)

# Function to view and manage all orders
def manageOrders():
    # Joins the ordre, person and burger tables to display all orders
    cursor.execute("""SELECT o."Ordrenummer", p."Brukernavn" AS "PersonName", b."Navn" AS "BurgerName", o."Produsert" FROM "ordre" o JOIN "person" p ON o."personID" = p."ID" JOIN "burger" b ON o."burgerID" = b."ID";""")
    orders = cursor.fetchall()

    print(" ID  |  Person  |  Burger  |  Produced")
    for i in orders:
        print(i)

    # User has to enter the ID of the order they want to manage
    order = int(input("Which order do you want to manage? "))
    cursor.execute("SELECT * FROM ordre WHERE Ordrenummer = ?", (order,))
    selectedOrder = cursor.fetchone()
    # Check if the order exists
    if selectedOrder is None:
        print("Order does not exist")

    else:
        # User can mark the order as produced or cancel the order
        print("What do you want to do with this order? ")
        option = input("1. Mark as produced\n2. Cancel order\n")

        if option == "1":
            # Update the Produsert column to 1 to mark the order as produced
            cursor.execute("UPDATE ordre SET Produsert = 1 WHERE Ordrenummer = ?", (order,))
            con.commit()
            print("Order has been marked as produced")

            # Get the ingredients of the burger and subtract 1 from the quantity of each ingredient. The ingredients are stored in comma seperated list with the use of GROUP_CONCAT
            cursor.execute("""SELECT b."Navn" AS "BurgerName",
            GROUP_CONCAT(i."Navn", ', ') AS "Ingredients"
            FROM "burger" AS b
            JOIN
                "BurgerIngrediens" AS bi ON b."ID" = bi."burgerID"
            JOIN
                "ingrediens" AS i ON bi."ingrediensID" = i."ID"
            WHERE
                b."ID" = ?""", (selectedOrder[3],)) # selectedOrder[3] is the burgerID of the selected order
            
            ingredients = cursor.fetchall()
            ingredientList = ingredients[0][1].split(",") #Turn ingredients into a list seperated by commas
            ingredientList = [x.strip() for x in ingredientList] # Remove whitespace from the list
            
            # Iterate throug all the ingredients and subtract 1 from the quantity of each ingredient
            for ingredient in ingredientList:

                cursor.execute("""UPDATE ingrediens SET Antall = Antall - 1 WHERE Navn = ?;""", (ingredient,))
            
            con.commit()
            
            
        elif option == "2":
            # Delete the order from the database
            cursor.execute("DELETE FROM ordre WHERE Ordrenummer = ?", (order,))
            con.commit()
            print("Order has been deleted")

        else:
            print("Please enter a valid option")

# Function to view inventory of ingredients and add more of an ingredient
def manageIngredients():
    # print all ingredients and their quantity
    cursor.execute("SELECT * FROM ingrediens")
    ingredients = cursor.fetchall()
    print(" ID  |  Name  |  Quantity")
    for i in ingredients:
        print(i)

    option = input("\nDo you want to add ingredients? (y/n) ")

    if option == "y":
        # Ask the user which ingredient they will increase
        ingredient = input("\nEnter the name of the ingredient: ")
        quantity = int(input("How many?: "))

        cursor.execute("SELECT * FROM ingrediens WHERE Navn = ?", (ingredient,))
        selectedIngredient = cursor.fetchone()
        # Check if the ingredient exists
        if selectedIngredient is None:
            print("\nIngredient does not exist in the database")

        else:
            # Update the quantity of the ingredient based on the user input
            cursor.execute("UPDATE ingrediens SET Antall = Antall + ? WHERE Navn = ?", (quantity, ingredient,))
            con.commit()
            print("Ingredient has been added\n")
    
# Main menu where the user can choose what they want to do
def menu(user):
     
     # The user is presented with different options depending on their role. Which it gets from the user variable
     if user[3] == 0:
        print("\nWelcome to Burger Queen " + user[1] + "!\n")
        print("1. Order\n2. View your orders\n3. Logout\n")

     elif user[3] == 1:
         print("\nHave a nice day at work " + user[1] + "!\n")
         print("1. Order\n2. View your orders\n3. Logout\n4. Manage orders\n5. Manage ingredients\n")
    
     else:
         print("Invalid role")
         
     option = input("Select an option: ")
     return option # Return the option to be used in the main function
         

def main():
    # The user and option variables are used to get data about the user and what option they chose
    user = None
    option = None  
    while True:
        if user is None:
            user = login() # Login and get information about the user

        elif user is not None and option == None: # Before the user has chosen an option, the menu is displayed
           option = menu(user) # Get the option the user chose to be used in the if statements below

        elif option == "1":
            order(user) # Run the order function with information about the user
            option = None # Option is set to None to display the menu after running the function

        elif option == "2":
            viewOrder(user)
            option = None

        elif option == "3":
            main() # Run main() to reset the program and log out
        
        elif option == "4":
            manageOrders()
            option = None

        elif option == "5":
            manageIngredients()
            option = None

# Run the main function when the program is started
if __name__ == "__main__":
    main()