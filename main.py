from ms_active_directory import ADDomain
import getpass

domain = ADDomain("net.mag")
password = getpass.getpass("Password: ")
session = domain.create_session_as_user("hly@markanthony.com", password)

lineBreak = "========================================"


def findManager():
    print(lineBreak)
    newManager = input("Type the username of the user's new manager (username): ")
    return session.find_user_by_sam_name(newManager, ["Name", "distinguishedName"])


def findUser():
    print(lineBreak)
    userToSearch = input("Type the name of the user to search for (First Last): ")
    return session.find_users_by_common_name(userToSearch, ["Name", "UserPrincipalName", "Title", "Manager"])


while (True):
    userSearchResult = findUser()
    user = None

    changeableAtrributes = ["Manager", "Title"]
    
    print("The attributes that you can change are: ", end = " ")
    
    for item in changeableAtrributes:
        print(item, end = " ")
    
    print()
    print(lineBreak)

    attributeToChange = input("What attribute would you like to change? ").capitalize()



    if len(userSearchResult) == 1:
        user = userSearchResult[0]
        print("User's UPN: " + user.get("UserPrincipalName"))
        print("User's Current Manager: " + user.get("Manager"))
        print(lineBreak)
    elif len(userSearchResult) == 0:
        print("No users have been found with the specified name.")
        print(lineBreak)
        continue
    else:
        print(str(len(userSearchResult)) + " users have been found. Please select the correct user.")
        
        for count, us in enumerate(userSearchResult):
            print("[" + count + "] UPN: " + us.get("UserPrincipalName") + "; Title: " + us.get("Title"))

        print("This edge case has yet to be fully implemented.")

    managerSearchResult = findManager()

    while (managerSearchResult == None):
        print("New manager could not be found. Please try again.")
        managerSearchResult = findManager()
    
    print(lineBreak)
    print("New Manager's Name: " + managerSearchResult.get("Name") + "; New Manager's DN: " + managerSearchResult.get("distinguishedName"))
    print(lineBreak)

    confirm = input(f"Confirm change of {user.get('Name')}\'s manager to {managerSearchResult.get('Name')}, ({managerSearchResult.get('distinguishedName')})? (y/n)").lower()
    print(lineBreak)

    if (confirm == "y"):
        success = session.overwrite_attribute_for_user(user, "Manager", managerSearchResult.get("distinguishedName"))
        if (success):
            print("Manger successfully updated.")
        else:
            print("Manager update failed.")
        print(lineBreak)
    else:
        continue

    
    continueRule = input("Would you like to create a new session? (y/n) ").lower()

    if continueRule == 'y':
        continue
    else:
        break


    