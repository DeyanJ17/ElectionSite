import requests, json
import math, random
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
        polls_data = []

    presidential_polls = []
    year = date.year
    month = date.month
    day = date.day

    for poll in polls_data:
        poll_start_date = datetime.strptime(poll['startDate'], "%Y-%m-%d").date()
        comparison_date = datetime(year, month, day).date()
        if poll['type'] == 'president-general' and (poll['answers'][0]['choice'] == "Harris" and poll['answers'][1]['choice'] == "Trump") and poll_start_date >= comparison_date:
            presidential_polls = presidential_polls + [poll]
    
    return presidential_polls

def calculate_weight(days_old, poll):
    size = int(poll['sampleSize'])
    date = math.exp(-days_old/10)

    if poll['sponsors'] == [] or (poll['sponsors'][0]['partisan'] is None and poll['partisan_pollster'] is None):
        sponsor = 0.95
    else:
        sponsor_dict = poll['sponsors'][0]
        try:
            if sponsor_dict['internal'] is True:
                sponsor = 0.65
        except:
            -1 # doesn't exist
        
        sponsor = 0
        for i in range(len(sponsor_dict)):
            if sponsor_dict['partisan'] == "Robert F. Kennedy": # RFK does individual matchup polls with himself and Harris/Trump
                sponsor += 0.15
            elif sponsor_dict['partisan'] == "Republican Party":
                sponsor += 0.4
            elif sponsor_dict['partisan'] == "Democratic Party":
                sponsor += 0.7
            else: 
                sponsor += 0.9
        
        sponsor /= len(sponsor_dict)
        
    return (size*date*sponsor)

def calculate_average(state_name, presidential_polls):
    avgs = [0,0] # Harris Avg, Trump Avg
    Harris_avg = 0
    trump_avg = 0

    total_weight = 0
    district_weight = 0
    
    for poll in presidential_polls:
        if poll['state'] == state_name and poll['sampleSize'] is not None:
            created_at = poll['created_at'].split('-')
            poll_date = datetime(int(created_at[0]), int(created_at[1]), int(created_at[2]))
            days_old = (datetime.now()-poll_date).days
            weight = calculate_weight(days_old, poll)
            state = poll['state']

            national_factor = 1
            if state != "National":
                if days_old >= 15:
                    national_factor = 1.5
                elif days_old >= 10:
                    national_factor = 1.35
                elif days_old >= 5:
                    national_factor = 1.1
                else:
                    national_factor = 1

            weight = weight*national_factor

            try:
                if poll['district'] == "2": # check if this is a ME-2 or NE-2 poll
                    district_weight += weight
                    Harris_avg += weight*float(poll['answers'][0]['pct'])
                    trump_avg += weight*float(poll['answers'][1]['pct'])
            except:
                total_weight += weight
                avgs[0] += weight*float(poll['answers'][0]['pct'])
                avgs[1] += weight*float(poll['answers'][1]['pct'])

    if district_weight != 0:
        district_avgs[state][0] = round(Harris_avg/district_weight, 2)
        district_avgs[state][1] = round(trump_avg/district_weight, 2)

    if total_weight > 0:
        return [round(avgs[0]/total_weight, 2), round(avgs[1]/total_weight, 2)]
    else:
        return "No Polls"
    
def get_color(lead):
    if lead < 0:
        lead = abs(lead)
        if lead <= 2.5:
            color = "#FAA0A0"
        elif lead > 2.5 and lead <= 6:
            color = "#FF474C"
        elif lead > 6 and lead < 10:
            color = "#DC143C"
        else:
            color = "#8B0000"    
    elif lead > 0:
        if lead <= 2.5:
            color = "#00FFFF"
        elif lead > 2.5 and lead <= 6:
            color = "#89CFF7"
        elif lead > 6 and lead < 10:
            color = "#6495ED"
        else:
            color = "blue"
    else:
        color = "white"
    
    return color

def get_trump_leads(lead):
    return lead < 0

