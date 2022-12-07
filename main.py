from ms_active_directory import ADDomain
from ms_active_directory import MsActiveDirectoryException
import getpass

def findManager():
    print(lineBreak)
    newManager = input("Type the username of the user's new manager (username): ")
    return session.find_user_by_sam_name(newManager, ["Name", "distinguishedName"])


def findUser():
    print(lineBreak)
    userToSearch = input("Type the name of the user to search for (First Last): ")
    return session.find_users_by_common_name(userToSearch, ["Name", "UserPrincipalName", "Title", "Manager"])

domain = ADDomain("net.mag")

session = None

while session is None:
    try:
        email = input("Enter your email: ")
        password = getpass.getpass("Enter your password: ")
        session = domain.create_session_as_user(email, password)
    except MsActiveDirectoryException:
        print("Authentication failed. Please try again.")
        pass

lineBreak = "=================================================================================================="


while (True):
    
    # Handle finding the AD User that you want to modify
    userSearchResult = findUser()
    user = None

    if len(userSearchResult) == 1:
        user = userSearchResult[0]
        print("Selected User's UPN: " + user.get("UserPrincipalName"))
    elif len(userSearchResult) == 0:
        print("No users have been found with the specified name.")
        continue
    else:
        print(str(len(userSearchResult)) + " users have been found. Please select the correct user.")
        
        for count, us in enumerate(userSearchResult):
            print("[" + count + "] UPN: " + us.get("UserPrincipalName") + "; Title: " + us.get("Title"))

        print("This edge case has yet to be fully implemented.")



    # Selecting the attribute you want to change
    changeableAtrributes = ["Manager", "Title"]
    
    print(lineBreak)
    print("The attributes that you can change are:", end = " ")
    
    for item in changeableAtrributes:
        print(item, end = "; ")
    
    print()
    attributeToChange = input("What attribute would you like to change? ").capitalize()

    while attributeToChange not in changeableAtrributes:
        print(lineBreak)
        print("Inputted attribute not found. Please try again.")
        attributeToChange = input("What attribute would you like to change? ").capitalize()


    if (attributeToChange == "Manager"):
        print("Selected User's Current Manager: " + user.get("Manager"))
        managerSearchResult = findManager()

        while (managerSearchResult == None):
            print("New manager could not be found. Please try again.")
            managerSearchResult = findManager()
        
        print(lineBreak)
        print("New Manager's Name: " + managerSearchResult.get("Name") + "; New Manager's DN: " + managerSearchResult.get("distinguishedName"))
        print(lineBreak)

        confirm = input(f"Confirm change of {user.get('Name')}\'s manager to {managerSearchResult.get('Name')}, ({managerSearchResult.get('distinguishedName')})? (y/n) ").lower()

        if (confirm == "y"):
            success = session.overwrite_attribute_for_user(user, "Manager", managerSearchResult.get("distinguishedName"))
            if (success):
                print("Manager successfully updated.")
            else:
                print("Manager update failed.")
            print(lineBreak)
        else:
            print("The manager change has been aborted. No changes have been made.")
    elif (attributeToChange == "Title"):
        print("Selected User's Current Title: " + user.get("Title"))
        print(lineBreak)

        newTitle = input("Enter the user's new title: ")
        print(lineBreak)

        confirm = input(f"Confirm change of {user.get('Name')}\'s title to {newTitle}? (y/n) ").lower()

        if (confirm == "y"):
            success = session.overwrite_attribute_for_user(user, "Title", newTitle)
            success2 = session.overwrite_attribute_for_user(user, "Description", newTitle)

            if (success and success2):
                print("Title successfully updated.")
            else:
                print("Title update failed.")
            print(lineBreak)
        else:
            print("The title change has been aborted. No changes have been made.")

    continueRule = input("Would you like to create a new session? (y/n) ").lower()

    goodInputs = ["y", "n"]

    while continueRule not in goodInputs:
        continueRule = input("ERROR: Unexpected input. Would you like to create a new session? (y/n) ").lower()

    if continueRule == 'y':
        continue
    else:
        break


    