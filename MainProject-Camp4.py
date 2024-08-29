import mysql.connector
import re
import datetime
from tabulate import tabulate
import textwrap


databaseobj = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Aswin2002',
    database='Library'
)
login = databaseobj.cursor()

login.execute("""
CREATE TABLE IF NOT EXISTS Plan(
    PlanID INT PRIMARY KEY,
    Duration VARCHAR(20),
    Cost DECIMAL(10,2),
    Coins DECIMAL(5,0),
    Details VARCHAR(200)
)
""")
login.execute("""
CREATE TABLE IF NOT EXISTS UserInfo(
    UserName VARCHAR(25) PRIMARY KEY,
    Password VARCHAR(20),
    FirstName VARCHAR(50),
    LastName VARCHAR(50),
    MobileNumber VARCHAR(10),
    Email VARCHAR(50),
    PlanID INT,
    Date_and_Time VARCHAR(30),
    FOREIGN KEY (PlanID) REFERENCES Plan(PlanID) ON DELETE SET NULL
)
""")
login.execute("""
CREATE TABLE IF NOT EXISTS Login(
    Password VARCHAR(20),
    UserName VARCHAR(25),
    FOREIGN KEY (UserName) REFERENCES UserInfo(UserName)
)
""")
login.execute("""
CREATE TABLE IF NOT EXISTS Genre(
    GenreID INT PRIMARY KEY,
    GenreName VARCHAR(50)
)
""")
login.execute("""
CREATE TABLE IF NOT EXISTS Author(
    AuthorID INT PRIMARY KEY,
    AuthorName VARCHAR(50)
)
""")

login.execute("""
CREATE TABLE IF NOT EXISTS Book(
    BookID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(200),
    GenreID INT,
    AuthorID INT,
    Details VARCHAR(500),
    Coins DECIMAL(3),
    Ratings DECIMAL(2,1),
    FOREIGN KEY (GenreID) REFERENCES Genre(GenreID) ON DELETE CASCADE,
    FOREIGN KEY (AuthorID) REFERENCES Author(AuthorID) ON DELETE CASCADE
)
""")

login.execute("""
CREATE TABLE IF NOT EXISTS Feedback(
    FeedbackID INT AUTO_INCREMENT PRIMARY KEY,
    Feedback VARCHAR(250),
    UserName VARCHAR(25),
    Response VARCHAR(250),
    FOREIGN KEY (UserName) REFERENCES UserInfo(UserName)
)
""")
login.execute("""
CREATE TABLE IF NOT EXISTS Favourite(
    FavouriteID INT AUTO_INCREMENT PRIMARY KEY,
    UserName VARCHAR(25),
    BookID INT,
    Coins DECIMAL(3),
    FOREIGN KEY (UserName) REFERENCES UserInfo(UserName),
    FOREIGN KEY (BookID) REFERENCES Book(BookID)
)
""")
login.execute("""
CREATE TABLE IF NOT EXISTS Balance(
    BalanceID INT AUTO_INCREMENT PRIMARY KEY,
    Coins DECIMAL(10,2),
    UserName VARCHAR(20),
    PlanID INT,
    FOREIGN KEY (UserName) REFERENCES UserInfo(UserName),
    FOREIGN KEY (PlanID) REFERENCES Plan(PlanID)
)
""")
login.execute("""
CREATE TABLE IF NOT EXISTS UserAccount(
    AccountID INT AUTO_INCREMENT PRIMARY KEY,
    UserName VARCHAR(20),
    PlanID INT,
    BalanceID INT,
    FOREIGN KEY (UserName) REFERENCES UserInfo(UserName),
    FOREIGN KEY (PlanID) REFERENCES Plan(PlanID),
    FOREIGN KEY (BalanceID) REFERENCES Balance(BalanceID)
)
""")
login.execute("""
CREATE TABLE IF NOT EXISTS Rented(
    RentedID INT AUTO_INCREMENT PRIMARY KEY,
    BookID INT,
    StartDate VARCHAR(30),
    EndDate VARCHAR(30),
    BalanceID INT,
    UserName VARCHAR(20),
    FOREIGN KEY (UserName) REFERENCES UserInfo(UserName),
    FOREIGN KEY (BalanceID) REFERENCES Balance(BalanceID), 
    FOREIGN KEY (BookID) REFERENCES Book(BookID)
)
""")
login.execute("""
CREATE TABLE IF NOT EXISTS Payment(
    PaymentID INT AUTO_INCREMENT PRIMARY KEY,
    Cost DECIMAL(10,2),
    BookID INT,
    BalanceID INT,
    PlanID INT,
    PaymentFor VARCHAR(30),
    ModeOfPayment VARCHAR(30),
    Date_and_Time VARCHAR(30),
    FOREIGN KEY (PlanID) REFERENCES Plan(PlanID),
    FOREIGN KEY (BookID) REFERENCES Book(BookID),
    FOREIGN KEY (BalanceID) REFERENCES Balance(BalanceID)
)
""")


def startpage():
    while True:
        print("""    
                                                -------------------------------------------------------------------------------------
                                                                             LIBRARY MANAGEMENT SYSTEM
                                                -------------------------------------------------------------------------------------
        
                                                 1. Log In
                                                 2. Register
                                                 3. Exit
                """)
        option = input("Enter the option [1/2/3]: ")
        if option == "1":
            loginpageuser()
        elif option == "2":
            register()
        elif option == "3":
            print("""                            
                                                -------------------------------------------------------------------------------------
                                                                 Thank you for using the Library. Have a nice day!
                                                -------------------------------------------------------------------------------------                       
                  """)
            exit()
        elif option == "xxxx":
            loginpageadmin()
        else:
            print("INVALID!!! Enter only numbers from 1 to 3.")


