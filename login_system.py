#Login system to access RFID Timestamp Information
admin_username = "jgs71"
admin_password = "computernetworks"

print("Welcome...")
welcome = input("Do you have an account? y/n: ")
if welcome == "n":
    while True:
        alogin = input("Enter admin username: ")
        apassword = input("Enter admin password: ")
        if alogin == admin_username and apassword == admin_password:
            username  = input("Enter a username:")
            password  = input("Enter a password:")
            password1 = input("Confirm password:")
            if password == password1:
                file = open("master_data.txt", "w")
                file.write(username+":"+password)
                file.close()
                welcome = "y"
                break
            print("Passwords do NOT match!")
 
if welcome == "y":
    while True:
        login1 = input("Login:")
        login2 = input("Password:")
        file = open("master_data.txt", "r")
        data   = file.readline()
        file.close()
        if data == login1+":"+login2:
            print("Welcome")
            break
        print("Incorrect username or password.")