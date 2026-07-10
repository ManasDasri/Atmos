# waqi_service.py - WITH SENSOR LOCATIONS FOR MAP DEPLOYMENT

import requests
import random
import os

WAQI_TOKEN = os.getenv("WAQI_API_KEY", "cf4a1a6815fac27dd20757d4052d8b516b847950")

# COMPREHENSIVE BENGALURU ZONES WITH SENSOR DEPLOYMENT LOCATIONS
# Each zone has 'sensor_locations' with specific landmarks for physical sensor placement
BENGALURU_ZONES = [
    # ==================================================================
    # NORTH BENGALURU
    # ==================================================================
    
    # Yelahanka Region
    {
        "name": "Yelahanka Old Town",
        "traffic": "Medium",
        "center": [13.1007, 77.5963],
        "sensor_locations": [
            {"name": "Yelahanka Bus Stand", "landmark": "Main Bus Terminal", "coords": [13.1007, 77.5963]},
            {"name": "Yelahanka Market", "landmark": "Town Market Area", "coords": [13.1020, 77.5980]}
        ]
    },
    {
        "name": "Yelahanka New Town",
        "traffic": "Medium",
        "center": [13.0892, 77.5964],
        "sensor_locations": [
            {"name": "Yelahanka New Town Main Road", "landmark": "Shopping Complex", "coords": [13.0892, 77.5964]},
            {"name": "Yelahanka Lake Road", "landmark": "Lake Vicinity", "coords": [13.0905, 77.5980]}
        ]
    },
    
    # Hebbal & Surroundings
    {
        "name": "Hebbal",
        "traffic": "High",
        "center": [13.0358, 77.5970],
        "sensor_locations": [
            {"name": "Hebbal Flyover", "landmark": "Main Flyover Junction", "coords": [13.0348, 77.5988]},
            {"name": "Hebbal BEL Circle", "landmark": "BEL Road Junction", "coords": [13.0368, 77.5950]},
            {"name": "Hebbal Metro Station", "landmark": "Metro Station Area", "coords": [13.0375, 77.5995]}
        ]
    },
    {
        "name": "Nagawara",
        "traffic": "Medium",
        "center": [13.0450, 77.6020],
        "sensor_locations": [
            {"name": "Nagawara Lake Park", "landmark": "Lake Park Entrance", "coords": [13.0475, 77.6055]},
            {"name": "Nagawara Main Road", "landmark": "Main Junction", "coords": [13.0450, 77.6020]}
        ]
    },
    {
        "name": "HBR Layout 1st Block",
        "traffic": "High",
        "center": [13.0290, 77.6380],
        "sensor_locations": [
            {"name": "HBR 1st Block Main Road", "landmark": "Shopping Area", "coords": [13.0290, 77.6380]},
            {"name": "HBR Layout Circle", "landmark": "Main Circle", "coords": [13.0305, 77.6395]}
        ]
    },
    {
        "name": "RT Nagar",
        "traffic": "High",
        "center": [13.0196, 77.5969],
        "sensor_locations": [
            {"name": "RT Nagar Main Road", "landmark": "Commercial Area", "coords": [13.0196, 77.5969]},
            {"name": "RT Nagar BEL Road", "landmark": "BEL Road Junction", "coords": [13.0220, 77.5945]}
        ]
    },
    
    # Manyata Tech Park
    {
        "name": "Manyata Tech Park Main Gate",
        "traffic": "High",
        "center": [13.0380, 77.6150],
        "sensor_locations": [
            {"name": "Manyata Main Gate", "landmark": "Tech Park Entrance", "coords": [13.0380, 77.6150]},
            {"name": "Manyata Food Court", "landmark": "Central Food Court", "coords": [13.0395, 77.6165]},
            {"name": "Manyata Block 2 Lobby", "landmark": "Block 2 Entrance", "coords": [13.0410, 77.6180]}
        ]
    },
    {
        "name": "Thanisandra Main Road",
        "traffic": "High",
        "center": [13.0520, 77.6250],
        "sensor_locations": [
            {"name": "Thanisandra Junction", "landmark": "Main Road Junction", "coords": [13.0520, 77.6250]},
            {"name": "Thanisandra Village", "landmark": "Village Center", "coords": [13.0545, 77.6195]}
        ]
    },
    
    # ==================================================================
    # NORTHEAST BENGALURU
    # ==================================================================
    
    # Banaswadi Region
    {
        "name": "Banaswadi",
        "traffic": "High",
        "center": [13.0157, 77.6516],
        "sensor_locations": [
            {"name": "Banaswadi Railway Station", "landmark": "Railway Station Road", "coords": [13.0140, 77.6495]},
            {"name": "Banaswadi Main Market", "landmark": "Main Market Area", "coords": [13.0175, 77.6535]}
        ]
    },
    {
        "name": "Kammanahalli",
        "traffic": "High",
        "center": [13.0098, 77.6372],
        "sensor_locations": [
            {"name": "Kammanahalli Main Road", "landmark": "Main Commercial Street", "coords": [13.0115, 77.6390]},
            {"name": "Kammanahalli Circle", "landmark": "Traffic Circle", "coords": [13.0098, 77.6372]}
        ]
    },
    {
        "name": "Kalyan Nagar",
        "traffic": "High",
        "center": [13.0280, 77.6383],
        "sensor_locations": [
            {"name": "Kalyan Nagar Metro Station", "landmark": "Metro Station Plaza", "coords": [13.0265, 77.6360]},
            {"name": "Kalyan Nagar Main Road", "landmark": "Commercial Hub", "coords": [13.0295, 77.6405]},
            {"name": "Kalyan Nagar 100ft Road", "landmark": "100 Feet Road", "coords": [13.0285, 77.6420]}
        ]
    },
    {
        "name": "Ramamurthy Nagar",
        "traffic": "High",
        "center": [13.0107, 77.6818],
        "sensor_locations": [
            {"name": "Ramamurthy Nagar Main Road", "landmark": "Main Commercial Area", "coords": [13.0125, 77.6840]},
            {"name": "Ramamurthy Nagar A Block", "landmark": "Residential Hub", "coords": [13.0085, 77.6795]}
        ]
    },
    
    # Mahadevapura & Tech Parks
    {
        "name": "Mahadevapura",
        "traffic": "High",
        "center": [12.9956, 77.6989],
        "sensor_locations": [
            {"name": "Mahadevapura Main Junction", "landmark": "ORR Junction", "coords": [12.9975, 77.7010]},
            {"name": "Mahadevapura Village", "landmark": "Village Center", "coords": [12.9956, 77.6989]}
        ]
    },
    {
        "name": "Doddanekundi",
        "traffic": "High",
        "center": [12.9805, 77.7185],
        "sensor_locations": [
            {"name": "Doddanekundi Circle", "landmark": "Main Circle", "coords": [12.9785, 77.7165]},
            {"name": "Doddanekundi Main Road", "landmark": "Commercial Area", "coords": [12.9825, 77.7205]}
        ]
    },
    {
        "name": "Horamavu Main Road",
        "traffic": "High",
        "center": [13.0290, 77.6680],
        "sensor_locations": [
            {"name": "Horamavu Main Junction", "landmark": "Main Road Junction", "coords": [13.0290, 77.6680]},
            {"name": "Horamavu Agara", "landmark": "Residential Area", "coords": [13.0315, 77.6720]}
        ]
    },
    
    # ==================================================================
    # EAST BENGALURU
    # ==================================================================
    
    # Whitefield
    {
        "name": "Whitefield Main Road",
        "traffic": "High",
        "center": [12.9716, 77.7502],
        "sensor_locations": [
            {"name": "Whitefield Forum Mall", "landmark": "Forum Mall Entrance", "coords": [12.9695, 77.7485]},
            {"name": "Whitefield Main Junction", "landmark": "Main Traffic Junction", "coords": [12.9716, 77.7502]},
            {"name": "Whitefield Railway Station", "landmark": "Railway Station Area", "coords": [12.9755, 77.7425]}
        ]
    },
    {
        "name": "Whitefield ITPL Main Road",
        "traffic": "High",
        "center": [12.9852, 77.7271],
        "sensor_locations": [
            {"name": "ITPL Main Gate", "landmark": "Tech Park Main Entrance", "coords": [12.9870, 77.7295]},
            {"name": "ITPL Block B", "landmark": "Block B Lobby", "coords": [12.9885, 77.7320]}
        ]
    },
    {
        "name": "Kadugodi",
        "traffic": "Medium",
        "center": [12.9920, 77.7545],
        "sensor_locations": [
            {"name": "Kadugodi Tree Park", "landmark": "Park Entrance", "coords": [12.9945, 77.7570]},
            {"name": "Kadugodi Main Road", "landmark": "Main Junction", "coords": [12.9920, 77.7545]}
        ]
    },
    {
        "name": "Varthur Main Road",
        "traffic": "High",
        "center": [12.9375, 77.7551],
        "sensor_locations": [
            {"name": "Varthur Main Junction", "landmark": "Main Road Junction", "coords": [12.9375, 77.7551]},
            {"name": "Varthur Lake Road", "landmark": "Lake Vicinity", "coords": [12.9335, 77.7515]}
        ]
    },
    
    # Marathahalli
    {
        "name": "Marathahalli Bridge",
        "traffic": "High",
        "center": [12.9591, 77.7010],
        "sensor_locations": [
            {"name": "Marathahalli Bridge Junction", "landmark": "Bridge Underpass", "coords": [12.9591, 77.7010]},
            {"name": "Marathahalli HAL Road", "landmark": "HAL Road Junction", "coords": [12.9555, 77.6975]}
        ]
    },
    
    # Indiranagar
    {
        "name": "Indiranagar",
        "traffic": "High",
        "center": [12.9716, 77.6412],
        "sensor_locations": [
            {"name": "Indiranagar 100 Feet Road", "landmark": "Main 100 Feet Road", "coords": [12.9735, 77.6435]},
            {"name": "Indiranagar Metro Station", "landmark": "Metro Station Plaza", "coords": [12.9710, 77.6395]},
            {"name": "Indiranagar 12th Main", "landmark": "12th Main Commercial", "coords": [12.9780, 77.6405]}
        ]
    },
    {
        "name": "Domlur",
        "traffic": "High",
        "center": [12.9611, 77.6387],
        "sensor_locations": [
            {"name": "Domlur Flyover", "landmark": "Flyover Junction", "coords": [12.9595, 77.6365]},
            {"name": "Domlur Inner Ring Road", "landmark": "Inner Ring Road", "coords": [12.9575, 77.6345]}
        ]
    },
    {
        "name": "HAL Old Airport Road",
        "traffic": "High",
        "center": [12.9630, 77.6850],
        "sensor_locations": [
            {"name": "HAL Airport Road Main", "landmark": "Main Road", "coords": [12.9630, 77.6850]},
            {"name": "HAL 2nd Stage", "landmark": "Residential Area", "coords": [12.9745, 77.6450]}
        ]
    },
    
    # Koramangala
    {
        "name": "Koramangala 5th Block",
        "traffic": "High",
        "center": [12.9320, 77.6195],
        "sensor_locations": [
            {"name": "Koramangala 5th Block Jyoti Nivas", "landmark": "Jyoti Nivas College", "coords": [12.9305, 77.6175]},
            {"name": "Koramangala 5th Block Main", "landmark": "5th Block Main Road", "coords": [12.9320, 77.6195]}
        ]
    },
    {
        "name": "Koramangala 6th Block",
        "traffic": "High",
        "center": [12.9342, 77.6101],
        "sensor_locations": [
            {"name": "Forum Mall Koramangala", "landmark": "Forum Mall Entrance", "coords": [12.9325, 77.6085]},
            {"name": "Koramangala 6th Block Main", "landmark": "Main Road", "coords": [12.9342, 77.6101]}
        ]
    },
    {
        "name": "Koramangala 7th Block",
        "traffic": "High",
        "center": [12.9385, 77.6280],
        "sensor_locations": [
            {"name": "Koramangala 7th Block BDA", "landmark": "BDA Complex", "coords": [12.9370, 77.6265]},
            {"name": "Koramangala 80 Feet Road", "landmark": "80 Feet Road", "coords": [12.9365, 77.6235]}
        ]
    },
    
    # ==================================================================
    # SOUTHEAST BENGALURU
    # ==================================================================
    
    # Sarjapur Road
    {
        "name": "Sarjapur Road Main",
        "traffic": "High",
        "center": [12.9019, 77.6881],
        "sensor_locations": [
            {"name": "Sarjapur Wipro Campus", "landmark": "Wipro Main Gate", "coords": [12.9045, 77.6825]},
            {"name": "Sarjapur RGA Tech Park", "landmark": "Tech Park Entrance", "coords": [12.9025, 77.6845]},
            {"name": "Sarjapur Main Junction", "landmark": "Main Road Junction", "coords": [12.9019, 77.6881]}
        ]
    },
    {
        "name": "Bellandur",
        "traffic": "High",
        "center": [12.9266, 77.6733],
        "sensor_locations": [
            {"name": "Bellandur ORR Junction", "landmark": "Outer Ring Road Junction", "coords": [12.9250, 77.6755]},
            {"name": "Bellandur Lake Road", "landmark": "Lake Area", "coords": [12.9285, 77.6795]}
        ]
    },
    {
        "name": "Kadubeesanahalli",
        "traffic": "High",
        "center": [12.9350, 77.6970],
        "sensor_locations": [
            {"name": "Kadubeesanahalli ORR", "landmark": "ORR Junction", "coords": [12.9330, 77.6995]},
            {"name": "Kadubeesanahalli Main", "landmark": "Main Road", "coords": [12.9350, 77.6970]}
        ]
    },
    
    # HSR Layout
    {
        "name": "HSR Layout Sector 1",
        "traffic": "High",
        "center": [12.9145, 77.6352],
        "sensor_locations": [
            {"name": "HSR Sector 1 Main Road", "landmark": "27th Main Road", "coords": [12.9116, 77.6381]},
            {"name": "HSR BDA Complex", "landmark": "BDA Office Complex", "coords": [12.9105, 77.6365]},
            {"name": "HSR Club Road", "landmark": "HSR Club Area", "coords": [12.9135, 77.6345]}
        ]
    },
    {
        "name": "HSR Layout Sector 2",
        "traffic": "High",
        "center": [12.9095, 77.6335],
        "sensor_locations": [
            {"name": "HSR Sector 2 Main", "landmark": "Sector 2 Main Road", "coords": [12.9095, 77.6335]},
            {"name": "HSR ORR Junction", "landmark": "ORR Exit", "coords": [12.9088, 77.6410]}
        ]
    },
    
    # BTM Layout
    {
        "name": "BTM Layout 2nd Stage",
        "traffic": "High",
        "center": [12.9165, 77.6101],
        "sensor_locations": [
            {"name": "BTM Udupi Garden", "landmark": "Udupi Garden Junction", "coords": [12.9180, 77.6125]},
            {"name": "BTM Water Tank", "landmark": "Water Tank Circle", "coords": [12.9145, 77.6065]},
            {"name": "BTM 100 Feet Road", "landmark": "100 Feet Road", "coords": [12.9165, 77.6101]}
        ]
    },
    {
        "name": "Madiwala",
        "traffic": "High",
        "center": [12.9140, 77.6180],
        "sensor_locations": [
            {"name": "Madiwala Market", "landmark": "Main Market Area", "coords": [12.9155, 77.6195]},
            {"name": "Madiwala Police Station", "landmark": "Police Station Road", "coords": [12.9125, 77.6165]}
        ]
    },
    
    # ==================================================================
    # SOUTH BENGALURU
    # ==================================================================
    
    # Jayanagar
    {
        "name": "Jayanagar 4th Block",
        "traffic": "Medium",
        "center": [12.9250, 77.5938],
        "sensor_locations": [
            {"name": "Jayanagar 4th Block Shopping Complex", "landmark": "Shopping Complex", "coords": [12.9235, 77.5925]},
            {"name": "Jayanagar 4th Block Main Road", "landmark": "Main Road", "coords": [12.9250, 77.5938]}
        ]
    },
    {
        "name": "Jayanagar 5th Block",
        "traffic": "Medium",
        "center": [12.9225, 77.5995],
        "sensor_locations": [
            {"name": "Jayanagar 5th Block Main", "landmark": "5th Block Center", "coords": [12.9225, 77.5995]},
            {"name": "Jayanagar East End", "landmark": "East End Circle", "coords": [12.9145, 77.6085]}
        ]
    },
    {
        "name": "South End Circle",
        "traffic": "High",
        "center": [12.9420, 77.5950],
        "sensor_locations": [
            {"name": "South End Circle Ashoka Pillar", "landmark": "Ashoka Pillar Junction", "coords": [12.9435, 77.5965]},
            {"name": "South End Circle Main Road", "landmark": "Main Circle", "coords": [12.9420, 77.5950]}
        ]
    },
    
    # JP Nagar
    {
        "name": "JP Nagar 1st Phase",
        "traffic": "High",
        "center": [12.9073, 77.5850],
        "sensor_locations": [
            {"name": "JP Nagar 1st Phase Main", "landmark": "Phase 1 Main Road", "coords": [12.9073, 77.5850]},
            {"name": "JP Nagar BMTC Depot", "landmark": "BMTC Bus Depot", "coords": [12.9045, 77.5805]}
        ]
    },
    {
        "name": "JP Nagar 7th Phase",
        "traffic": "Medium",
        "center": [12.8910, 77.5870],
        "sensor_locations": [
            {"name": "JP Nagar 7th Phase Metro", "landmark": "Metro Station", "coords": [12.8925, 77.5885]},
            {"name": "JP Nagar 7th Phase Main", "landmark": "Main Road", "coords": [12.8910, 77.5870]}
        ]
    },
    
    # Banashankari
    {
        "name": "Banashankari 2nd Stage",
        "traffic": "Medium",
        "center": [12.9280, 77.5515],
        "sensor_locations": [
            {"name": "Banashankari Temple Road", "landmark": "Temple Main Road", "coords": [12.9265, 77.5495]},
            {"name": "Banashankari 2nd Stage Main", "landmark": "Stage Main Road", "coords": [12.9280, 77.5515]}
        ]
    },
    {
        "name": "Banashankari 3rd Stage",
        "traffic": "Medium",
        "center": [12.9250, 77.5487],
        "sensor_locations": [
            {"name": "Banashankari 3rd Stage BDA", "landmark": "BDA Complex", "coords": [12.9235, 77.5465]},
            {"name": "IIMB Road", "landmark": "IIM Bangalore Road", "coords": [12.9198, 77.5380]}
        ]
    },
    
    # Basavanagudi
    {
        "name": "Basavanagudi",
        "traffic": "Medium",
        "center": [12.9423, 77.5739],
        "sensor_locations": [
            {"name": "Gandhi Bazaar", "landmark": "Gandhi Bazaar Main Road", "coords": [12.9455, 77.5775]},
            {"name": "Bull Temple Road", "landmark": "Bull Temple", "coords": [12.9438, 77.5755]}
        ]
    },
    
    # ==================================================================
    # SOUTHWEST BENGALURU
    # ==================================================================
    
    # Electronic City
    {
        "name": "Electronic City Phase 1",
        "traffic": "High",
        "center": [12.8456, 77.6603],
        "sensor_locations": [
            {"name": "Electronic City Infosys Gate", "landmark": "Infosys Main Gate", "coords": [12.8475, 77.6625]},
            {"name": "Electronic City Metro Station", "landmark": "Metro Station", "coords": [12.8408, 77.6590]},
            {"name": "Electronic City Hosur Road", "landmark": "Hosur Road Junction", "coords": [12.8435, 77.6555]}
        ]
    },
    {
        "name": "Electronic City Phase 2",
        "traffic": "High",
        "center": [12.8398, 77.6770],
        "sensor_locations": [
            {"name": "Electronic City TCS Campus", "landmark": "TCS Main Gate", "coords": [12.8415, 77.6795]},
            {"name": "Electronic City Phase 2 Main", "landmark": "Phase 2 Main Road", "coords": [12.8398, 77.6770]}
        ]
    },
    
    # Bannerghatta Road
    {
        "name": "Bannerghatta Road Main",
        "traffic": "High",
        "center": [12.8810, 77.6040],
        "sensor_locations": [
            {"name": "Bannerghatta Road HSR Link", "landmark": "HSR Layout Link", "coords": [12.8995, 77.6115]},
            {"name": "Bilekahalli Metro Station", "landmark": "Metro Station", "coords": [12.8945, 77.6145]}
        ]
    },
    {
        "name": "Gottigere",
        "traffic": "Medium",
        "center": [12.8765, 77.6065],
        "sensor_locations": [
            {"name": "Gottigere Main Road", "landmark": "Main Junction", "coords": [12.8785, 77.6085]},
            {"name": "Gottigere Village", "landmark": "Village Center", "coords": [12.8765, 77.6065]}
        ]
    },
    
    # ==================================================================
    # WEST BENGALURU
    # ==================================================================
    
    # Rajajinagar
    {
        "name": "Rajajinagar",
        "traffic": "Medium",
        "center": [12.9916, 77.5544],
        "sensor_locations": [
            {"name": "Rajajinagar Main Road", "landmark": "Main Commercial Road", "coords": [12.9935, 77.5565]},
            {"name": "Rajajinagar Industrial Estate", "landmark": "Industrial Area", "coords": [12.9895, 77.5515]}
        ]
    },
    {
        "name": "Mahalaxmi Layout",
        "traffic": "Medium",
        "center": [12.9780, 77.5420],
        "sensor_locations": [
            {"name": "Mahalaxmi Layout Metro", "landmark": "Metro Station", "coords": [12.9795, 77.5440]},
            {"name": "Mahalaxmi Layout Main Road", "landmark": "Main Road", "coords": [12.9765, 77.5395]}
        ]
    },
    
    # Malleshwaram
    {
        "name": "Malleshwaram",
        "traffic": "Medium",
        "center": [13.0052, 77.5703],
        "sensor_locations": [
            {"name": "Malleshwaram 18th Cross", "landmark": "18th Cross Main Road", "coords": [13.0075, 77.5725]},
            {"name": "Mantri Square Mall", "landmark": "Mall Entrance", "coords": [13.0095, 77.5745]},
            {"name": "Malleshwaram Circle", "landmark": "Main Circle", "coords": [13.0020, 77.5670]}
        ]
    },
    
    # Peenya Industrial Area
    {
        "name": "Peenya Industrial Area",
        "traffic": "High",
        "center": [13.0297, 77.5158],
        "sensor_locations": [
            {"name": "Peenya 1st Stage KSSIDC", "landmark": "KSSIDC Complex", "coords": [13.0365, 77.5085]},
            {"name": "Peenya Gate 1", "landmark": "Main Gate 1", "coords": [13.0320, 77.5135]},
            {"name": "Peenya BMTC Depot", "landmark": "Bus Depot", "coords": [13.0335, 77.5125]}
        ]
    },
    
    # Yeshwanthpur
    {
        "name": "Yeshwanthpur",
        "traffic": "High",
        "center": [13.0280, 77.5385],
        "sensor_locations": [
            {"name": "Yeshwanthpur Railway Station", "landmark": "Railway Station", "coords": [13.0295, 77.5365]},
            {"name": "Yeshwanthpur Industrial Area", "landmark": "Industrial Zone", "coords": [13.0250, 77.5325]}
        ]
    },
    
    # Vijayanagar
    {
        "name": "Vijayanagar",
        "traffic": "High",
        "center": [12.9716, 77.5322],
        "sensor_locations": [
            {"name": "Vijayanagar Main Road", "landmark": "Main Commercial Street", "coords": [12.9735, 77.5345]},
            {"name": "Vijayanagar Chord Road", "landmark": "Chord Road Junction", "coords": [12.9716, 77.5322]}
        ]
    },
    
    # ==================================================================
    # CENTRAL BENGALURU
    # ==================================================================
    
    # MG Road & Brigade
    {
        "name": "MG Road",
        "traffic": "High",
        "center": [12.9750, 77.6069],
        "sensor_locations": [
            {"name": "MG Road Metro Station", "landmark": "Metro Station Plaza", "coords": [12.9765, 77.6085]},
            {"name": "Trinity Circle", "landmark": "Trinity Circle Junction", "coords": [12.9795, 77.6095]},
            {"name": "Brigade Road Junction", "landmark": "Brigade Road", "coords": [12.9716, 77.6089]}
        ]
    },
    {
        "name": "Commercial Street",
        "traffic": "High",
        "center": [12.9830, 77.6085],
        "sensor_locations": [
            {"name": "Commercial Street Main", "landmark": "Main Shopping Area", "coords": [12.9830, 77.6085]},
            {"name": "Russell Market", "landmark": "Market Area", "coords": [12.9845, 77.6105]}
        ]
    },
    {
        "name": "Shivajinagar",
        "traffic": "High",
        "center": [12.9809, 77.6022],
        "sensor_locations": [
            {"name": "Shivajinagar Bus Stand", "landmark": "Main Bus Terminal", "coords": [12.9825, 77.6040]},
            {"name": "Shivajinagar Hospital Road", "landmark": "Hospital Area", "coords": [12.9795, 77.6005]}
        ]
    },
    
    # Cubbon Park Area
    {
        "name": "Vidhana Soudha",
        "traffic": "High",
        "center": [12.9795, 77.5908],
        "sensor_locations": [
            {"name": "Vidhana Soudha Main Gate", "landmark": "Government Building", "coords": [12.9795, 77.5908]},
            {"name": "High Court Road", "landmark": "High Court", "coords": [12.9815, 77.5895]}
        ]
    },
]