def register():
    while True:
        try:
            global UserName
            print("Register Your Details Here.")
            while True:
                UserName = input("Enter Your UserName: ")
                if " " not in UserName and re.fullmatch(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{5,25}$', UserName):
                    break
                else:
                    print("INVALID!!! UserName should be an alpha-numeric character of length 5 to 25 with no spaces.")
            while True:
                Password = input("Enter Your password: ")
                if " " not in Password and re.fullmatch(r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+!_]).{5,20}$',
                                                        Password):
                    ConfirmPassword = input("Confirm your password: ")
                    if Password == ConfirmPassword:
                        break
                    else:
                        print("Passwords do not match! Please try again.")
                else:
                    print(
                        "INVALID!!! Password must be 5-20 characters long, containing at least one uppercase letter, one lowercase letter, one digit, and one special character [@ # $ % ^ & + ! _ ].")
            while True:
                FirstName = input("Enter the First Name: ")
                if re.fullmatch("[A-Za-z]{3,25}", FirstName):
                    break
                else:
                    print("INVALID!!! First Name must be 3-25 characters long and contain only alphabets.")
            while True:
                LastName = input("Enter the Last Name: ")
                if re.fullmatch("[A-Za-z]{1,25}", LastName):
                    break
                else:
                    print("INVALID!!! Last Name must be 1-25 characters long and contain only alphabets.")
            while True:
                MobileNumber = input("Enter the Mobile Number: ")
                if len(MobileNumber) == 10 and MobileNumber.isdigit() and MobileNumber[0] in '6789':
                    break
                else:
                    print("INVALID!!! Mobile Number must be a 10-digit number starting with 6, 7, 8, or 9.")
            while True:
                Email = input("Enter the Email: ")
                if re.fullmatch(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", Email):
                    break
                else:
                    print("INVALID!!! Please enter a valid email address.")
            while True:
                viewplan()
                PlanID = input("Enter the PlanID: ")
                if len(PlanID) == 3 and PlanID.isdigit():
                    print("""                              
                                                -------------------------------------------------------------------------------------
                                                                               CHOOSE YOUR PAYMENT METHOD
                                                -------------------------------------------------------------------------------------    

                                                ->Choose an option to continue :

                                                1. Card
                                                2. UPI
                                                3. QR Code
                                                4. Cancel
                                                5. Homepage
                            """)

                    option = input("Enter Your Payment Method: ")
                    if option == "1":
                        payment = "Card"
                        print("""                          
                                                -------------------------------------------------------------------------------------
                                                                               PAYMENT SUCCESSFUL!!!
                                                -------------------------------------------------------------------------------------                       
                                 """)
                        break
                    elif option == "2":
                        payment = "UPI"

                        print("""                          
                                                -------------------------------------------------------------------------------------
                                                                               PAYMENT SUCCESSFUL!!!
                                                -------------------------------------------------------------------------------------                       
                                  """)
                        break
                    elif option == "3":
                        payment = "QR Code"
                        print("""                          
                                                -------------------------------------------------------------------------------------
                                                                               PAYMENT SUCCESSFUL!!!
                                                -------------------------------------------------------------------------------------                       
                              """)
                        break
                    elif option == "4":
                        return register()
                    elif option == "5":
                        return startpage()
                    else:
                        print("INVALID!!! Please select a valid payment method.")
                else:
                    print("INVALID!!! PlanID must be a 3-digit number.")
            login.execute("SELECT Coins, Cost FROM Plan WHERE PlanID = %s", (PlanID,))
            result = login.fetchone()
            if not result:
                print("INVALID!!! PlanID not found.")
                continue
            Coins, Cost = result
            Date_and_Time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            insert_query_reg = (
                "INSERT INTO UserInfo (UserName, Password, FirstName, LastName, MobileNumber, Email, PlanID, Date_and_Time) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            )
            login.execute(insert_query_reg,
                          (UserName, Password, FirstName, LastName, MobileNumber, Email, PlanID, Date_and_Time))
            insert_query_user = "INSERT INTO Login (UserName, Password) VALUES (%s, %s)"
            login.execute(insert_query_user, (UserName, Password))
            insert_query_balance = "INSERT INTO Balance (UserName, PlanID, Coins) VALUES (%s, %s, %s)"
            login.execute(insert_query_balance, (UserName, PlanID, Coins))
            login.execute("SELECT BalanceID FROM Balance WHERE UserName = %s AND PlanID = %s", (UserName, PlanID))
            balance_result = login.fetchone()
            if not balance_result:
                print("Error retrieving BalanceID. Please try again.")
                continue
            BalanceID = balance_result[0]
            insert_query_user_account = "INSERT INTO UserAccount (UserName, PlanID, BalanceID) VALUES (%s, %s, %s)"
            login.execute(insert_query_user_account, (UserName, PlanID, BalanceID))
            insert_payment = (
                "INSERT INTO Payment (Cost, PlanID, BalanceID, PaymentFor, ModeOfPayment, Date_and_Time) "
                "VALUES (%s, %s, %s, %s, %s, %s)"
            )
            login.execute(insert_payment, (Cost, PlanID, BalanceID, 'Plan', payment, Date_and_Time))
            databaseobj.commit()
            print("""                          
                                               -------------------------------------------------------------------------------------
                                                                        You have successfully registered!!!
                                               -------------------------------------------------------------------------------------                       
            """)

            startpage()
            break

        except Exception as e:
            print(f"An error occurred: {e}")
            databaseobj.rollback()


def loginpageuser():
    global UserName
    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        UserName = input("Enter UserName: ")
        if UserName == "":
            print("This field cannot be empty.")
            attempts += 1
            remaining_attempts = max_attempts - attempts
            if remaining_attempts == 0:
                print("You have been logged out due to too many failed login attempts.")
                return
            print(f"You have {remaining_attempts} attempts left.")
            continue
        Password = input("Enter the password: ")
        if Password == "":
            print("This field cannot be empty.")
            attempts += 1
            remaining_attempts = max_attempts - attempts
            if remaining_attempts == 0:
                print("You have been logged out due to too many failed login attempts.")
                return
            print(f"You have {remaining_attempts} attempts left.")
            continue
        select_query = "SELECT * FROM Login WHERE UserName=%s COLLATE utf8mb4_bin AND Password=%s COLLATE utf8mb4_bin"
        login.execute(select_query, (UserName, Password))
        result = login.fetchone()
        if result is not None:
            print("""                            
                                                -------------------------------------------------------------------------------------              
                                                                             You have Logged in successful!!!
                                                -------------------------------------------------------------------------------------                       
                              """)
            
            optionpageuser()
            return
        else:
            attempts += 1
            remaining_attempts = max_attempts - attempts
            if remaining_attempts <= 0:
                print("You have been logged out due to too many failed login attempts.")
                exit()
            else:
                print(f"Incorrect UserName or Password. You have {remaining_attempts} attempts left.")


def optionpageuser():
    global UserName
    while True:
        print(f"""                              
                                                -------------------------------------------------------------------------------------
                                                                                WELCOME {UserName}
                                                -------------------------------------------------------------------------------------    
                                                                       
                                                ->Choose an option to continue :
                                                
                                                1. View All Books
                                                2. Favourite Books
                                                3. Rented Books
                                                4. Feedback
                                                5. Account
                                                6. Log out
        """)

        option = input("Choose an option [1 to 9]: ")
        if option == "1":
            viewbookuser()
        elif option == "2":
            favorite()
        elif option == "3":
            rent()
        elif option == "4":
            userfeedback()
        elif option == "5":
            accounts()
        elif option == "6":
            print("""                            
                                                -------------------------------------------------------------------------------------
                                                                You have successfully logged out... Have a nice day!!!
                                                -------------------------------------------------------------------------------------                        
                  """)
            
            startpage()
        else:
            print("INVALID!!! Choose options from 1 to 9 only.")

def viewbookuser():
    query = '''SELECT b.BookID, b.Title, b.Details, a.AuthorName, g.GenreName, b.Coins, b.Ratings 
               FROM Book b 
               INNER JOIN Author a ON b.AuthorID = a.AuthorID 
               INNER JOIN Genre g ON b.GenreID = g.GenreID'''
    login.execute(query)
    query_result = login.fetchall()

    if query_result:
        wrapped_result = []
        for row in query_result:
            adjusted_row = list(row)
            adjusted_row[2] = "\n".join(textwrap.wrap(adjusted_row[2], width=75))
            wrapped_result.append(adjusted_row)
            wrapped_result.append([""] * len(row))
        print(tabulate(wrapped_result,
                       headers=["BookID", "Title", "Details", "AuthorName", "GenreName", "Coins", "Ratings"]))
        
    else:
        print("""                            
                                                -------------------------------------------------------------------------------------
                                                                                There are No Book Available 
                                                -------------------------------------------------------------------------------------                         
              """)
        


def favorite():
    while True:
        print("""                            
                                                -------------------------------------------------------------------------------------
                                                                                       FAVORITE
                                                -------------------------------------------------------------------------------------

                                                Choose the option you want to:
                                                
                                                1. View favorite books
                                                2. Add to favorite 
                                                3. Remove from favorites
                                                4. Go Back                       
              """)
        choice = input("Enter a number from the above list: ")
        if choice == "1":
            viewfavorite()
        elif choice == "2":
            addfavorite()
        elif choice == "3":
            removefavorite()
        elif choice == "4":
            return
        else:
            print("INVALID!!! Choose options from 1 to 4 only.")

def viewfavorite():
    global UserName
    query = '''
    SELECT f.FavouriteID, b.BookID,b.Title,b.Details,a.AuthorName,g.GenreName,b.Coins, b.Ratings FROM Favourite f
    INNER JOIN Book b ON f.BookID = b.BookID INNER JOIN Author a ON b.AuthorID = a.AuthorID INNER JOIN Genre g ON b.GenreID = g.GenreID
    WHERE f.UserName=%s;
    '''
    login.execute(query, (UserName,))
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result,
                       headers=["FavouriteID", "BookID", "Title", "Details", "AuthorName", "GenreName", "Coins","Ratings"]))
    else:
        print("""                            
                                                -------------------------------------------------------------------------------------
                                                                                No Book Favorite's Till Now.
                                                -------------------------------------------------------------------------------------                         
              """)
        


