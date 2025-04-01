import pandas as pd
import us
import re

# Correcting file path using raw string
file_path = r"C:\Users\arava\Desktop\Portfolio\Project 1\Data\car_prices.csv"

# Load the dataset
data = pd.read_csv(file_path)

# Display first few rows
#print(data.head())

#Show info of the dataset
#print(data.info())

#Drop blank rows
data.dropna(inplace=True)
#print(data.info())

#Drop duplicates
data.drop_duplicates(inplace=True)
#print(data.info())

#Remove columns
data.drop(columns=['vin', 'saledate',"seller"], errors='ignore', inplace=True)

#US State mapping
state_abbr_to_name = {state.abbr: state.name for state in us.states.STATES}
data['state'] = data['state'].str.upper().map(state_abbr_to_name).fillna(data['state'])
data.loc[data['state'] == "pr", 'state'] = "Puerto Rico"

#Standardization
data['make']=data['make'].str.lower().str.strip()
make_mappings={
    "merc":"mercedes",
    "mb":"mercedes",
    "chevy":"chevrolet",
    "vw":"volkswagen",
    "bwm":"bmw",
    "toy":"toyota",
    "hnd":"honda",
}
data['make']=data['make'].replace(make_mappings)
data['make']=data['make'].str.title()
data['condition']=pd.to_numeric(data['condition'],errors='coerce')  # Convert to numeric
data.loc[data['condition'] > 5, 'condition']/=10 # Convert 45 → 4.5
data['condition'] = data['condition'].clip(lower=1, upper=5)
text_columns = ['body', 'transmission', 'color', 'interior']
for col in text_columns:
    data[col] = data[col].str.lower().str.strip().str.title()
body_mapping = {
    "SUV": ["Suv"],
    "Sedan": ["Sedan", "G Sedan"],
    "Coupe": ["Coupe", "G Coupe", "Genesis Coupe", "Elantra Coupe", "Cts Coupe", "Cts-V Coupe", "G37 Coupe", "Q60 Coupe"],
    "Convertible": ["Convertible", "G Convertible", "G37 Convertible", "Q60 Convertible", "Beetle Convertible", "Granturismo Convertible"],
    "Hatchback": ["Hatchback", "Koup"],
    "Wagon": ["Wagon", "Cts Wagon", "Cts-V Wagon", "Tsx Sport Wagon"],
    "Minivan": ["Minivan"],
    "Van": ["Van", "E-Series Van", "Transit Van", "Promaster Cargo Van", "Ram Van"],
    "Pickup Truck": [
        "Crew Cab", "Double Cab", "Crewmax Cab", "Access Cab", "King Cab", "Supercrew", "Extended Cab",
        "Supercab", "Regular Cab", "Quad Cab", "Mega Cab", "Cab Plus 4", "Cab Plus", "Club Cab", "Xtracab", "Regular-Cab"
    ]
}
def standardize_body(body_type):
    for standard, variations in body_mapping.items():
        if body_type in variations:
            return standard
    return body_type  # If no match, keep original
