# MLB Data Web Scraper
import requests
import json
import tkinter as tk

class MLB_GUI:
    def __init__(self): # creates GUI window
        self.window = tk.Tk()
        self.window.title("MLB Data GUI")
        self.window.geometry("400x300")
        self.label = None
        self.players_dropdown = None
        self.season = tk.StringVar()
        self.season.set("Please pick a season") # prompts user to pick a season 
        self.seasons = list(range(2022, 1876, -1))

        self.season_dropdown = tk.OptionMenu(self.window, self.season, *self.seasons, command = self.season_chosen)
        self.season_dropdown.grid(row = 0, column = 0)

        self.window.mainloop()  

    def season_chosen(self, event = "None"): # gets season info 
        self.season_request_string = f"http://lookup-service-prod.mlb.com/json/named.team_all_season.bam?sport_code='mlb'&all_star_sw='N'&sort_order=name_asc&season={self.season.get()}"
        self.request = requests.get(self.season_request_string) # requests info
        self.team_dict = self.request.json()
        self.team_to_ids_dict = {}
        self.populate_id_dict()
        self.dropdown_teams_string_var = tk.StringVar()
        self.dropdown_teams_string_var.set("Please pick a team") # prompts user to pick a team
        self.dropdown_teams = tk.OptionMenu(self.window, self.dropdown_teams_string_var, *self.team_list, command = self.team_chosen)
        self.dropdown_teams.config(width = 20)
        self.dropdown_teams.grid(row = 0, column = 1)
        if self.label != None:
            self.label.destroy()
        if self.players_dropdown != None:
            self.players_dropdown.destroy()

    def populate_id_dict(self): # finds ID information from chosen year
        self.team_list = []
        temp_dict = {}
        for item in self.team_dict["team_all_season"]["queryResults"]["row"]:
            temp_dict[item["name"]] = int(item["team_id"])
            self.team_list.append(item["name"]) # add all team names to option choices 

        self.team_list.sort() 
        for item in self.team_list:
            self.team_to_ids_dict[item] = temp_dict.get(item)
        
    def team_chosen(self, event = "None"): # finds team information from chosen team
        self.player_list = []
        self.player_to_id_temp_dict = {}
        self.team = self.dropdown_teams_string_var.get()
        self.team_chosen_id = self.team_to_ids_dict[self.team]
        self.team_request_string = f"http://lookup-service-prod.mlb.com/json/named.roster_40.bam?team_id='{self.team_chosen_id}'"
        self.team_request = requests.get(self.team_request_string) # requests info
        for item in self.team_request.json()["roster_40"]["queryResults"]["row"]: # gets roster information from chosen team
            self.player_list.append(item["name_display_first_last"])
            self.player_to_id_temp_dict[item["name_display_first_last"]] = item["player_id"] # associates player ID with player first and last name
        self.sort_players()
        self.create_players_dropdown()
        if self.label != None:
            self.label.destroy()
        
    def sort_players(self): # sorts players based on ID number
        self.player_list.sort()
        self.player_to_id_dict = {}
        for item in self.player_list:
            self.player_to_id_dict[item] = self.player_to_id_temp_dict.get(item)
                       
    def create_players_dropdown(self): # creates player option drop-down box
        self.player_string_var = tk.StringVar()
        self.player_string_var.set("Please select a player")
        self.players_dropdown = tk.OptionMenu(self.window, self.player_string_var, *self.player_list, command = self.player_chosen)
        self.players_dropdown.config(width = 20)
        self.players_dropdown.grid(row = 0, column = 2, sticky = "NW")

    def player_chosen(self, event = "None"): # gets player information from chosen player
        self.player = self.player_string_var.get()
        self.player_id  = self.player_to_id_dict[self.player]
        self.player_info()
        self.postion_name()

        text = f"Player information:\n Name: {self.player}\n Team: {self.team}\n Postion: {self.postion}\n Age: {self.age}\n Jersey Number: {self.number}\n Bats: {self.bats}\n Throws: {self.throws}\n Pro Debut: {self.debut}"

        self.label = tk.Label(self.window, width = 40, height = 10, text = text)
        self.label.place(x = 0, y = 40)

    def postion_name(self): # allocates player position
        if self.postion == "1":
            self.postion = "Pitcher"
        elif self.postion == "2":
            self.postion = "Catcher"
        elif self.postion == "3":
            self.postion = "First-Base"
        elif self.postion == "4":
            self.postion = "Second-Base"
        elif self.postion == "5":
            self.postion = "Third Base"
        elif self.postion == "6":
            self.postion = "Shortstop"
        elif self.postion == "7":
            self.postion = "Left Field"
        elif self.postion == "8":
            self.postion = "Center Field"
        elif self.postion == "9":
            self.postion = "Right Field"
        
    def player_info(self): # formats and prints all of chosen player's information

        self.player_request_string = f"http://lookup-service-prod.mlb.com/json/named.player_info.bam?sport_code='mlb'&player_id={self.player_id}"
        self.player_request = requests.get(self.player_request_string)

        self.postion = self.player_request.json()['player_info']['queryResults']['row'].get("primary_position") # position
        self.age = self.player_request.json()['player_info']['queryResults']['row'].get("age") # age
        self.number = self.player_request.json()['player_info']['queryResults']['row'].get("jersey_number") # number
        self.bats = self.player_request.json()['player_info']['queryResults']['row'].get("bats") # batting stance
        self.throws = self.player_request.json()['player_info']['queryResults']['row'].get("throws") # throwing arm
        self.debut = self.player_request.json()['player_info']['queryResults']['row'].get("pro_debut_date") # pro debut

if __name__ == "__main__": # run program
    MLB_GUI()