def addfavorite():
    global UserName
    query = 'SELECT b.BookID, b.Title, b.Details, a.AuthorName, g.GenreName, b.Coins, b.Ratings FROM Book b INNER JOIN Author a ON b.AuthorID = a.AuthorID INNER JOIN Genre g ON b.GenreID = g.GenreID'
    login.execute(query)
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result,
                       headers=["BookID", "Title", "Details", "AuthorName", "GenreName", "Coins", "Ratings"]))
        
        while True:
            try:
                BookID = int(input("\nEnter the BookID of the book you want to add to your favorites: "))
                selected_book = next((book for book in query_result if book[0] == BookID), None)
                if selected_book:
                    insert_query = "INSERT INTO Favourite (BookID, Coins,UserName) VALUES (%s, %s, %s)"
                    login.execute(insert_query, (BookID, selected_book[5],UserName))
                    databaseobj.commit()
                    print(f"""                            
                                                -------------------------------------------------------------------------------------
                                                                Book '{selected_book[1]}' has been added to your favorites.
                                                -------------------------------------------------------------------------------------                         
                                  """)
                    
                    break
                else:
                    print("Invalid BookID. Please enter a valid BookID.")
            except ValueError:
                print("Invalid input. Please enter a numeric BookID.")
    else:
        print("""                            
                                                -------------------------------------------------------------------------------------
                                                                                  There are No Book Available 
                                                -------------------------------------------------------------------------------------                         
                      """)


def removefavorite():
    global UserName
    query = '''
        SELECT f.FavouriteID, b.BookID, b.Title, b.Details, a.AuthorName, g.GenreName, b.Coins, b.Ratings 
        FROM Favourite f
        INNER JOIN Book b ON f.BookID = b.BookID 
        INNER JOIN Author a ON b.AuthorID = a.AuthorID 
        INNER JOIN Genre g ON b.GenreID = g.GenreID
        WHERE f.UserName = %s;
    '''
    login.execute(query, (UserName,))
    query_result = login.fetchall()

    if query_result:
        print(tabulate(query_result,
                       headers=["FavouriteID", "BookID", "Title", "Details", "AuthorName", "GenreName", "Coins",
                                "Ratings"]))
        while True:
            FavouriteID = input("\nEnter the FavouriteID of the book you want to remove from your favorites: ")
            if FavouriteID.isdigit():
                FavouriteID = int(FavouriteID)
                selected_favorite = next((fav for fav in query_result if fav[0] == FavouriteID), None)
                if selected_favorite:
                    delete_query = "DELETE FROM Favourite WHERE FavouriteID = %s AND UserName = %s"
                    login.execute(delete_query, (FavouriteID, UserName))
                    databaseobj.commit()
                    print(f"""                            
                                                    -------------------------------------------------------------------------------------
                                                                Book '{selected_favorite[2]}' has been removed from your favorites.
                                                    -------------------------------------------------------------------------------------                         
                           """)
                    break
                else:
                    print("Invalid FavouriteID. Please enter a valid FavouriteID.")
            else:
                print("Invalid input. Please enter a numeric FavouriteID.")
    else:
        print("""                            
                                                -------------------------------------------------------------------------------------
                                                                                  No Book Favorites Till Now.
                                                -------------------------------------------------------------------------------------                       
                  """)


def rent():
    while True:
        print("""                            
                                                -------------------------------------------------------------------------------------
                                                                                       RENT
                                                -------------------------------------------------------------------------------------

                                                Choose the option you want to:
                    
                                                1. View Rented Books
                                                2. Add to Rented Books
                                                3. Go Back                       
              """)
        choice = input("Enter a number from the above list: ")
        if choice == "1":
            viewrentbook()
        elif choice == "2":
            rentbook()
        elif choice == "3":
            return
        else:
            print("INVALID!!! Choose options from 1 to 3 only.")

def viewrentbook():
    try:
        global UserName
        query = """
        SELECT R.BookID, B.Title, R.StartDate, R.EndDate FROM Rented R JOIN Book B ON R.BookID = B.BookID
        WHERE R.UserName = %s
        """
        login.execute(query, (UserName,))
        rented_books = login.fetchall()

        if rented_books:
            print(tabulate(rented_books, headers=["BookID", "BookName", "StartDate", "EndDate"]))
        else:
            print("""                            
                                                -------------------------------------------------------------------------------------
                                                                                No Book Rented Till Now
                                                -------------------------------------------------------------------------------------
            """)
            
    except Exception as e:
        print(f"An error occurred: {e}")


def rentbook():
    try:
        viewbookuser()
        BookID = input("Enter the BookID to rent: ")
        DaysRented = int(input("Enter the number of days you want to rent the book: "))

        print("""                              
                                                -------------------------------------------------------------------------------------
                                                                              CHOOSE YOUR PAYMENT METHOD
                                                -------------------------------------------------------------------------------------    

                                                ->Choose an option to continue:

                                                1. Card
                                                2. UPI
                                                3. QR Code
                                                4. Cancel
                                                5. Homepage
                                    """)

        option = input("Enter Your Payment Method: ")
        if option == "1":
            payment_method = "Card"
        elif option == "2":
            payment_method = "UPI"
        elif option == "3":
            payment_method = "QR Code"
        elif option == "4":
            return  # Cancel and return to the previous menu
        elif option == "5":
            optionpageuser()  # Go to homepage
            return
        else:
            print("Invalid option selected!")
            return

        login.execute("SELECT Coins FROM Book WHERE BookID = %s", (BookID,))
        result = login.fetchone()
        if result:
            cost_per_day = result[0]
            rental_cost = cost_per_day * DaysRented
        else:
            print("INVALID!!! BookID does not exist. Please try again.")
            return

        login.execute("SELECT BalanceID FROM Balance WHERE UserName = %s", (UserName,))
        balance_result = login.fetchone()
        if balance_result:
            BalanceID = balance_result[0]
        else:
            print("Error retrieving BalanceID. Please try again.")
            return

        login.execute("SELECT Coins FROM Balance WHERE BalanceID = %s", (BalanceID,))
        balance = login.fetchone()
        if balance and balance[0] >= rental_cost:
            login.execute("UPDATE Balance SET Coins = Coins - %s WHERE BalanceID = %s", (rental_cost, BalanceID))
            Date_and_Time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            login.execute("SELECT EndDate FROM Rented WHERE BookID = %s AND UserName = %s", (BookID, UserName))
            rented_record = login.fetchone()

            if rented_record:
                existing_end_date = datetime.datetime.strptime(rented_record[0], "%Y-%m-%d")
                new_end_date = (existing_end_date + datetime.timedelta(days=DaysRented)).strftime("%Y-%m-%d")
                login.execute("UPDATE Rented SET EndDate = %s WHERE BookID = %s AND UserName = %s",
                              (new_end_date, BookID, UserName))
            else:
                end_date = (datetime.datetime.now() + datetime.timedelta(days=DaysRented)).strftime("%Y-%m-%d")
                insert_rented = (
                    "INSERT INTO Rented (BookID, UserName, StartDate, EndDate) "
                    "VALUES (%s, %s, %s, %s)"
                )
                login.execute(insert_rented, (BookID, UserName, datetime.datetime.now().strftime("%Y-%m-%d"), end_date))

            insert_rental_payment = (
                "INSERT INTO Payment (Cost, BookID, BalanceID, PaymentFor, ModeOfPayment, Date_and_Time) "
                "VALUES (%s, %s, %s, %s, %s, %s)"
            )
            login.execute(insert_rental_payment,
                          (rental_cost, BookID, BalanceID, 'Book Rental', payment_method, Date_and_Time))
            databaseobj.commit()
            print("""                            
                                                -------------------------------------------------------------------------------------
                                                                              Book rented successfully!
                                                -------------------------------------------------------------------------------------
                        """)

        else:
            print(f"""                            
                                                -------------------------------------------------------------------------------------
                                                                  INSUFFICIENT COINS!!! Please recharge your account.
                                                -------------------------------------------------------------------------------------

                                                Amount Needed to rent Book :{rental_cost - balance[0]}
                                                Choose the option you want to:

                                                1. Recharge
                                                2. Go Back 
                                    """)

            choice = input("Enter a number from the above list: ")
            if choice == "1":
                recharge()
            elif choice == "2":
                return
            else:
                print("INVALID!!! Choose options from 1/2 only")
    except Exception as e:
        print(f"An error occurred: {e}")
        databaseobj.rollback()