data['body'] = data['body'].map(standardize_body)
model_mapping = {
    # Toyota
    "Camry": ["Camry", "Camry Hybrid", "Camry XSE", "Camry SE"],
    "Corolla": ["Corolla", "Corolla Cross", "Corolla Hybrid", "Corolla LE", "Corolla XSE"],
    "Highlander": ["Highlander", "Highlander Hybrid"],
    "Tacoma": ["Tacoma", "Tacoma TRD", "Tacoma SR5"],
    "RAV4": ["RAV4", "RAV4 Hybrid", "RAV4 Prime"],
    "4Runner": ["4Runner", "4Runner TRD"],
    "Tundra": ["Tundra", "Tundra Hybrid"],

    # Honda
    "Civic": ["Civic", "Civic Type R", "Civic Hybrid", "Civic EX", "Civic LX"],
    "Accord": ["Accord", "Accord Hybrid", "Accord Sport"],
    "CR-V": ["CR-V", "CR-V Hybrid"],
    "Pilot": ["Pilot", "Pilot Elite"],
    "Odyssey": ["Odyssey", "Odyssey Touring"],

    # Nissan
    "Altima": ["Altima", "Altima Coupe", "Altima SL"],
    "Sentra": ["Sentra", "Sentra Nismo"],
    "Maxima": ["Maxima", "Maxima Platinum"],
    "Pathfinder": ["Pathfinder", "Pathfinder Rock Creek"],
    "Rogue": ["Rogue", "Rogue Sport"],
    "Frontier": ["Frontier", "Frontier Pro-4X"],
    "Titan": ["Titan", "Titan XD"],

    # Ford
    "F-150": ["F150", "F-150", "F 150", "F-150 XLT", "F-150 Lariat"],
    "Mustang": ["Mustang", "Mustang Mach-E", "Mustang GT"],
    "Explorer": ["Explorer", "Explorer Sport", "Explorer Hybrid"],
    "Escape": ["Escape", "Escape Hybrid"],
    "Edge": ["Edge", "Edge ST"],
    "Bronco": ["Bronco", "Bronco Sport"],
    "Expedition": ["Expedition", "Expedition Max"],
    "Super Duty": ["F-250", "F-350", "F-450", "Super Duty F-250", "Super Duty F-350"],

    # Chevrolet
    "Tahoe": ["Tahoe", "Tahoe Hybrid"],
    "Silverado": ["Silverado 1500", "Silverado 2500", "Silverado 3500"],
    "Malibu": ["Malibu", "Malibu Hybrid"],
    "Equinox": ["Equinox", "Equinox EV"],
    "Traverse": ["Traverse", "Traverse RS"],
    "Blazer": ["Blazer", "Blazer EV"],
    "Suburban": ["Suburban", "Suburban Premier"],

    # Jeep
    "Wrangler": ["Wrangler", "Wrangler Unlimited", "Wrangler Sahara"],
    "Grand Cherokee": ["Grand Cherokee", "Grand Cherokee L", "Grand Cherokee 4xe"],
    "Cherokee": ["Cherokee", "Cherokee Trailhawk"],
    "Compass": ["Compass", "Compass Limited"],
    "Renegade": ["Renegade", "Renegade Trailhawk"],
    "Gladiator": ["Gladiator", "Gladiator Mojave"],

    # Tesla
    "Model S": ["Model S", "Tesla Model S"],
    "Model 3": ["Model 3", "Tesla Model 3"],
    "Model X": ["Model X", "Tesla Model X"],
    "Model Y": ["Model Y", "Tesla Model Y"],

    # Mercedes-Benz
    "C-Class": ["C-Class", "C300", "C350"],
    "E-Class": ["E-Class", "E350", "E450"],
    "S-Class": ["S-Class", "S550", "S560"],
    "GLC": ["GLC", "GLC 300"],
    "GLE": ["GLE", "GLE 350"],
    "GLS": ["GLS", "GLS 450"],
    
    # BMW
    "3 Series": ["3 Series", "330i", "320i"],
    "5 Series": ["5 Series", "530i", "540i"],
    "7 Series": ["7 Series", "740i", "750i"],
    "X3": ["X3", "X3 M40i"],
    "X5": ["X5", "X5 M50i"],
    "X7": ["X7", "X7 M60i"],

    # Audi
    "A3": ["A3", "A3 Sportback"],
    "A4": ["A4", "A4 Allroad"],
    "A6": ["A6", "A6 Quattro"],
    "Q3": ["Q3", "Q3 S Line"],
    "Q5": ["Q5", "Q5 Sportback"],
    "Q7": ["Q7", "Q7 Premium"],
    "Q8": ["Q8", "Q8 e-tron"],

    # Lexus
    "RX": ["RX", "RX 350", "RX 450h"],
    "NX": ["NX", "NX 300", "NX 450h"],
    "ES": ["ES", "ES 350", "ES 300h"],
    "IS": ["IS", "IS 350", "IS 300"],
    "GX": ["GX", "GX 460"],
    "LX": ["LX", "LX 600"],

    # Hyundai
    "Elantra": ["Elantra", "Elantra Hybrid", "Elantra N"],
    "Sonata": ["Sonata", "Sonata Hybrid"],
    "Tucson": ["Tucson", "Tucson Hybrid"],
    "Santa Fe": ["Santa Fe", "Santa Fe Hybrid"],
    "Palisade": ["Palisade", "Palisade Calligraphy"],

    # Kia
    "Forte": ["Forte", "Forte GT"],
    "Optima": ["Optima", "Optima Hybrid"],
    "Sorento": ["Sorento", "Sorento Hybrid"],
    "Sportage": ["Sportage", "Sportage Hybrid"],
    "Telluride": ["Telluride", "Telluride SX"],

    # Miscellaneous
    "Range Rover": ["Range Rover", "Range Rover Sport"],
    "Defender": ["Defender", "Defender 90", "Defender 110"],
    "911": ["911", "911 Carrera", "911 Turbo"],
    "Cayenne": ["Cayenne", "Cayenne Coupe"],
    "Macan": ["Macan", "Macan S"]
}
def standardize_model(model_name):
    for standard, variations in model_mapping.items():
        if model_name in variations:
            return standard
    return model_name  # Keep original if no match
data['model'] = data['model'].map(standardize_model)

#Save cleaned file
cleaned_file_path=r"C:\Users\arava\Desktop\Portfolio\Project 1\Data\cleaned_car_prices.csv"
data.to_csv(cleaned_file_path,index=False)
print("File Cleaned and Saved")