"""
Example of a radiation calculation
"""
__author__ = "Prageeth Jayathissa"
__copyright__ = "Copyright 2016, Architecture and Building Systems - ETH Zurich"
__credits__ = []
__license__ = "MIT"
__version__ = "0.1"
__maintainer__ = "Prageeth Jayathissa"
__email__ = "jayathissa@arch.ethz.ch"
__status__ = "Production"


import sys
import os

# Set root folder one level up, just for this example
mainPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, mainPath)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
from building_physics import Building  # Importing Building Class
import supply_system
import emission_system
from radiation import Location
from radiation import Window


# Initialise the Location with a weather file
Zurich = Location(path=os.path.join(
    mainPath, 'auxiliary', 'Zurich-Kloten_2013.epw'))

# Set the hour of the year for determination of the solar angles
# 9:00 am 16 June
hoy = 3993

# Determine the solar azimuth and altitude angle
Altitude, Azimuth = Zurich.calc_sun_position(year=2015, hoy=hoy)

# Define Windows
SouthWindow = Window(azimuth_tilt=0, alititude_tilt=90, glass_solar_transmittance=0.7,
                     glass_light_transmittance=0.8, area=1)
EastWindow = Window(azimuth_tilt=90, alititude_tilt=90, glass_solar_transmittance=0.7,
                    glass_light_transmittance=0.8, area=1)
WestWindow = Window(azimuth_tilt=180, alititude_tilt=90, glass_solar_transmittance=0.7,
                    glass_light_transmittance=0.8, area=1)
NorthWindow = Window(azimuth_tilt=270, alititude_tilt=90, glass_solar_transmittance=0.7,
                     glass_light_transmittance=0.8, area=1)
RoofAtrium = Window(azimuth_tilt=0, alititude_tilt=0, glass_solar_transmittance=0.7,
                    glass_light_transmittance=0.8, area=1)

# Loop through all windows
for selected_window in [SouthWindow, EastWindow, WestWindow, NorthWindow, RoofAtrium]:
    selected_window.calc_solar_gains(sun_altitude=Altitude, sun_azimuth=Azimuth,
                                     normal_direct_radiation=Zurich.weather_data[
                                         'dirnorrad_Whm2'][hoy],
                                     horizontal_diffuse_radiation=Zurich.weather_data['difhorrad_Whm2'][hoy])
    selected_window.calc_illuminance(sun_altitude=Altitude, sun_azimuth=Azimuth,
                                     normal_direct_illuminance=Zurich.weather_data[
                                         'dirnorillum_lux'][hoy],
                                     horizontal_diffuse_illuminance=Zurich.weather_data['difhorillum_lux'][hoy])

print(SouthWindow.incident_solar)
print(EastWindow.incident_solar)
print(WestWindow.incident_solar)
print(NorthWindow.incident_solar)
print(RoofAtrium.incident_solar)

print(SouthWindow.solar_gains)
print(EastWindow.solar_gains)
print(WestWindow.solar_gains)
print(NorthWindow.solar_gains)
print(RoofAtrium.solar_gains)

print(SouthWindow.transmitted_illuminance)
print(EastWindow.transmitted_illuminance)
print(WestWindow.transmitted_illuminance)
print(NorthWindow.transmitted_illuminance)
print(RoofAtrium.transmitted_illuminance)
