import sys
import os


# Set root folder one level up, just for this example
mainPath = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, mainPath)

import unittest
import numpy as np
import pandas as pd
from radiation import Location
from radiation import Window
import math


class TestRadiation(unittest.TestCase):

    def test_sunPosition(self):

        Zurich = Location(epwfile_path=os.path.join(
            mainPath, 'auxiliary', 'Zurich-Kloten_2013.epw'))

        Azimuth = []
        Altitude = []
        Sunnyhoy = []

        for hoy in range(8760):
            angles = Zurich.calc_sun_position(
                latitude_deg=47.480, longitude_deg=8.536, year=2015, hoy=hoy)

            Altitude.append(angles[0])
            Azimuth.append(angles[1])
            Sunnyhoy.append(hoy + 1)

        sunPosition = pd.read_csv(os.path.join(
            mainPath, 'auxiliary', 'SunPosition.csv'), skiprows=1)

        transSunPos = sunPosition.transpose()
        hoy_check = transSunPos.index.tolist()
        hoy_check = [float(ii) for ii in hoy_check]
        Azimuth_check = (180 - transSunPos[1]).tolist()

        Altitude_check = transSunPos[0].tolist()

        self.assertEqual(round(Altitude[9], 1), round(Altitude_check[1], 1))
        self.assertEqual(round(Azimuth[9], 1), round(Azimuth_check[1], 1))

        self.assertEqual(round(Altitude[3993], 1),
                         round(Altitude_check[2023], 1))
        self.assertEqual(round(Azimuth[3993], 1),
                         round(Azimuth_check[2023], 1))

        # Azimuth Angles go out of sync with data, however the sin and cosine
        # must still match
        self.assertEqual(round(Altitude[4000], 1),
                         round(Altitude_check[2030], 1))
        self.assertEqual(round(math.cos(math.radians(Azimuth[4000])), 1), round(
            math.cos(math.radians(Azimuth_check[2030])), 1))
        self.assertEqual(round(math.sin(math.radians(Azimuth[4000])), 1), round(
            math.sin(math.radians(Azimuth_check[2030])), 1))

    def test_windowSolarGains(self):

        hoy = 3993
        # 9:00 am 16 June 2015

        Zurich = Location(epwfile_path=os.path.join(
            mainPath, 'auxiliary', 'Zurich-Kloten_2013.epw'))
        Altitude, Azimuth = Zurich.calc_sun_position(
            latitude_deg=47.480, longitude_deg=8.536, year=2015, hoy=hoy)

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

        for selected_window in [SouthWindow, EastWindow, WestWindow, NorthWindow, RoofAtrium]:

            selected_window.calc_solar_gains(sun_altitude=Altitude, sun_azimuth=Azimuth,
                                             normal_direct_radiation=Zurich.weather_data[
                                                 'dirnorrad_Whm2'][hoy],
                                             horizontal_diffuse_radiation=Zurich.weather_data['difhorrad_Whm2'][hoy])

            selected_window.calc_illuminance(sun_altitude=Altitude, sun_azimuth=Azimuth,
                                             normal_direct_illuminance=Zurich.weather_data[
                                                 'dirnorillum_lux'][hoy],
                                             horizontal_diffuse_illuminance=Zurich.weather_data['difhorillum_lux'][hoy])

        self.assertEqual(round(SouthWindow.incident_solar, 2), 315.85)
        self.assertEqual(round(EastWindow.incident_solar, 2), 570.06)
        self.assertEqual(round(WestWindow.incident_solar, 2), 58.0)
        self.assertEqual(round(NorthWindow.incident_solar, 2), 58.0)
        self.assertEqual(round(RoofAtrium.incident_solar, 2), 855.87)

        self.assertEqual(round(SouthWindow.solar_gains, 2), 221.1)
        self.assertEqual(round(EastWindow.solar_gains, 2), 399.04)
        self.assertEqual(round(WestWindow.solar_gains, 2), 40.6)
        self.assertEqual(round(NorthWindow.solar_gains, 2), 40.6)
        self.assertEqual(round(RoofAtrium.solar_gains, 2), 599.11)

        self.assertEqual(
            round(SouthWindow.transmitted_illuminance, 2), 27330.46)
        self.assertEqual(
            round(EastWindow.transmitted_illuminance, 2), 47989.19)
        self.assertEqual(round(WestWindow.transmitted_illuminance, 2), 6375.2)
        self.assertEqual(round(NorthWindow.transmitted_illuminance, 2), 6375.2)
        self.assertEqual(
            round(RoofAtrium.transmitted_illuminance, 2), 72878.36)


if __name__ == '__main__':
    unittest.main()