def generate_fallback_data():
    """Generate realistic fallback AQI data"""
    zones = []
    
    for zone in BENGALURU_ZONES:
        base_pm25 = random.uniform(60, 150)
        
        if zone['traffic'] == 'High':
            pm25 = base_pm25 * random.uniform(1.1, 1.3)
        elif zone['traffic'] == 'Medium':
            pm25 = base_pm25 * random.uniform(0.9, 1.1)
        else:
            pm25 = base_pm25 * random.uniform(0.7, 0.9)
        
        zones.append({
            'name': zone['name'],
            'pm25': round(pm25, 1),
            'traffic': zone['traffic'],
            'center': zone['center']
        })
    
    return {
        'source': 'fallback',
        'zones': zones,
        'timestamp': 'simulated'
    }

def fetch_live_aqi():
    """Fetch live AQI data from WAQI API"""
    try:
        url = f"https://api.waqi.info/feed/bangalore/?token={WAQI_TOKEN}"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data.get('status') == 'ok':
                aqi_data = data['data']
                iaqi = aqi_data.get('iaqi', {})
                
                if 'pm25' in iaqi:
                    base_pm25 = iaqi['pm25'].get('v', 75)
                elif 'aqi' in aqi_data:
                    base_pm25 = aqi_data['aqi'] * 0.8
                else:
                    base_pm25 = 75
                
                print(f"✓ WAQI API: Base PM2.5 = {base_pm25}")
                
                zones = []
                for zone in BENGALURU_ZONES:
                    variation = random.uniform(0.7, 1.3)
                    if zone['traffic'] == 'High':
                        variation *= 1.2
                    elif zone['traffic'] == 'Low':
                        variation *= 0.8
                    
                    zone_pm25 = base_pm25 * variation
                    
                    zones.append({
                        'name': zone['name'],
                        'pm25': round(zone_pm25, 1),
                        'traffic': zone['traffic'],
                        'center': zone['center']
                    })
                
                return {
                    'source': 'waqi_api',
                    'zones': zones,
                    'timestamp': aqi_data.get('time', {}).get('s', 'unknown'),
                    'base_aqi': round(base_pm25, 1)
                }
        
        print(f"⚠ WAQI API returned {response.status_code}, using fallback")
        return generate_fallback_data()
        
    except Exception as e:
        print(f"⚠ WAQI API error: {e}, using fallback")
        return generate_fallback_data()