def get_state_multiplier(state, lead, difference):
    trump_leads = get_trump_leads(lead)
    if state == "Arizona" or state == "Georgia" or state == "Nevada" or state == "North Carolina": # Sunbelt States
        if trump_leads: # Trump's support increased from inroads with minorities, who are less likely to turn out
            if "R" in spread_2020[state]: 
                multiplier = 0.1*(difference+lead)
            else: # Suburban voters/minority voters underpolled in 2020
                multiplier = 0.2*(difference+lead)
            
            return -multiplier
        else: 
            if "R" in spread_2020[state]: # Risk of underpolling Trump supporters and overpolling college educated/suburban voters
                multiplier = 0.3*(difference+lead)
                return -multiplier
            else: # Suburban voters/minority voters underpolled in 2020
                multiplier = 0.1*(difference+lead) 
                return multiplier

    elif state == "Florida" or state == "Texas": # States where Latino populations lean more conservative
        if "R" in spread_2020[state]: 
            if trump_leads: # Trump's support increased from inroads with minorities
                multiplier = abs(0.2*(difference+lead))
            else: # Suburban voters/minority voters underpolled in 2020
                multiplier = abs(0.1*(difference+lead))
            
            return -multiplier
        else: 
            if "R" in spread_2020[state]: # Risk of underpolling Trump supporters and overpolling college educated/suburban voters
                multiplier = 0.5*(difference+lead)
                return -multiplier
            else: # Suburban voters/minority voters underpolled in 2020
                multiplier = 0.075*(difference+lead) 
                return multiplier

    elif state == "Michigan" or state == "Minnesota" or state == "Pennsylvania" or state == "Wisconsin": # Rustbelt States
        if trump_leads: # Trump's support increased from minorities; Trump voters undersampled in 2020
            if "R" in spread_2020[state]:
                multiplier = abs(0.1*(difference+lead))
                return -multiplier
            else: # Suburban voters/minority voters underpolled in 2020
                multiplier = abs(0.2*(difference+lead))
                return multiplier

        else: # Risk of underpolling Trump supporters and overpolling college educated/suburban voters
            if "R" in spread_2020[state]:
                multiplier = 0.1*(difference+lead)
                return -multiplier
            else: # Suburban voters/minority voters underpolled in 2020
                multiplier = 0.05*(difference+lead) 
                return multiplier

    else:
        return 1

def model_prediction(lead, state):
    trump_leads = get_trump_leads(lead)
    lead = abs(lead)
    harris_chance = 50

    if lead <= 2.5:
        multiplier = 1.6
    elif lead <= 4:
        multiplier = 1.75
    elif lead <= 6:
        multiplier = 1.85
    elif lead <= 8:
        multiplier = 1.9
    elif lead < 10:
        multiplier = 1.95
    else:
        multiplier = 2

    lead *= multiplier    
    if trump_leads:
        harris_chance -= lead
    else:
        harris_chance += lead

    if state != "National":
        pvi_arr = cook_pvi[state].split("+")
        margin = int(pvi_arr[1])

        if "R" in pvi_arr[0]:
            harris_chance -= margin
        else:
            harris_chance += margin
    
        if state in spread_2020:
            difference = float(spread_2020[state].split("+")[1])
            harris_chance += get_state_multiplier(state, lead, difference)

            if state == "Ohio": # Adjusting for Trump's 5+ margin in 2020
                harris_chance -= 10
            elif state == "Florida" or state == "Texas": # Adjusting for Trump 3+ margin in 2020
                harris_chance -= 5

            if state == "New Mexico" or state == "Virginia": # Adjusting for Harris's 10+ margin in 2020
                harris_chance += 10
            elif state == "Maine" or state == "Minnesota" or state == "New Hampshire": # Adjusting for Harris's 5+ margin in 2020
                harris_chance += 5

    harris_chance = max(min(harris_chance, 99), 1)
    trump_chance = max(min(100-harris_chance, 99), 1)

    return {"Harris Prob": round(harris_chance), "Trump Prob": round(trump_chance)}

def get_results(presidential_polls):
    formatted = {}
    state_results = {}
    for state in states:
        result = calculate_average(state, presidential_polls)
        if result == "No Polls":
            formatted[state] = "No Polls"
        else:
            candidate_pct = {}
            candidate_pct["Harris"] = result[0]
            candidate_pct["Trump"] = result[1]
            state_results[state] = candidate_pct

            lead = (round(result[0] - result[1], 2))
            prediction = model_prediction(lead, state)
            if lead < 0:
                formatted[state] = [state_results[state], "R +" + str(abs(lead)), get_color(lead), prediction]
            else:
                formatted[state] = [state_results[state], "D +" + str(abs(lead)), get_color(lead), prediction]

            me_lead = abs(district_avgs["Maine"][0]-district_avgs["Maine"][1])
            ne_lead = abs(district_avgs["Nebraska"][0]-district_avgs["Nebraska"][1])

            formatted["ME-2"] = [district_avgs["Maine"], str(me_lead), get_color(me_lead)]
            formatted["NE-2"] = [district_avgs["Nebraska"], str(ne_lead), get_color(ne_lead)]

    return formatted

def main():
    presidential_polls = get_new_json(date)
    path = '../site/src/pages/imports/data.json'
    results = get_results(presidential_polls)
    with open(path, 'w') as f:
        json.dump(results, f)

    simulate_election(results)


# Variables for simulate_election()

