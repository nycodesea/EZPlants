import plantsdb

plantsdb.init_db()
user_input = input("0 : showing data\n1 : Input data\n2 : Delete data by name\n")
if user_input == "1":
    plantsdb.save_plants(plantsdb.Input_plants_data())
    print("Saved.")
elif user_input == "0":
    user_input = input("Input a search word or blank for table: ")
    print("Display Plants Database\n")
    plantsdb.show_data(user_input)
elif user_input == "2":
    user_input = input("Input an item name to dlete: ")
    print("Delete ", user_input)
    plantsdb.delete_data(user_input)