def userfeedback():
    while True:
        print("""                            
                                                -------------------------------------------------------------------------------------
                                                                                        FEEDBACK
                                                -------------------------------------------------------------------------------------

                                                Choose the option you want to:
                                                      
                                                1. View Feedback
                                                2. Add New Feedback
                                                3. Go Back                       
              """)
        choice = input("Enter a number from the above list: ")
        if choice == "1":
            viewfeedback()
        elif choice == "2":
            addfeedback()
        elif choice == "3":
            return
        else:
            print("INVALID!!! Choose options from 1 to 7 only.")

def viewfeedback():
    query = 'SELECT FeedbackID,Feedback,Response FROM Feedback where UserName=%s'
    login.execute(query,(UserName,))
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result,
                       headers=["FeedbackID","Feedback","Response"]))
        
    else:
        print("""                            
                                                -------------------------------------------------------------------------------------
                                                                              Your Feedback List is empty.
                                                -------------------------------------------------------------------------------------                        
              """)
        
def addfeedback():
    global UserName
    Feedback = input("Enter Feedback: ")
    Response = "Not Yet Responded"
    insert_query = "INSERT INTO Feedback(Feedback,Response,UserName) VALUES (%s,%s,%s)"
    login.execute(insert_query, (Feedback,Response,UserName))
    databaseobj.commit()
    print("""                            
                                                -------------------------------------------------------------------------------------
                                                                                You have added a Feedback!!!
                                                -------------------------------------------------------------------------------------                         
          """)
    

def accounts():
    while True:
        print("""                            
                                                -------------------------------------------------------------------------------------
                                                                                           ACCOUNT
                                                -------------------------------------------------------------------------------------

                                                Choose the option you want to:
                    
                                                1. View Balance
                                                2. Recharge Account
                                                3. View Profile Details
                                                4. Edit Profile
                                                5. My Payments
                                                6. Go Back                       
              """)
        choice = input("Enter a number from the above list: ")
        if choice == "1":
            balance()
        elif choice == "2":
            recharge()
        elif choice == "3":
            viewuser()
        elif choice == "4":
            updateuser()
        elif choice == "5":
            userpayment()
        elif choice == "6":
            return
        else:
            print("INVALID!!! Choose options from 1 to 6 only.")
def balance():
    try:
        global UserName
        login.execute("SELECT PlanID FROM UserInfo WHERE UserName = %s", (UserName,))
        plan_info = login.fetchone()
        if plan_info:
            PlanID = plan_info[0]
        else:
            print("No plan associated with the provided UserName.")
            return
        login.execute("SELECT Coins FROM Balance WHERE UserName = %s AND PlanID = %s", (UserName, PlanID))
        balance_info = login.fetchone()
        if balance_info:
            Coins = balance_info[0]
            print(f"""                            
                                                -------------------------------------------------------------------------------------
                                                                        Your current balance is: {Coins:.2f} coins
                                                -------------------------------------------------------------------------------------                         
                      """)
            
        else:
            print("No balance found for the provided UserName.")

    except Exception as e:
        print(f"An error occurred: {e}")

def recharge():
    try:
        Amount = float(input("Enter the amount to recharge: "))
        if Amount > 0:
            print("""                              
                                                -------------------------------------------------------------------------------------
                                                                               CHOOSE YOUR PAYMENT METHOD
                                                -------------------------------------------------------------------------------------    

                                                ->Choose an option to continue :

                                                1. Card
                                                2. UPI
                                                3. QR Code
                                                4. Cancel
                                                5. Homepage
                                        """)

            option = input("Enter Your Payment Method: ")
            if option == "1":
                payment_method = "Card"
            elif option == "2":
                payment_method = "UPI"
            elif option == "3":
                payment_method = "QR Code"
            elif option == "4":
                recharge()
                return
            elif option == "5":
                startpage()
                return
            else:
                print("Invalid option selected!")
                return

            print("""                          
                                                -------------------------------------------------------------------------------------
                                                                             PAYMENT SUCCESSFUL!!!
                                                -------------------------------------------------------------------------------------                       
                                            """)
            
        else:
            print("INVALID!!! Recharge amount must be greater than zero.")
            return

        login.execute("SELECT BalanceID FROM Balance WHERE UserName = %s", (UserName,))
        balance_result = login.fetchone()
        if balance_result:
            BalanceID = balance_result[0]
        else:
            print("Error retrieving BalanceID. Please try again.")
            return

        Date_and_Time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        insert_recharge_payment = (
            "INSERT INTO Payment (Cost, BalanceID, PaymentFor, ModeOfPayment, Date_and_Time) "
            "VALUES (%s, %s, %s, %s, %s)"
        )
        login.execute(insert_recharge_payment, (Amount, BalanceID, 'Recharge', payment_method, Date_and_Time))

        login.execute("UPDATE Balance SET Coins = Coins + %s WHERE BalanceID = %s", (Amount, BalanceID))
        databaseobj.commit()

        print(f"""                            
                                                -------------------------------------------------------------------------------------
                                                                                    Recharge successful!
                                                -------------------------------------------------------------------------------------                         
                              """)
        
    except Exception as e:
        print(f"An error occurred: {e}")


def viewuser():
    global UserName
    query = 'SELECT UserName,Password,FirstName,LastName,MobileNumber,Email,PlanID FROM UserInfo WHERE UserName=%s'
    login.execute(query,(UserName,))
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result,
                       headers=["UserName","Password", "FirstName", "LastName", "MobileNumber", "Email", "PlanID"]))
        
    else:
        print("""                            
                                                -------------------------------------------------------------------------------------
                                                                                     The User Info is Blank
                                                -------------------------------------------------------------------------------------                         
              """)
        



def updateuser():
    global UserName
    query = 'SELECT FirstName,LastName,MobileNumber,Email,PlanID FROM UserInfo WHERE UserName=%s;'
    login.execute(query,(UserName,))
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result, headers=["FirstName", "LastName", "MobileNumber", "Email","PlanID"]))
        query = "SELECT FirstName,LastName,MobileNumber,Email FROM UserInfo WHERE UserName=%s;"
        login.execute(query, (UserName,))
        result = login.fetchone()
        if result is None:
            print("INVALID!!!")
        else:
            print("Profile Details: ")
            while True:
                print("""
                Choose an option you want to update:
                1. FirstName
                2. LastName
                3. MobileNumber
                4. Email
                5. Go back
                """)
                choice = input("Enter a number from the above list: ")
                if choice == "1":
                    new_FirstName = input("Enter FirstName: ")
                    if re.fullmatch("[A-Za-z]{3,25}", new_FirstName):
                        update_user_detail("FirstName", new_FirstName, UserName)
                    else:
                        print("FirstName must only have alphabets of length 3 to 25.")
                elif choice == "2":
                    new_LastName = input("Enter LastName: ")
                    if re.fullmatch("[A-Za-z]{1,25}", new_LastName):
                        update_user_detail("LastName", new_LastName, UserName)
                    else:
                        print("LastName must only have alphabets and have atleast 1 character")
                elif choice == "3":
                    new_MobileNumber = input("Enter MobileNumber: ")
                    if len(new_MobileNumber) == 10 and new_MobileNumber.isdigit() and new_MobileNumber[0] in '6789':
                        update_user_detail("MobileNumber", new_MobileNumber, UserName)
                    else:
                        print("PhoneNumber must be a 10-digit number which should start with 9, 8, 7, 6.")
                elif choice == "4":
                    new_Email = input("Enter the Email: ")
                    if re.fullmatch(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", new_Email):
                        update_user_detail("Email", new_Email, UserName)
                    else:
                        print("Invalid Email address! Please enter a valid email.")
                elif choice == "5":
                    break
                else:
                    print("INVALID!!! Enter numbers from 1 to 5 only.")
    else:
        print("""                            
                                                -------------------------------------------------------------------------------------
                                                                                The User Info is Blank
                                                -------------------------------------------------------------------------------------                         
                      """)
        


def update_user_detail(field_name, new_value, UserName):
    query = f"UPDATE UserInfo SET {field_name}=%s WHERE UserName=%s"
    login.execute(query, (new_value, UserName))
    databaseobj.commit()
    print(f"""                            
                                                ------------------------------------------------------------------------------------- 
                                                                    You have successfully updated your {field_name}.!!!
                                                -------------------------------------------------------------------------------------                         
         """)


def userpayment():
    global UserName
    query = """
        SELECT p.PaymentID, p.Cost, p.ModeOfPayment, p.PaymentFor, p.Date_and_Time FROM Payment p
        JOIN Balance b ON p.BalanceID = b.BalanceID JOIN UserInfo u ON b.UserName = u.UserName
        WHERE u.UserName = %s ;
    """
    login.execute(query, (UserName,))
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result,
                       headers=["PaymentID", "Cost", "ModeOfPayment","PaymentFor","Date_and_Time"]))

    else:
        print("""                           
                                                -------------------------------------------------------------------------------------
                                                                                   No Payment has been done !!  
                                                -------------------------------------------------------------------------------------                       
         """)


