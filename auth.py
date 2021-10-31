# Authentication 
# -- Before the game starts a user need to authenticate
print("Please login to be able to save you points: \n Press (x) to login  \n Press (y) to register \n ")
# Login
if keyboard.read_key() == "x":
    print("Login")
    login() 
# Register 
if keyboard.read_key() == "y":
    print("Register")
    register()
    print("You are now ready to go !")
    print("The game will start .. NOW")