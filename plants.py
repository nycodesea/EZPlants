import plantsdb
from plantsdb import DB
import graph

TABLE = "plants_data"
FAVTABLE = "plants_fav_data"

plantsdb.init_db()
plantsdb.init_fav_db()
user_input = input(
    "0 : showing data\n1 : Input data\n2 : Delete data by name\n3 : Add to Favorite by name\n4 : Show Favorites\n"
)
if user_input == "0":
    user_input = input("Input a search word or blank for table: ")
    print("Display Plants Database\n")
    plantsdb.show_data(user_input, TABLE, DB)
    rows = plantsdb.get_temp_rows(user_input, TABLE, DB)
    graph.show_temp_range(rows)
    if user_input:
        gantt_rows = plantsdb.get_gantt_data(user_input, TABLE, DB)
        graph.show_gantt_chart(gantt_rows)
elif user_input == "1":
    plantsdb.save_plants(plantsdb.Input_plants_data(), TABLE, DB)
    print("Saved.")
elif user_input == "2":
    user_input = input("Input an item name to dlete: ")
    user_choose = input('Choose a table "Plants" or "Favorite"')
    print("Delete ", user_input)
    if user_choose == "Plants":
        plantsdb.delete_data(user_input, TABLE, DB)
    elif user_choose == "Favorite":
        plantsdb.delete_data(user_input, FAVTABLE, DB)
    else:
        print("Canceled deleting")

elif user_input == "3":
    user_input = input("Input a plants name to add: ")
    plantsdb.add_favorite(user_input)
    print("Saved to favorite")

elif user_input == "4":
    print("Favorites TABLE")
    plantsdb.show_data(None, FAVTABLE, DB)