state_dict = {"Alabama": ["AL", 9], "Alaska": ["AK", 3], "Arizona": ["AZ", 11], "Arkansas": ["AR", 6], "California": ["CA", 54], "Colorado": ["CO", 10], 
    "Connecticut": ["CT", 6], "Delaware": ["DE", 3], "Florida": ["FL", 30], "Georgia": ["GA", 16], "Hawaii": ["HI", 4], "Idaho": ["ID", 4], "Illinois": ["IL", 19],
    "Indiana": ["IN", 9], "Iowa": ["IA", 6], "Kansas": ["KS", 6], "Kentucky": ["KY", 6], "Louisiana": ["LA", 8], "Maine": ["ME", 2], "Maryland": ["MD", 10], 
    "Massachusetts": ["MA", 11], "Michigan": ["MI", 15], "Minnesota": ["MN", 10], "Mississippi": ["MI", 6], "Missouri": ["MO", 10],  "Montana": ["MT", 4], 
    "Nebraska": ["NE", 4], "Nevada": ["NV", 6], "New Hampshire": ["NH", 4], "New Jersey": ["NJ", 14], "New Mexico": ["NM", 5], "New York": ["NY", 28], 
    "North Carolina": ["NC", 16], "North Dakota": ["ND", 3], "Ohio": ["OH", 17], "Oklahoma": ["OK", 7], "Oregon": ["OR", 8], "Pennsylvania": ["PA", 19], 
    "Rhode Island": ["RI", 4], "South Carolina": ["SC", 9], "South Dakota": ["SD", 3], "Tennessee": ["TN", 11], "Texas": ["TX", 40], "Utah": ["UT", 6], 
    "Vermont": ["VT", 3], "Virginia": ["VA", 13], "Washington": ["WA", 12], "West Virginia": ["WV", 4], "Wisconsin": ["WI", 10], "Wyoming": ["WY", 3]} 

red_states = ["Alabama", "Arkansas", "Indiana", "Idaho", "Kansas", "Kentucky", "Louisiana", "Mississippi", "South Carolina", "Wyoming"]

def simulate_election(election_data):
    harris_wins = 0

    for i in range(1000):
        # adding electoral votes from states without polls
        harris_votes = 3  # adding DC EVs
        trump_votes = 0

        for state in state_dict:
            if election_data[state] == "No Polls":
                if state not in red_states:
                    harris_votes += state_dict[state][1]
            elif state in ["ME-1", "ME-2", "NE-2"]:
                if state == "ME-2" and (election_data["ME-1"][0][0] > election_data["ME-2"][0][1]):
                    harris_votes += 1
                elif state == "ME-2":
                    pass # don't add to Harris as this should go to Trump
                elif state == "NE-2" and (election_data["NE-2"][0][0] > election_data["NE-2"][0][1]):
                    harris_votes += 1
            else:
                random_num = random.random()*100
                if election_data[state][3]["Harris Prob"] >= random_num:
                    harris_votes += state_dict[state][1]
                else:
                    trump_votes += state_dict[state][1]

        if harris_votes >= 270:
            harris_wins += 1

    harris_prob = round((harris_wins/1000)*100)

    path = '../site/src/pages/imports/simulation.json'
    with open(path, 'w') as f:
        json.dump([harris_prob, 100-harris_prob], f)

# Global Variables for Simplicity
date = datetime(2024, 7, 21)
district_avgs = {"Maine": [0,0], "Nebraska":[0,0]}

spread_2020 = {"Arizona": "R +0.6", "Florida": "R +4.2", "Georgia": "D +1.3", "Maine": "R +3.93", "Michigan": "R +1.4", "Minnesota": "D +2.9", 
                    "New Hampshire": "R +3.75", "New Mexico": "R +0.91", "Nevada": "R +2.88", "North Carolina": "R +1.1", "Pennsylvania": "R +3.53", "Texas": "R +4.5", 
                    "Virginia": "R +1.6", "Wisconsin": "R +6.0"} # Difference between RCP average and actual results (used 538 averages for ME, NH, NM, NV, PA, VA)

cook_pvi = {"Alabama": "R +15", "Alaska": "R +8", "Arizona": "R +2", "Arkansas": "R +16", "California": "D +13", "Colorado": "D +4", "Connecticut": "D +7", "Delaware": "D +7", 
            "Florida": "R +3", "Georgia": "R +3", "Hawaii": "D +14", "Idaho": "R +18", "Illinois": "D +7", "Indiana": "R +11", "Iowa": "R +6", "Kansas": "R +10", 
            "Kentucky": "R +16", "Louisiana": "R +12", "Maine": "D +2", "ME-1": "D +9", "Maryland": "D +14", "Massachusetts": "D +15", "Michigan": "R +1", 
            "Minnesota": "D +1", "Mississippi": "R +11", "Missouri": "R +10", "Montana": "R +11", "Nebraska": "R+ 13", "Nevada": "R +1", "New Hampshire": "D +1", 
            "New Jersey": "D +6", "New Mexico": "D +3", "New York": "D +10", "North Carolina": "R +3", "North Dakota": "R +20", "Ohio": "R +6", "Oklahoma": "R +20", 
            "Oregon": "D +6", "Pennsylvania": "R +2", "Rhode Island": "D +8", "South Carolina": "R +8", "South Dakota": "R +16", "Tennessee": "R +14", "Texas": "R +5", 
            "Utah": "R +13", "Vermont": "D +16", "Virginia": "D +3", "Washington": "D +8", "West Virginia": "R +22", "Wisconsin": "R +2", "Wyoming": "R +25"}

main()