def loginpageadmin():
    global UserName
    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        print("Hello Admin")
        UserName = input("Enter UserName: ")
        if UserName == "":
            print("This field cannot be empty.")
            attempts += 1
            remaining_attempts = max_attempts - attempts
            if remaining_attempts == 0:
                print("You have been logged out due to too many failed login attempts.")
                return
            print(f"You have {remaining_attempts} attempts left.")
            continue

        Password = input("Enter the password: ")
        if Password == "":
            print("This field cannot be empty.")
            attempts += 1
            remaining_attempts = max_attempts - attempts
            if remaining_attempts == 0:
                print("You have been logged out due to too many failed login attempts.")
                return
            print(f"You have {remaining_attempts} attempts left.")
            continue

        select_query = "SELECT * FROM Login WHERE UserName=%s COLLATE utf8mb4_bin AND Password=%s COLLATE utf8mb4_bin"
        login.execute(select_query, (UserName, Password))
        result = login.fetchone()

        if result is not None:
            print("""                            
                                                ------------------------------------------------------------------------------------- 
                                                                            You have Logged in successful!!!
                                                -------------------------------------------------------------------------------------                        
                              """)
            
            optionpageadmin()
            return
        else:
            attempts += 1
            remaining_attempts = max_attempts - attempts
            if remaining_attempts <= 0:
                print("You have been logged out due to too many failed login attempts.")
                exit()
            else:
                print(f"Incorrect UserName or Password. You have {remaining_attempts} attempts left.")



def optionpageadmin():
    global UserName
    while True:
        print(f"""                              
                                                ------------------------------------------------------------------------------------- 
                                                                                WELCOME ADMIN {UserName}
                                                -------------------------------------------------------------------------------------  
                                                                        
                                                ->Choose an option to continue :
                                                
                                                1. Books
                                                2. Users
                                                3. Genre
                                                4. Author
                                                5. Plan
                                                6. Feedback 
                                                7. Payments
                                                8. Log out
        """)
        option = input("Choose an option [1 to 8]: ")
        if option == "1":
            book()
        elif option == "2":
            users()
        elif option == "3":
            genre()
        elif option == "4":
            author()
        elif option == "5":
            plan()
        elif option == "6":
            feedback()
        elif option == "7":
            payments()
        elif option == "8":
            print("""                           
                                                -------------------------------------------------------------------------------------
                                                                  You have successfully logged out... Have a nice day!!!
                                                -------------------------------------------------------------------------------------                       
                  """)
            
            startpage()
        else:
            print("INVALID!!! Choose options from 1 to 8 only.")


def book():
    print("""                                  
                                                -------------------------------------------------------------------------------------
                                                                                        BOOK
                                                -------------------------------------------------------------------------------------      
                                                                 
                                                Choose the option you want to:
                                                
                                                1. Add
                                                2. Edit
                                                3. View
                                                4. Delete
                                                5. Search
                                                6. Go Back
          """)
    choice = input("Enter an option: ")
    if choice == "1":
        addbook()
    elif choice == "2":
        updatebook()
    elif choice == "3":
        viewbookadmin()
    elif choice == "4":
        deletebook()
    elif choice == "5":
        print("""    
                                                ---------------------What Book Are You Looking For...  Search By--------------------- 
                                               
                                                1. Author
                                                2. Title
                                                3. Go Back

                        """)
        option = input("Choose an option [1 to 7]: ")
        if option == "1":
            search_by_author()
        elif option == "2":
            search_by_title()
        elif option == "3":
            optionpageadmin()
    elif choice == "6":
        return
    else:
        print("INVALID!!! Enter numbers from 1-4")


def viewbookadmin():
    query = 'SELECT b.BookID,b.Title,b.Details,a.AuthorID,a.AuthorName,g.GenreID,g.GenreName,b.Coins,b.Ratings FROM Book b INNER JOIN Author a ON b.AuthorID = a.AuthorID INNER JOIN Genre g ON b.GenreID = g.GenreID'
    login.execute(query)
    query_result = login.fetchall()
    if query_result:
        wrapped_result = []
        for row in query_result:
            adjusted_row = list(row)
            adjusted_row[2] = "\n".join(textwrap.wrap(adjusted_row[2], width=75))
            wrapped_result.append(adjusted_row)
            wrapped_result.append([""] * len(row))
        print(tabulate(wrapped_result,
                       headers=["BookID","Title", "Details", "AuthorID", "AuthorName", "GenreID", "GenreName", "Coins", "Ratings"]))
        
    else:
        print("""                            
                                                -------------------------------------------------------------------------------------
                                                                               There are No Book Available 
                                                -------------------------------------------------------------------------------------                         
              """)
        

def addbook():
    while True:
        Title = input("Enter Book Title: ")
        if len(Title) >= 3:
            break
        else:
            print("Title must have atleast 3 characters")
    while True:
        Details = input("Enter Book Details: ")
        break
    while True:
        viewauthor()
        AuthorID = input("Enter the AuthorID: ")
        if len(AuthorID) <= 3:
            break
        else:
            print("AuthorID cannot be empty!!!")
    while True:
        viewgenre()
        GenreID = input("Enter the GenreID: ")
        if  len(GenreID) <= 3:
            break
        else:
            print("GenreID cannot be empty!!!")
    while True:
        Coins = input("Enter the Coin Value: ")
        if  len(Coins) <= 3:
            break
        else:
            print("Coin Value cannot be empty!!!")
    while True:
        Ratings = input("Enter the Ratings: ")
        if len(Ratings) <= 2:
            break
        else:
            print("Coin Value cannot be empty!!!")

    insert_query = "INSERT INTO Book(Title, Details, AuthorID, GenreID, Coins, Ratings) VALUES (%s, %s, %s, %s, %s, %s)"
    login.execute(insert_query, (Title, Details, int(AuthorID), int(GenreID), int(Coins), float(Ratings)))
    databaseobj.commit()
    print("""                           
                                                -------------------------------------------------------------------------------------
                                                                              You have successfully added a Book!!! 
                                                -------------------------------------------------------------------------------------                       
          """)
    
    book()