def get_zone_aqi(zone_name):
    """Get AQI for a specific zone"""
    data = fetch_live_aqi()
    zone = next((z for z in data['zones'] if z['name'].lower() == zone_name.lower()), None)
    return zone

if __name__ == "__main__":
    print("Testing WAQI service with sensor locations...")
    data = fetch_live_aqi()
    print(f"\n✓ Source: {data['source']}")
    print(f"✓ Total zones: {len(data['zones'])}")
    
    if 'base_aqi' in data:
        print(f"✓ Base AQI: {data['base_aqi']}")
    
    # Show sample zones with sensor locations
    print(f"\n📍 Sample zones with sensor deployment locations:")
    for zone_data in BENGALURU_ZONES[:5]:
        print(f"\n  Zone: {zone_data['name']}")
        print(f"  Traffic: {zone_data['traffic']}")
        print(f"  Center: {zone_data['center']}")
        print(f"  Sensor Locations:")
        for loc in zone_data.get('sensor_locations', []):
            print(f"    - {loc['name']}")
            print(f"      Landmark: {loc['landmark']}")
            print(f"      Coords: {loc['coords']}")
    
    # Count total possible sensor locations
    total_locations = sum(len(z.get('sensor_locations', [])) for z in BENGALURU_ZONES)
    print(f"\n" + "="*60)
    print(f"✓ Total zones defined: {len(BENGALURU_ZONES)}")
    print(f"✓ Total sensor deployment locations available: {total_locations}")
    print(f"✓ Average locations per zone: {total_locations/len(BENGALURU_ZONES):.1f}")
    print("="*60)