aircraft_data = {
    "F-15": {
        "avg_speed": 3500,
        "min_speed": 1200,
        "max_speed": 8500,
        "max_altitutde": 25000,
        "accelerating": 80,
        "stealth": 0.033,
        "military" : True,
        'h_max_rate' : 5,
        'v_max_rate' : 4,
        "jammer" : 0.5,
        "signal_killer": 2
    },
    "Su-27": {
        "avg_speed": 3300,
        "min_speed": 1100,
        "max_speed": 6500,
        "max_altitutde": 23000,
        "accelerating": 67,
        "stealth": 0.02,
        "military": True,
        'h_max_rate': 5,
        'v_max_rate': 5,
        "jammer" : 0.3,
        "signal_killer": 1
    },
    "F-18": {
        "avg_speed": 3000,
        "min_speed": 1250,
        "max_speed": 6000,
        "max_altitutde": 21000,
        "accelerating": 75,
        "stealth": 0.048,
        "military": True,
        'h_max_rate': 6,
        'v_max_rate': 5,
        'jammer' : 0.55,
        "signal_killer": 3.5
    },
    "Su-35": {
        "avg_speed": 3200,
        "min_speed": 1300,
        "max_speed": 7000,
        "max_altitutde": 27000,
        "accelerating": 80,
        "stealth": 0.045,
        "military": True,
        'h_max_rate': 7,
        'v_max_rate': 5,
        'jammer' : 0.4,
        "signal_killer": 2
    },
    "Su-57": {
        "avg_speed": 3700,
        "min_speed": 1200,
        "max_speed": 8000,
        "max_altitutde": 27000,
        "accelerating": 100,
        "stealth": 0.072,
        "military": True,
        'h_max_rate': 9,
        'v_max_rate': 8,
        "jammer": 0.6,
        "signal_killer": 4
    },
    "F-35": {
        "avg_speed": 3000,
        "min_speed": 1000,
        "max_speed": 7000,
        "max_altitutde": 25000,
        "accelerating": 90,
        "stealth": 0.115,
        "military": True,
        'h_max_rate': 7,
        'v_max_rate': 6,
        "jammer": 0.8,
        "signal_killer": 7

    },
    "F-22": {
        "avg_speed": 3300,
        "min_speed": 1200,
        "max_speed": 10000,
        "max_altitutde": 30000,
        "accelerating": 130,
        "stealth": 0.16,
        "military": True,
        'h_max_rate': 7,
        'v_max_rate': 7,
        "jammer": 0.95,
        "signal_killer" : 10

    },
    "Boeing 777 Passenger Plane": {
        "avg_speed": 3000,
        "min_speed": 850,
        "max_speed": 4000,
        "max_altitutde": 15000,
        "accelerating": 40,
        "stealth": 0,
        "military": False,
        'h_max_rate': 3,
        'v_max_rate': 2,
        "jammer": 0,
        "signal_killer": 2
    }
}

import random

russian = random.choice([-1,1])  ### if -1 is ukraine, 1 is russian 

rand = 0

def iff_check(id):
    global rand
    value = 0
    match id:
        case 1 | 3 | 4:
            if russian == 1 and rand == 0:
                rand = round(random.uniform(0.5, 1) * 100, 2)
            elif russian == -1 and rand ==0:
                if id !=4:
                    rand = round(random.uniform(0.3, 0.6) * 100, 2)
                else:
                    rand = round(random.uniform(0.5, 1) * 100, 2)
            value = round(random.uniform(rand - 5, rand + 5), 2)
        case 0 | 2:
            luck = random.random()
            if luck < 0.1:
                if rand == 0:
                    rand = round(random.uniform(0.5, 0.6) * 100, 2)
                value = round(random.uniform(rand - 5, rand + 5), 2)
            else:
                if rand == 0:
                    rand = round(random.uniform(0.3, 0.5) * 100, 2)
                value = round(random.uniform(rand - 15, rand + 15), 2)
        case 5 | 6:
            luck = random.random()
            if luck < 0.65:
                if rand == 0:
                    rand = round(random.uniform(0.5, 0.8) * 100, 2)
                value = round(random.uniform(rand - 7, rand + 7), 2)
            else:
                if rand == 0:
                    rand = round(random.uniform(0.4, 0.5) * 100, 2)
                value = round(random.uniform(rand - 10, rand + 10), 2)
        case 7:
            if rand == 0:
                rand = round(random.uniform(0.2, 0.4) * 100, 2)
            value = round(random.uniform(rand - 15, rand + 15), 2)
    return value