def updatebook():
    global BookID
    query = 'SELECT * FROM Book'
    login.execute(query)
    query_result = login.fetchall()


    if query_result:
        wrapped_result = []
        for row in query_result:
            adjusted_row = list(row)

            if isinstance(adjusted_row[2], str):
                adjusted_row[2] = "\n".join(textwrap.wrap(adjusted_row[2], width=50))

            wrapped_result.append(adjusted_row)
            wrapped_result.append([""] * len(row))

        print(tabulate(wrapped_result,
                       headers=["BookID", "Title", "Details", "AuthorID", "AuthorName", "GenreID", "GenreName", "Coins",
                                "Ratings"]))

        while True:
            BookID = input("Enter the BookID to be edited: ")
            if BookID.isdigit():
                break
            else:
                print("BookID must be a number.")

        query = "SELECT * FROM Book WHERE BookID=%s"
        login.execute(query, (BookID,))
        result = login.fetchone()

        if result is None:
            print("INVALID!!! BookID does not exist...Enter a valid BookID")
        else:
            print("Details for the selected BookID are:")
            print(
                f"BookID: {result[0]}\nTitle: {result[1]}\nDetails: {result[2]}\nAuthorID: {result[3]}\nGenreID: {result[4]}\nCoins: {result[5]}\nRatings: {result[6]}")

            while True:
                print("""
                Choose an option you want to update:
                1. Title
                2. Details
                3. AuthorID
                4. GenreID
                5. Coins
                6. Ratings
                7. Go back
                """)
                choice = input("Enter a number from the above list: ")

                if choice == "1":
                    new_Title = input("Enter New Title: ")
                    if len(new_Title) >= 3:
                        update_book_detail("Title", new_Title, BookID)
                        break
                    else:
                        print("Title must have at least 3 characters.")

                elif choice == "2":
                    new_Details = input("Enter New Details: ")
                    update_book_detail("Details", new_Details, BookID)
                    break

                elif choice == "3":
                    viewauthor()
                    new_AuthorID = input("Enter New AuthorID: ")
                    if new_AuthorID.isdigit():
                        update_book_detail("AuthorID", new_AuthorID, BookID)
                        break
                    else:
                        print("AuthorID must be a valid number.")

                elif choice == "4":
                    viewgenre()
                    new_GenreID = input("Enter New GenreID: ")
                    if new_GenreID.isdigit():
                        update_book_detail("GenreID", new_GenreID, BookID)
                        break
                    else:
                        print("GenreID must be a valid number.")

                elif choice == "5":
                    new_Coins = input("Enter New Coin Value: ")
                    if new_Coins.isdigit() and 0 <= int(new_Coins) <= 999:
                        update_book_detail("Coins", new_Coins, BookID)
                        break
                    else:
                        print("Coins must be a valid number between 0 and 999.")

                elif choice == "6":
                    new_Ratings = input("Enter New Ratings (0.0 - 10.0): ")
                    try:
                        new_Ratings = float(new_Ratings)
                        if 0.0 <= new_Ratings <= 10.0:
                            update_book_detail("Ratings", new_Ratings, BookID)
                            break
                        else:
                            print("Ratings must be a valid number between 0.0 and 10.0.")
                    except ValueError:
                        print("Ratings must be a floating-point number.")

                elif choice == "7":
                    break

                else:
                    print("INVALID!!! Enter numbers from 1 to 7 only.")
    else:
        print("""                           
                                                -------------------------------------------------------------------------------------
                                                                              There are No Books Available  
                                                -------------------------------------------------------------------------------------                       
                                  """)

    book()


def update_book_detail(field_name, new_value, BookID):
    query = f"UPDATE Book SET {field_name}=%s WHERE BookID=%s"
    login.execute(query, (new_value, BookID))
    databaseobj.commit()
    print(f"""                           
                                                -------------------------------------------------------------------------------------
                                                                     You have successfully updated the {field_name}.!!!  
                                                -------------------------------------------------------------------------------------                       
          """)

    book()



def deletebook():
    query = 'SELECT * FROM Book'
    login.execute(query)
    query_result = login.fetchall()

    if query_result:
        print(tabulate(query_result, headers=["BookID", "Title", "Details", "AuthorID", "GenreID", "Coins", "Ratings"]))

        while True:
            BookID = input("Enter the BookID to be deleted: ")
            if BookID.isdigit():
                query = "SELECT * FROM Book WHERE BookID=%s"
                login.execute(query, (BookID,))
                result = login.fetchone()

                if result is None:
                    print("BookID does not exist.")
                else:
                    print(
                        f"\nBook Details:\nBookID: {result[0]}\nTitle: {result[1]}\nDetails: {result[2]}\nAuthorID: {result[3]}\nGenreID: {result[4]}\nCoins: {result[5]}\nRatings: {result[6]}")

                    # Check if the book is referenced in the Payment table
                    query = "SELECT * FROM Payment WHERE BookID=%s"
                    login.execute(query, (BookID,))
                    payment_result = login.fetchone()

                    if payment_result:
                        print("This book has associated payment records and cannot be deleted.")
                    else:
                        while True:
                            print("""
                            Are you sure you want to delete this Book?
                            1. Yes
                            2. No
                            """)
                            choice = input("Enter an option from above choice: ")
                            if choice == "1":
                                query = "DELETE FROM Book WHERE BookID=%s"
                                login.execute(query, (BookID,))
                                databaseobj.commit()
                                print("""                           
                                                    -------------------------------------------------------------------------------------
                                                                            You have deleted a Book successfully!!  
                                                    -------------------------------------------------------------------------------------                       
                                        """)
                                break
                            elif choice == "2":
                                break
                            else:
                                print("INVALID!!! Enter an option from above [1 or 2].")
                break
            else:
                print("BookID must be a number.")
    else:
        print("""                           
                                                -------------------------------------------------------------------------------------
                                                                                There are No Books Available   
                                                -------------------------------------------------------------------------------------                       
              """)

    book()


def search_by_author():
    search_author = input("Enter the Author to search: ")
    query = ('SELECT b.BookID, b.Title, b.Details, a.AuthorID, a.AuthorName, g.GenreID, g.GenreName, b.Coins, b.Ratings '
             'FROM Book b '
             'INNER JOIN Author a ON b.AuthorID = a.AuthorID '
             'INNER JOIN Genre g ON b.GenreID = g.GenreID '
             'WHERE a.AuthorName LIKE %s')
    login.execute(query, ('%' + search_author + '%',))
    query_result = login.fetchall()
    if query_result:
        print("""                           
                                               -------------------------------------------------------------------------------------
                                                                              Book found with that Author !!  
                                               -------------------------------------------------------------------------------------                       
                      """)
        print(tabulate(query_result, headers=["BookID", "Title", "Details", "AuthorID", "AuthorName", "GenreID", "GenreName", "Coins", "Ratings"]))
        
    else:
        print("""                           
                                               -------------------------------------------------------------------------------------
                                                                              No Book found with that Author !!  
                                               -------------------------------------------------------------------------------------                       
          """)
        
    book()
def search_by_title():
    search_title = input("Enter the title to search: ")
    query = ('SELECT b.BookID, b.Title, b.Details, a.AuthorID, a.AuthorName, g.GenreID, g.GenreName, b.Coins, b.Ratings '
             'FROM Book b '
             'INNER JOIN Author a ON b.AuthorID = a.AuthorID '
             'INNER JOIN Genre g ON b.GenreID = g.GenreID '
             'WHERE b.Title LIKE %s')

    login.execute(query, ('%' + search_title + '%',))
    query_result = login.fetchall()
    if query_result:
        print("""                           
                                               -------------------------------------------------------------------------------------
                                                                            Book found with that Title !!  
                                               -------------------------------------------------------------------------------------                       
                  """)
        print(tabulate(query_result, headers=["BookID", "Title", "Details", "AuthorID", "AuthorName", "GenreID", "GenreName", "Coins", "Ratings"]))
        
    else:
        print("""                           
                                               -------------------------------------------------------------------------------------
                                                                           No Book found with that Title !!  
                                               -------------------------------------------------------------------------------------                       
                          """)
        
    book()

def users():
    query = 'SELECT * FROM UserInfo'
    login.execute(query)
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result,
                       headers=["UserName","Password", "FirstName", "LastName", "MobileNumber", "Email", "PlanID", "Date_and_Time"]))
        
    else:
        print("""                           
                                               -------------------------------------------------------------------------------------
                                                                                  No User has registered !!  
                                               -------------------------------------------------------------------------------------                       
               """)
        

