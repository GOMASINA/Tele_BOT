from DatabaseManager import DatabaseManager

a = DatabaseManager()
a.Connect()
print(a.UserInformation('3'))
