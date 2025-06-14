import tkinter as tk
from tkinter import messagebox

# Global variables to store user data
import mysql.connector as sqlator
mycon = sqlator.connect(host = "localhost",user = "root",passwd= "root", database ="pms")
cursor = mycon.cursor()
cursor.execute("select * from login")
data=cursor.fetchall()
mycon.close()

# Function for the Sign In page
def sign_in_page():
    # Hide the main window
    main_window.withdraw()
    
    # Create Sign In page window
    sign_in_window = tk.Toplevel()
    sign_in_window.title("Sign In")
    
    # Username Label and Entry
    tk.Label(sign_in_window, text="Username:").pack(pady=5)
    username_entry = tk.Entry(sign_in_window)
    username_entry.pack(pady=5)
    
    # Password Label and Entry
    tk.Label(sign_in_window, text="Password:").pack(pady=5)
    password_entry = tk.Entry(sign_in_window, show="*")
    password_entry.pack(pady=5)
    
    # Function to handle Sign In
    def submit_sign_in():
        username = username_entry.get()
        password = password_entry.get()
        #check if user exist or not
        for i in data:
            if  username in i and password in i:
                messagebox.showinfo("Sign In Success", "Welcome back, {}!".format(username))
                print(f"Signed in as: {username}")
                data_entry_page()
                  
            else:
                messagebox.showerror("Error", "Invalid username or password.")
    
    # Submit Button
    submit_button = tk.Button(sign_in_window, text="Submit", command=submit_sign_in)
    submit_button.pack(pady=10)
    
    # Cancel Button to go back to the main page
    cancel_button = tk.Button(sign_in_window, text="Back", command=lambda: go_back(sign_in_window))
    cancel_button.pack(pady=10)
    
    sign_in_window.mainloop()

# Function for the Sign Up page
def sign_up_page():
    # Hide the main window
    main_window.withdraw()
    
    # Create Sign Up page window
    sign_up_window = tk.Toplevel()
    sign_up_window.title("Sign Up")
    
    # Username Label and Entry
    tk.Label(sign_up_window, text="Username:").pack(pady=5)
    username_entry = tk.Entry(sign_up_window)
    username_entry.pack(pady=5)
    
    # Password Label and Entry
    tk.Label(sign_up_window, text="Password:").pack(pady=5)
    password_entry = tk.Entry(sign_up_window, show="*")
    password_entry.pack(pady=5)

    # Function to handle Sign Up
    def submit_sign_up():
        username = username_entry.get()
        password = password_entry.get()
        
        # Check if the username already exists
        if username in data:
            messagebox.showerror("Error", "Username already exists!")
        else:
            # Store the user's credentials
            import mysql.connector as sqlator
            mycon = sqlator.connect(host = "localhost",user = "root",passwd= "root", database ="pms")
            cursor = mycon.cursor()
            ps = "insert into login values (%s,%s) "
            aj = (username,password)
            cursor.execute(ps,aj)
            print('USER REGISTERED SUCCESSFULLY!!!')
            mycon.commit()
            mycon.close()
            data[0]=username
            data[1]=password  #for testing purpose
            messagebox.showinfo("Sign Up Success", f"Account created for {username}!")
            print(f"Signed up as: {username}")
            data_entry_page()
    
    # Submit Button
    submit_button = tk.Button(sign_up_window, text="Submit", command=submit_sign_up)
    submit_button.pack(pady=10)
    
    # Cancel Button to go back to the main page
    cancel_button = tk.Button(sign_up_window, text="Back", command=lambda: go_back(sign_up_window))
    cancel_button.pack(pady=10)
    
    sign_up_window.mainloop()

# Function to go back to the main page
def go_back(window):
    window.destroy()
    main_window.deiconify()

#data entry page
def data_entry_page():
    # Hide the main window
    main_window.withdraw()
    
    # Create data entry page window
    data_entry_window = tk.Toplevel()
    data_entry_window.title("Enter data")
    
    # name Label and Entry
    tk.Label(data_entry_window, text="Name of customer:").pack(pady=5)
    name_entry = tk.Entry(data_entry_window)
    name_entry.pack(pady=5)
    
    # taxi no Label and Entry
    tk.Label(data_entry_window, text="Taxi no:").pack(pady=5)
    taxi_no = tk.Entry(data_entry_window)
    taxi_no.pack(pady=5)

    # fare per km lable
    tk.Label(data_entry_window,text="Fare per km:").pack(pady=5)
    fare_per_km= tk.Entry(data_entry_window)
    fare_per_km.pack(pady=5)
    #distance
    tk.Label(data_entry_window,text="Total distance covered").pack(pady=5)
    d=tk.Entry(data_entry_window)
    d.pack(pady=5)
    # function for handling data


    tk.Button(data_entry_window, text="Generate Receipt", command=end_slip_page).pack(pady=20)



    def data_entry():
        name= name_entry.get()
        a=taxi_no.get()
        b=d.get()
        b=int(b)
        c=fare_per_km.get()
        c=int(c)
        messagebox.showinfo("Total Payable Amount(inr)",c*b)
        import mysql.connector as sqlator
        mycon = sqlator.connect(host = "localhost",user = "root",passwd= "root", database ="pms")
        cursor = mycon.cursor()
        rj =  (name,a,b,c,b*c)
        ppj ="insert into userdata values (%s,%s,%s,%s,%s)"
        cursor.execute(ppj,rj)
        mycon.commit()
        mycon.close()

    submit_button = tk.Button(data_entry_window, text="Submit", command=data_entry)
    submit_button.pack(pady=10)
    
    data_entry_window.mainloop()

def end_slip_page():
    # Database connection
    mycon = sqlator.connect(host="localhost", user="root", passwd="root", database="pms")
    cursor = mycon.cursor()
    
    # Retrieve user data
    cursor.execute("SELECT * FROM userdata")
    user_data = cursor.fetchall()
    mycon.close()

    # Hide main window
    main_window.withdraw()

    # Create new window for receipt
    end_slip_window = tk.Toplevel()
    end_slip_window.title("User Data - Receipt")

    # Header label
    tk.Label(end_slip_window, text="CUSTOMERS SO FAR", font=("Arial", 14, "bold")).pack(pady=5)

    # Display user data
    user_data_text = "\n".join([f"User: {user[0]}, Taxi No: {user[1]}, Fare: {user[2]}, Distance: {user[3]}, Total: {user[4]}" for user in user_data])
    
    if user_data_text:
        user_data_label = tk.Label(end_slip_window, text=user_data_text, justify="left", font=("Arial", 12))
        user_data_label.pack(pady=10)
    else:
        tk.Label(end_slip_window, text="No user data available.", font=("Arial", 12, "italic")).pack(pady=10)

    # Close button
    close_button = tk.Button(end_slip_window, text="Close", command=lambda: go_back(end_slip_window))
    close_button.pack(pady=10)

# Create the main window
main_window = tk.Tk()
main_window.title("Main Page")

# Sign In Button
sign_in_button = tk.Button(main_window, text="Sign In", command=sign_in_page)
sign_in_button.pack(pady=10)

# Sign Up Button
sign_up_button = tk.Button(main_window, text="Sign Up", command=sign_up_page)
sign_up_button.pack(pady=10)

main_window.mainloop()