def genre():
    print("""                            
                                                -------------------------------------------------------------------------------------
                                                                                          GENRE
                                                -------------------------------------------------------------------------------------                        
                   
                                                Choose the option you want to:
                                                 
                                                1. Add
                                                2. Edit
                                                3. View
                                                4. Go Back
          """)
    choice = input("Enter an option: ")
    if choice == "1":
        addgenre()
    elif choice == "2":
        updategenre()
    elif choice == "3":
        viewgenre()
    elif choice == "4":
        return
    else:
        print("INVALID!!! Enter numbers from 1-4")


def viewgenre():
    query = 'SELECT * FROM Genre'
    login.execute(query)
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result,
                       headers=["GenreID","GenreName"]))
        
    else:
        print("""                           
                                                -------------------------------------------------------------------------------------
                                                                              No Genre has been added !!  
                                                -------------------------------------------------------------------------------------                       
                """)
        

def addgenre():
    while True:
        GenreID = input("Enter GenreID: ")
        if len(GenreID) <= 3:
            break
        else:
            print("GenreID must have atleast 3 characters")
    while True:
        GenreName = input("Enter GenreName: ")
        if len(GenreName) >= 3:
            break
        else:
            print("GenreName must have atleast 3 characters")
    insert_query = "INSERT INTO Genre VALUES (%s,%s)"
    login.execute(insert_query, (int(GenreID),GenreName))
    databaseobj.commit()
    print("""                           
                                                 -------------------------------------------------------------------------------------
                                                                         You have successfully added a Genre!!! 
                                                 -------------------------------------------------------------------------------------                       
                    """)
    
    genre()

def updategenre():
    global GenreID
    query = 'SELECT * FROM Genre'
    login.execute(query)
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result, headers=["GenreID", "GenreName"]))
        while True:
            GenreID = input("Enter the GenreID to be edited: ")
            if GenreID.isdigit():
                break
            else:
                print("GenreID must be a number.")
        query = "SELECT * FROM Genre WHERE GenreID=%s"
        login.execute(query, (GenreID,))
        result = login.fetchone()
        if result is None:
            print("INVALID!!! GenreID does not exist...Enter a valid GenreID")
        else:
            print("Details for the selected GenreID are: ")
            print("GenreID:", result[0], "\nGenreName:", result[1])
            while True:
                print("""
                Choose an option you want to update:
                1. GenreName
                2. Go back
                """)
                choice = input("Enter a number from the above list: ")
                if choice == "1":
                    new_GenreName = input("Enter New GenreName: ")
                    if len(new_GenreName) >= 3:
                        query = f"UPDATE Genre SET GenreName=%s WHERE GenreID=%s"
                        login.execute(query, (new_GenreName, GenreID))
                        databaseobj.commit()
                        print("""                           
                                                 -------------------------------------------------------------------------------------
                                                                      You have successfully updated the GenreName.!!! 
                                                 -------------------------------------------------------------------------------------                       
                                        """)
                        
                    else:
                        print("GenreName must have atleast 3 characters")
                elif choice == "2":
                    break
                else:
                    print("INVALID!!! Enter numbers from 1/2")
    else:
        print("""                           
                                                -------------------------------------------------------------------------------------
                                                                                    No Genre has been added !!  
                                                -------------------------------------------------------------------------------------                       
                        """)
        
    genre()


def author():
    print("""                            
                                                -------------------------------------------------------------------------------------
                                                                                             AUTHOR
                                                -------------------------------------------------------------------------------------                        

                                                Choose the option you want to:
                                                 
                                                1. Add
                                                2. Edit
                                                3. View
                                                4. Go Back
          """)
    choice = input("Enter an option: ")
    if choice == "1":
        addauthor()
    elif choice == "2":
        updateauthor()
    elif choice == "3":
        viewauthor()
    elif choice == "4":
        return
    else:
        print("INVALID!!! Enter numbers from 1-4")

def viewauthor():
    query = 'SELECT * FROM Author'
    login.execute(query)
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result,
                       headers=["AuthorID","AuthorName"]))
        
    else:
        print("""                           
                                                 -------------------------------------------------------------------------------------
                                                                                No Author has been added !!  
                                                 -------------------------------------------------------------------------------------                       
                  """)
        

def addauthor():
    while True:
        AuthorID = input("Enter AuthorID: ")
        if len(AuthorID) <= 3:
            break
        else:
            print("AuthorID must have atleast 3 characters")
    while True:
        AuthorName = input("Enter AuthorName: ")
        if len(AuthorName) >= 3:
            break
        else:
            print("AuthorName must have atleast 3 characters")
    insert_query = "INSERT INTO Author VALUES (%s,%s)"
    login.execute(insert_query, (int(AuthorID),AuthorName))
    databaseobj.commit()
    print("""                           
                                                 -------------------------------------------------------------------------------------
                                                                       You have successfully added an Author!!!  
                                                 -------------------------------------------------------------------------------------                       
                      """)
    
    author()

def updateauthor():
    global AuthorID
    query = 'SELECT * FROM Author'
    login.execute(query)
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result, headers=["AuthorID", "AuthorName"]))
        while True:
            AuthorID = input("Enter the AuthorID to be edited: ")
            if AuthorID.isdigit():
                break
            else:
                print("AuthorID must be a number.")
        query = "SELECT * FROM Author WHERE AuthorID=%s"
        login.execute(query, (AuthorID,))
        result = login.fetchone()
        if result is None:
            print("INVALID!!! AuthorID does not exist...Enter a valid AuthorID")
        else:
            print("Details for the selected AuthorID are: ")
            print("AuthorID:", result[0], "\nAuthorName:", result[1])
            while True:
                print("""
                Choose an option you want to update:
                1. AuthorName
                2. Go back
                """)
                choice = input("Enter a number from the above list: ")
                if choice == "1":
                    new_AuthorName = input("Enter New AuthorName: ")
                    if len(new_AuthorName) >= 3:
                        query = f"UPDATE Author SET AuthorName=%s WHERE AuthorID=%s"
                        login.execute(query, (new_AuthorName, AuthorID))
                        databaseobj.commit()
                        print("""                           
                                               -------------------------------------------------------------------------------------
                                                                     You have successfully updated the AuthorName.!!!
                                               -------------------------------------------------------------------------------------                       
                                """)
                        
                    else:
                        print("AuthorName must have atleast 3 characters")
                elif choice == "2":
                    break
                else:
                    print("INVALID!!! Enter numbers from 1/2")
    else:
        print("""                           
                                               -------------------------------------------------------------------------------------
                                                                          No Author has been added !!  
                                               -------------------------------------------------------------------------------------                       
                          """)
        
    author()

def plan():
    print("""                            
                                                -------------------------------------------------------------------------------------
                                                                                        PLAN
                                                -------------------------------------------------------------------------------------                       

                                                Choose the option you want to:
                                                 
                                                1. Add
                                                2. Edit
                                                3. View
                                                4. Go Back
          """)
    choice = input("Enter an option: ")
    if choice == "1":
        addplan()
    elif choice == "2":
        updateplan()
    elif choice == "3":
        viewplan()
    elif choice == "4":
        return
    else:
        print("INVALID!!! Enter numbers from 1-4")

def viewplan():
    query = 'SELECT * FROM Plan where PlanID !=000'
    login.execute(query)
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result,
                       headers=["PlanID","Duration","Cost","Coins","Details"]))
        
    else:
        print("""                           
                                                -------------------------------------------------------------------------------------
                                                                                 No Plan has been added !!  
                                                -------------------------------------------------------------------------------------                       
                 """)

