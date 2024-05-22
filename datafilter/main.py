import requests
import json
from datetime import datetime

url = "https://projects.fivethirtyeight.com/polls/polls.json"
states = ["National", 
          "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", 
          "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", 
          "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", 
          "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"] 

def get_new_json(date):
    response = requests.get(url)

    if response.status_code == 200:
        polls_data = response.json()
    else:
        print("Failed to retrieve the data")
        polls_data = []

    presidential_polls = []
    year = date[0]
    month = date[1]
    day = date[2]

    for poll in polls_data:
        poll_start_date = datetime.strptime(poll['startDate'], "%Y-%m-%d").date()
        comparison_date = datetime(year, month, day).date()
        if poll['type'] == 'president-general' and (poll['answers'][0]['choice'] == "Biden" and poll['answers'][1]['choice'] == "Trump") and poll_start_date >= comparison_date:
            presidential_polls = presidential_polls + [poll]
    
    return presidential_polls

def calculate_average(state_name, presidential_polls):
    total = [0, 0]
    count = 0
    for poll in presidential_polls:
        if poll['state'] == state_name:
            total[0] += float(poll['answers'][0]['pct']) # adding Biden's numbers
            total[1] += float(poll['answers'][1]['pct']) # adding Trump's numbers
            count += 1

    if count > 0:
        return [round(total[0]/count, 2), round(total[1]/count, 2)]
    else:
        return "No Polls"

def get_results(presidential_polls):
    formatted = {}
    state_results = {}
    for state in states:
        result = calculate_average(state, presidential_polls)
        if result == "No Polls":
            formatted[state] = "No Polls"
        else:
            candidate_pct = {}
            candidate_pct["Biden"] = result[0]
            candidate_pct["Trump"] = result[1]
            state_results[state] = candidate_pct
            
            lead = round(result[0] - result[1], 2)
            if lead < 0:
                lead = abs(lead)
                if lead <= 3.5:
                    color = "#FF474C"
                    formatted[state] = [state_results[state], "R +" + str(lead), color]
                elif lead > 3.5 and lead <= 7.5:
                    color = "#DC143C"
                    formatted[state] = [state_results[state], "R +" + str(lead), color]
                else:
                    color = "#8B0000"
                    formatted[state] = [state_results[state], "R +" + str(lead), color]
            else:
                if lead <= 3.5:
                    color = "#89CFF0"
                    formatted[state] = [state_results[state], "D +" + str(lead), color]
                elif lead <= 7.5:
                    color = "#6495ED"
                    formatted[state] = [state_results[state], "D +" + str(lead), color]
                else:
                    color = "blue"
                    formatted[state] = [state_results[state], "D +" + str(lead), color]

    return formatted

def main():
    date_arr = input("Enter a date (yyyy/mm/dd): ").split("/")
    date = (int(date_arr[0]), int(date_arr[1]), int(date_arr[2]))
    presidential_polls = get_new_json(date)
    
    path = '../site/src/pages/imports/data.json'
    with open(path, 'w') as f:
        json.dump(get_results(presidential_polls), f)

main()