def addplan():
    global PlanID
    viewplan()
    while True:
        PlanID = input("Enter PlanID: ")
        if len(PlanID) <= 3:
            break
        else:
            print("PlanID must have atleast 3 characters")
    while True:
        Duration = input("Enter Duration: ")
        if len(Duration) >= 3:
            break
        else:
            print("Duration must be Mentioned")
    while True:
        Cost = input("Enter Cost: ")
        if len(Cost) >= 3:
            break
        else:
            print("Cost must be Mentioned")
    while True:
        Coins = input("Enter Coins: ")
        if len(Coins) >= 3:
            break
        else:
            print("Coins must be Mentioned")
    while True:
        Details = input("Enter Details: ")
        if len(Details) >= 3:
            break
        else:
            print("Details must be Mentioned")
    insert_query = "INSERT INTO Plan VALUES (%s,%s,%s,%s,%s)"
    login.execute(insert_query, (int(PlanID),Duration,float(Cost),int(Coins),Details))
    databaseobj.commit()
    print("""                           
                                                -------------------------------------------------------------------------------------
                                                                           You have successfully added an Plan!!!  
                                                -------------------------------------------------------------------------------------                       
                     """)
    
    plan()


def updateplan():
    global PlanID
    query = 'SELECT * FROM Plan where PlanID !=000'
    login.execute(query)
    query_result = login.fetchall()

    if query_result:
        print(tabulate(query_result, headers=["PlanID", "Duration", "Cost", "Coins", "Details"]))

        while True:
            PlanID = input("Enter the PlanID to be edited: ")
            if PlanID.isdigit():
                break
            else:
                print("PlanID must be a number.")

        query = "SELECT * FROM Plan WHERE PlanID=%s"
        login.execute(query, (PlanID,))
        result = login.fetchone()

        if result is None:
            print("INVALID!!! PlanID does not exist...Enter a valid PlanID")
        else:
            print("Details for the selected PlanID are: ")
            print("PlanID:", result[0], "\nDuration:", result[1], "\nCost:", result[2], "\nCoins:", result[3],
                  "\nDetails:", result[4])

            while True:
                print("""
                Choose an option you want to update:
                1. Duration
                2. Cost
                3. Coins
                4. Details
                5. Go back
                """)

                choice = input("Enter a number from the above list: ")

                if choice == "1":
                    new_Duration = input("Enter New Duration: ")
                    if new_Duration:
                        query = "UPDATE Plan SET Duration=%s WHERE PlanID=%s"
                        login.execute(query, (new_Duration, PlanID))
                        databaseobj.commit()
                        print("""                           
                                                 -------------------------------------------------------------------------------------
                                                                       You have successfully updated the Duration.!!! 
                                                 -------------------------------------------------------------------------------------                       
                                                        """)
                    else:
                        print("Duration must be mentioned.")

                elif choice == "2":
                    new_Cost = input("Enter New Cost: ")
                    if new_Cost:
                        query = "UPDATE Plan SET Cost=%s WHERE PlanID=%s"
                        login.execute(query, (new_Cost, PlanID))
                        databaseobj.commit()
                        print("""                           
                                                 -------------------------------------------------------------------------------------
                                                                       You have successfully updated the Cost.!!! 
                                                 -------------------------------------------------------------------------------------                       
                                                                 """)
                    else:
                        print("Cost must be mentioned.")

                elif choice == "3":
                    new_Coins = input("Enter New Coins Value: ")
                    if new_Coins:
                        query = "UPDATE Plan SET Coins=%s WHERE PlanID=%s"
                        login.execute(query, (new_Coins, PlanID))
                        databaseobj.commit()
                        print("""                           
                                                 -------------------------------------------------------------------------------------
                                                                      You have successfully updated the Coins.!!! 
                                                 -------------------------------------------------------------------------------------                       
                                                                 """)
                    else:
                        print("Coins value must be mentioned.")

                elif choice == "4":
                    new_Details = input("Enter New Details: ")
                    if new_Details:
                        query = "UPDATE Plan SET Details=%s WHERE PlanID=%s"
                        login.execute(query, (new_Details, PlanID))
                        databaseobj.commit()
                        print("""                           
                                                 -------------------------------------------------------------------------------------
                                                                       You have successfully updated the Details.!!! 
                                                 -------------------------------------------------------------------------------------                       
                                                                 """)
                    else:
                        print("Details must be mentioned.")

                elif choice == "5":
                    break
                else:
                    print("INVALID!!! Enter numbers from 1-5.")
    else:
        print("""                           
                                                 -------------------------------------------------------------------------------------
                                                                                No Plan has been added !!  
                                                 -------------------------------------------------------------------------------------                       
                         """)
        
    plan()


def feedback():
    while True:
        print("""                            
                                                 -------------------------------------------------------------------------------------   
                                                                                        FEEDBACK
                                                 -------------------------------------------------------------------------------------   
                                  
                                                 Choose the option you want to:
                                                      
                                                 1. View Feedback
                                                 2. Response to Feedbacks
                                                 3. Go Back                       
              """)
        choice = input("Enter a number from the above list: ")
        if choice == "1":
            query = 'SELECT * FROM Feedback'
            login.execute(query)
            query_result = login.fetchall()
            if query_result:
                print(tabulate(query_result,
                               headers=["FeedbackID", "Feedback", "UserName", "Response"]))
                
            else:
                print("""                           
                                                 -------------------------------------------------------------------------------------
                                                                                  No Feedbacks has been added !!  
                                                 -------------------------------------------------------------------------------------                       
                    """)
                
        elif choice == "2":
            global FeedbackID
            query = 'SELECT * FROM Feedback'
            login.execute(query)
            query_result = login.fetchall()
            if query_result:
                print(tabulate(query_result, headers=["FeedbackID", "Feedback", "UserName", "Response"]))
                
                while True:
                    FeedbackID = input("Enter the FeedbackID to Respond: ")
                    if FeedbackID.isdigit():
                        break
                    else:
                        print("FeedbackID must be a number.")
                query = "SELECT * FROM Feedback WHERE FeedbackID=%s"
                login.execute(query, (FeedbackID,))
                result = login.fetchone()
                if result is None:
                    print("INVALID!!! FeedbackID does not exist...Enter a valid FeedbackID")
                else:
                    print("Details for the selected FeedbackID are: ")
                    print("FeedbackID:", result[0], "\nFeedback:", result[1], "\nUserName:", result[2], "\nResponse:",
                          result[3])
                    while True:
                        print("""
                            Choose an option you want to do:
                            1. Respond
                            2. Go back
                            """)
                        choice = input("Enter a number from the above list: ")
                        if choice == "1":
                            new_Response = input("Enter Response: ")
                            if new_Response:
                                query = f"UPDATE Feedback SET Response=%s WHERE FeedbackID=%s"
                                login.execute(query,(new_Response,FeedbackID))
                                databaseobj.commit()
                                print("""                           
                                                 -------------------------------------------------------------------------------------
                                                                    You have successfully added your Response.!!! 
                                                 -------------------------------------------------------------------------------------                       
                                        """)
                                
                        elif choice == "2":
                            break
                        else:
                            print("INVALID!!! Enter numbers from 1/2")
            else:
                print("""                           
                                                 -------------------------------------------------------------------------------------
                                                                            No Feedbacks has been added !!  
                                                 -------------------------------------------------------------------------------------                       
                                    """)
                
        elif choice == "3":
            break
        else:
            print("INVALID!!! Enter numbers from 1/2/3")


def payments():
    query = """
        SELECT p.PaymentID, p.Cost, p.BookID, p.BalanceID, p.PlanID, p.ModeOfPayment, p.PaymentFor, p.Date_and_Time, u.UserName
        FROM Payment p
        JOIN Balance b ON p.BalanceID = b.BalanceID
        JOIN UserInfo u ON b.UserName = u.UserName
    """
    login.execute(query)
    query_result = login.fetchall()
    if query_result:
        print(tabulate(query_result,
                       headers=["PaymentID", "Cost", "BookID", "BalanceID", "PlanID", "ModeOfPayment", "PaymentFor", "Date_and_Time", "UserName"]))
        
    else:
        print("""                           
                                                 -------------------------------------------------------------------------------------
                                                                                   No Payment has been done !!  
                                                 -------------------------------------------------------------------------------------                       
         """)
        

if __name__ == "__main__":
    startpage()