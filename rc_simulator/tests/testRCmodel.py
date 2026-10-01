import sys
import os
import unittest

# Set root folder one level up, just for this example
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..')))

from building_physics import Zone  # Importing Zone Class
import supply_system
import emission_system


class TestBuildingSim(unittest.TestCase):

    def test_NoHVACNoLight(self):
        t_out = 10
        t_m_prev = 22
        # Internal heat gains, in Watts
        internal_gains = 10

        # Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 2000

        # Illuminance after transmitting through the window
        ill = 44000  # Lumens

        # Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        # Set Zone Parameters
        Office = Zone(window_area=13.5,
                      walls_area=15.19 - 13.5,
                      floor_area=34.3,
                      room_vol=106.33,
                      total_internal_area=142.38,
                      lighting_load=11.7,
                      lighting_control=300,
                      lighting_utilisation_factor=0.45,
                      lighting_maintenance_factor=0.9,
                      u_walls=0.2,
                      u_windows=1.1,
                      ach_vent=1.5,
                      ach_infl=0.5,
                      ventilation_efficiency=0,
                      thermal_capacitance_per_floor_area=165000,
                      t_set_heating=20,
                      t_set_cooling=26,
                      max_cooling_energy_per_floor_area=-12,
                      max_heating_energy_per_floor_area=12,
                      heating_supply_system=supply_system.DirectHeater,
                      cooling_supply_system=supply_system.DirectCooler,
                      heating_emission_system=emission_system.AirConditioning,
                      cooling_emission_system=emission_system.AirConditioning,
                      )

        Office.solve_energy(
            internal_gains, solar_gains, t_out, t_m_prev)
        Office.solve_lighting(ill, occupancy)

        self.assertEqual(round(Office.t_m, 2), 22.33)
        self.assertEqual(Office.energy_demand, 0)
        self.assertEqual(round(Office.heating_sys_electricity, 2), 0)
        self.assertEqual(round(Office.cooling_sys_electricity, 2), 0)
        self.assertEqual(Office.lighting_demand, 0)

    def test_CoolingRequired(self):
        t_out = 25
        t_m_prev = 24
        # Internal heat gains, in Watts
        internal_gains = 10

        # Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 4000

        # Illuminance after transmitting through the window
        ill = 44000  # Lumens

        # Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        # Set Zone Parameters
        Office = Zone(window_area=13.5,
                      walls_area=15.19 - 13.5,
                      floor_area=34.3,
                      room_vol=106.33,
                      total_internal_area=142.38,
                      lighting_load=11.7,
                      lighting_control=300,
                      lighting_utilisation_factor=0.45,
                      lighting_maintenance_factor=0.9,
                      u_walls=0.2,
                      u_windows=1.1,
                      ach_vent=1.5,
                      ach_infl=0.5,
                      ventilation_efficiency=0,
                      thermal_capacitance_per_floor_area=165000,
                      t_set_heating=20,
                      t_set_cooling=26,
                      max_cooling_energy_per_floor_area=-12,
                      max_heating_energy_per_floor_area=12,
                      heating_supply_system=supply_system.DirectHeater,
                      cooling_supply_system=supply_system.DirectCooler,
                      heating_emission_system=emission_system.AirConditioning,
                      cooling_emission_system=emission_system.AirConditioning,
                      )

        Office.solve_energy(
            internal_gains, solar_gains, t_out, t_m_prev)
        Office.solve_lighting(ill, occupancy)

        self.assertEqual(round(Office.energy_demand, 2), -264.75)
        self.assertEqual(round(Office.cooling_sys_electricity, 2), 264.75)
        self.assertEqual(round(Office.heating_sys_electricity, 2), 0)
        self.assertEqual(round(Office.t_m, 2), 25.15)
        self.assertTrue(Office.has_cooling_demand)

        self.assertEqual(Office.lighting_demand, 0)

    def test_HeatingRequired(self):

        t_out = 10
        t_m_prev = 20
        # Internal heat gains, in Watts
        internal_gains = 10

        # Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 2000

        # Illuminance after transmitting through the window
        ill = 44000  # Lumens

        # Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        # Set Zone Parameters
        Office = Zone(window_area=13.5,
                      walls_area=15.19 - 13.5,
                      floor_area=34.3,
                      room_vol=106.33,
                      total_internal_area=142.38,
                      lighting_load=11.7,
                      lighting_control=300,
                      lighting_utilisation_factor=0.45,
                      lighting_maintenance_factor=0.9,
                      u_walls=0.2,
                      u_windows=1.1,
                      ach_vent=1.5,
                      ach_infl=0.5,
                      ventilation_efficiency=0,
                      thermal_capacitance_per_floor_area=165000,
                      t_set_heating=20,
                      t_set_cooling=26,
                      max_cooling_energy_per_floor_area=-12,
                      max_heating_energy_per_floor_area=12,
                      heating_supply_system=supply_system.DirectHeater,
                      cooling_supply_system=supply_system.DirectCooler,
                      heating_emission_system=emission_system.AirConditioning,
                      cooling_emission_system=emission_system.AirConditioning,
                      )

        Office.solve_energy(
            internal_gains, solar_gains, t_out, t_m_prev)
        Office.solve_lighting(ill, occupancy)

        self.assertEqual(round(Office.t_m, 2), 20.46)
        self.assertTrue(Office.has_heating_demand)
        self.assertEqual(round(Office.energy_demand, 2), 328.09)
        self.assertEqual(round(Office.heating_sys_electricity, 2), 328.09)
        self.assertEqual(round(Office.cooling_sys_electricity, 2), 0)
        self.assertEqual(Office.lighting_demand, 0)

    def test_MaxCoolingRequired(self):
        t_out = 30
        t_m_prev = 25
        # Internal heat gains, in Watts
        internal_gains = 10

        # Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 5000

        # Illuminance after transmitting through the window
        ill = 44000  # Lumens

        # Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        # Set Zone Parameters
        Office = Zone(window_area=13.5,
                      walls_area=15.19 - 13.5,
                      floor_area=34.3,
                      room_vol=106.33,
                      total_internal_area=142.38,
                      lighting_load=11.7,
                      lighting_control=300,
                      lighting_utilisation_factor=0.45,
                      lighting_maintenance_factor=0.9,
                      u_walls=0.2,
                      u_windows=1.1,
                      ach_vent=1.5,
                      ach_infl=0.5,
                      ventilation_efficiency=0,
                      thermal_capacitance_per_floor_area=165000,
                      t_set_heating=20,
                      t_set_cooling=26,
                      max_cooling_energy_per_floor_area=-12,
                      max_heating_energy_per_floor_area=12,
                      heating_supply_system=supply_system.DirectHeater,
                      cooling_supply_system=supply_system.DirectCooler,
                      heating_emission_system=emission_system.AirConditioning,
                      cooling_emission_system=emission_system.AirConditioning,
                      )

        Office.solve_energy(
            internal_gains, solar_gains, t_out, t_m_prev)
        Office.solve_lighting(ill, occupancy)

        self.assertEqual(round(Office.t_m, 2), 26.49)
        self.assertTrue(Office.has_cooling_demand)
        self.assertEqual(round(Office.energy_demand, 2), -411.6)
        self.assertEqual(round(Office.cooling_sys_electricity, 2), 411.6)
        self.assertEqual(round(Office.heating_sys_electricity, 2), 0)
        self.assertEqual(Office.lighting_demand, 0)

    def test_MaxHeatingRequired(self):

        t_out = 5
        t_m_prev = 19
        # Internal heat gains, in Watts
        internal_gains = 10

        # Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 2000

        # Illuminance after transmitting through the window
        ill = 44000  # Lumens

        # Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        # Set Zone Parameters
        Office = Zone(window_area=13.5,
                      walls_area=15.19 - 13.5,
                      floor_area=34.3,
                      room_vol=106.33,
                      total_internal_area=142.38,
                      lighting_load=11.7,
                      lighting_control=300,
                      lighting_utilisation_factor=0.45,
                      lighting_maintenance_factor=0.9,
                      u_walls=0.2,
                      u_windows=1.1,
                      ach_vent=1.5,
                      ach_infl=0.5,
                      ventilation_efficiency=0,
                      thermal_capacitance_per_floor_area=165000,
                      t_set_heating=20,
                      t_set_cooling=26,
                      max_cooling_energy_per_floor_area=-12,
                      max_heating_energy_per_floor_area=12,
                      heating_supply_system=supply_system.DirectHeater,
                      cooling_supply_system=supply_system.DirectCooler,
                      heating_emission_system=emission_system.AirConditioning,
                      cooling_emission_system=emission_system.AirConditioning,
                      )

        Office.solve_energy(
            internal_gains, solar_gains, t_out, t_m_prev)
        Office.solve_lighting(ill, occupancy)

        self.assertEqual(round(Office.t_m, 2), 19.39)
        self.assertTrue(Office.has_heating_demand)
        self.assertEqual(round(Office.energy_demand, 2), 411.6)
        self.assertEqual(round(Office.heating_sys_electricity, 2), 411.6)
        self.assertEqual(round(Office.cooling_sys_electricity, 2), 0)
        self.assertEqual(Office.lighting_demand, 0)

    def test_lightingrequired(self):

        t_out = 10
        t_m_prev = 22
        # Internal heat gains, in Watts
        internal_gains = 10

        # Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 2000

        # Illuminance after transmitting through the window
        ill = 4000  # Lumens

        # Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        # Set Zone Parameters
        Office = Zone(window_area=13.5,
                      walls_area=15.19 - 13.5,
                      floor_area=34.3,
                      room_vol=106.33,
                      total_internal_area=142.38,
                      lighting_load=11.7,
                      lighting_control=300,
                      lighting_utilisation_factor=0.45,
                      lighting_maintenance_factor=0.9,
                      u_walls=0.2,
                      u_windows=1.1,
                      ach_vent=1.5,
                      ach_infl=0.5,
                      ventilation_efficiency=0,
                      thermal_capacitance_per_floor_area=165000,
                      t_set_heating=20.0,
                      t_set_cooling=26.0,
                      max_cooling_energy_per_floor_area=-12.0,
                      max_heating_energy_per_floor_area=12.0,
                      heating_supply_system=supply_system.DirectHeater,
                      cooling_supply_system=supply_system.DirectCooler,
                      heating_emission_system=emission_system.AirConditioning,
                      cooling_emission_system=emission_system.AirConditioning,
                      )

        Office.solve_energy(
            internal_gains, solar_gains, t_out, t_m_prev)
        Office.solve_lighting(ill, occupancy)

        self.assertEqual(round(Office.t_m, 2), 22.33)
        self.assertEqual(Office.energy_demand, 0)
        self.assertEqual(round(Office.heating_sys_electricity, 2), 0)
        self.assertEqual(round(Office.cooling_sys_electricity, 2), 0)
        self.assertEqual(round(Office.lighting_demand, 2), 401.31)

    #     ###############################Tests with infiltration variation####

    def test_NoHVACNoLight_infl(self):
        t_out = 10
        t_m_prev = 22
        # Internal heat gains, in Watts
        internal_gains = 10

        # Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 2000

        # Illuminance after transmitting through the window
        ill = 44000  # Lumens

        # Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        # Set Zone Parameters
        Office = Zone(window_area=13.5,
                      walls_area=15.19 - 13.5,
                      floor_area=34.3,
                      room_vol=106.33,
                      total_internal_area=142.38,
                      lighting_load=11.7,
                      lighting_control=300,
                      lighting_utilisation_factor=0.45,
                      lighting_maintenance_factor=0.9,
                      u_walls=0.2,
                      u_windows=1.1,
                      ach_vent=1.5,
                      ach_infl=0.5,
                      ventilation_efficiency=0.66,
                      thermal_capacitance_per_floor_area=165000,
                      t_set_heating=20,
                      t_set_cooling=26,
                      max_cooling_energy_per_floor_area=-12,
                      max_heating_energy_per_floor_area=12,
                      heating_supply_system=supply_system.DirectHeater,
                      cooling_supply_system=supply_system.DirectCooler,
                      heating_emission_system=emission_system.AirConditioning,
                      cooling_emission_system=emission_system.AirConditioning,
                      )

        Office.solve_energy(
            internal_gains, solar_gains, t_out, t_m_prev)
        Office.solve_lighting(ill, occupancy)

        self.assertEqual(round(Office.t_m, 2), 22.44)
        self.assertEqual(Office.energy_demand, 0)
        self.assertEqual(round(Office.heating_sys_electricity, 2), 0)
        self.assertEqual(round(Office.cooling_sys_electricity, 2), 0)
        self.assertEqual(Office.lighting_demand, 0)

    def test_CoolingRequired_infl(self):
        t_out = 25
        t_m_prev = 24
        # Internal heat gains, in Watts
        internal_gains = 10

        # Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 4000

        # Illuminance after transmitting through the window
        ill = 44000  # Lumens

        # Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        # Set Zone Parameters
        Office = Zone(window_area=13.5,
                      walls_area=15.19 - 13.5,
                      floor_area=34.3,
                      room_vol=106.33,
                      total_internal_area=142.38,
                      lighting_load=11.7,
                      lighting_control=300,
                      lighting_utilisation_factor=0.45,
                      lighting_maintenance_factor=0.9,
                      u_walls=0.2,
                      u_windows=1.1,
                      ach_vent=1.5,
                      ach_infl=0.5,
                      ventilation_efficiency=0.6,
                      thermal_capacitance_per_floor_area=165000,
                      t_set_heating=20,
                      t_set_cooling=26,
                      max_cooling_energy_per_floor_area=-12,
                      max_heating_energy_per_floor_area=12,
                      heating_supply_system=supply_system.DirectHeater,
                      cooling_supply_system=supply_system.DirectCooler,
                      heating_emission_system=emission_system.AirConditioning,
                      cooling_emission_system=emission_system.AirConditioning,
                      )

        Office.solve_energy(
            internal_gains, solar_gains, t_out, t_m_prev)
        Office.solve_lighting(ill, occupancy)

        self.assertEqual(round(Office.energy_demand, 2), -296.65)
        self.assertEqual(round(Office.cooling_sys_electricity, 2), 296.65)
        self.assertEqual(round(Office.heating_sys_electricity, 2), 0)
        self.assertEqual(round(Office.t_m, 2), 25.15)
        self.assertTrue(Office.has_cooling_demand)

        self.assertEqual(Office.lighting_demand, 0)

    def test_HeatingRequired_infl(self):

        t_out = 10
        t_m_prev = 20
        # Internal heat gains, in Watts
        internal_gains = 10

        # Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 2000

        # Illuminance after transmitting through the window
        ill = 44000  # Lumens

        # Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        # Set Zone Parameters
        Office = Zone(window_area=13.5,
                      walls_area=15.19 - 13.5,
                      floor_area=34.3,
                      room_vol=106.33,
                      total_internal_area=142.38,
                      lighting_load=11.7,
                      lighting_control=300,
                      lighting_utilisation_factor=0.45,
                      lighting_maintenance_factor=0.9,
                      u_walls=0.2,
                      u_windows=1.1,
                      ach_vent=1.5,
                      ach_infl=0.5,
                      ventilation_efficiency=0.6,
                      thermal_capacitance_per_floor_area=165000,
                      t_set_heating=20,
                      t_set_cooling=26,
                      max_cooling_energy_per_floor_area=-12,
                      max_heating_energy_per_floor_area=12,
                      heating_supply_system=supply_system.DirectHeater,
                      cooling_supply_system=supply_system.DirectCooler,
                      heating_emission_system=emission_system.AirConditioning,
                      cooling_emission_system=emission_system.AirConditioning,
                      )

        Office.solve_energy(
            internal_gains, solar_gains, t_out, t_m_prev)
        Office.solve_lighting(ill, occupancy)

        self.assertEqual(round(Office.t_m, 2), 20.46)
        self.assertTrue(Office.has_heating_demand)
        self.assertEqual(round(Office.energy_demand, 2), 9.1)
        self.assertEqual(round(Office.heating_sys_electricity, 2), 9.1)
        self.assertEqual(round(Office.cooling_sys_electricity, 2), 0)
        self.assertEqual(Office.lighting_demand, 0)

    def test_MaxCoolingRequired_infl(self):
        t_out = 30
        t_m_prev = 25
        # Internal heat gains, in Watts
        internal_gains = 10

        # Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 5000

        # Illuminance after transmitting through the window
        ill = 44000  # Lumens

        # Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        # Set Zone Parameters
        Office = Zone(window_area=13.5,
                      walls_area=15.19 - 13.5,
                      floor_area=34.3,
                      room_vol=106.33,
                      total_internal_area=142.38,
                      lighting_load=11.7,
                      lighting_control=300,
                      lighting_utilisation_factor=0.45,
                      lighting_maintenance_factor=0.9,
                      u_walls=0.2,
                      u_windows=1.1,
                      ach_vent=1.5,
                      ach_infl=0.5,
                      ventilation_efficiency=0.6,
                      thermal_capacitance_per_floor_area=165000,
                      t_set_heating=20,
                      t_set_cooling=26,
                      max_cooling_energy_per_floor_area=-12,
                      max_heating_energy_per_floor_area=12,
                      heating_supply_system=supply_system.DirectHeater,
                      cooling_supply_system=supply_system.DirectCooler,
                      heating_emission_system=emission_system.AirConditioning,
                      cooling_emission_system=emission_system.AirConditioning,
                      )

        Office.solve_energy(
            internal_gains, solar_gains, t_out, t_m_prev)
        Office.solve_lighting(ill, occupancy)

        self.assertEqual(round(Office.t_m, 2), 26.48)
        self.assertTrue(Office.has_cooling_demand)
        self.assertEqual(round(Office.energy_demand, 2), -411.6)
        self.assertEqual(round(Office.cooling_sys_electricity, 2), 411.6)
        self.assertEqual(round(Office.heating_sys_electricity, 2), 0)
        self.assertEqual(Office.lighting_demand, 0)

    def test_MaxHeatingRequired_infl(self):

        t_out = 5
        t_m_prev = 19
        # Internal heat gains, in Watts
        internal_gains = 10

        # Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 2000

        # Illuminance after transmitting through the window
        ill = 44000  # Lumens

        # Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        # Set Zone Parameters
        Office = Zone(window_area=13.5,
                      walls_area=15.19 - 13.5,
                      floor_area=34.3,
                      room_vol=106.33,
                      total_internal_area=142.38,
                      lighting_load=11.7,
                      lighting_control=300,
                      lighting_utilisation_factor=0.45,
                      lighting_maintenance_factor=0.9,
                      u_walls=0.2,
                      u_windows=1.1,
                      ach_vent=1.5,
                      ach_infl=0.5,
                      ventilation_efficiency=0.6,
                      thermal_capacitance_per_floor_area=165000,
                      t_set_heating=20,
                      t_set_cooling=26,
                      max_cooling_energy_per_floor_area=-12,
                      max_heating_energy_per_floor_area=12,
                      heating_supply_system=supply_system.DirectHeater,
                      cooling_supply_system=supply_system.DirectCooler,
                      heating_emission_system=emission_system.AirConditioning,
                      cooling_emission_system=emission_system.AirConditioning,
                      )

        Office.solve_energy(
            internal_gains, solar_gains, t_out, t_m_prev)
        Office.solve_lighting(ill, occupancy)

        self.assertEqual(round(Office.t_m, 2), 19.51)
        self.assertTrue(Office.has_heating_demand)
        self.assertEqual(round(Office.energy_demand, 2), 411.6)
        self.assertEqual(round(Office.cooling_sys_electricity, 2), 0)
        self.assertEqual(round(Office.heating_sys_electricity, 2), 411.6)
        self.assertEqual(Office.lighting_demand, 0)

    def test_lightingrequired_infl(self):

        t_out = 10
        t_m_prev = 22
        # Internal heat gains, in Watts
        internal_gains = 10

        # Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 2000

        # Illuminance after transmitting through the window
        ill = 14000  # Lumens

        # Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        # Set Zone Parameters
        Office = Zone(window_area=13.5,
                      walls_area=15.19 - 13.5,
                      floor_area=34.3,
                      room_vol=106.33,
                      total_internal_area=142.38,
                      lighting_load=11.7,
                      lighting_control=300,
                      lighting_utilisation_factor=0.45,
                      lighting_maintenance_factor=0.9,
                      u_walls=0.2,
                      u_windows=1.1,
                      ach_vent=1.5,
                      ach_infl=0.5,
                      ventilation_efficiency=0.6,
                      thermal_capacitance_per_floor_area=165000,
                      t_set_heating=20.0,
                      t_set_cooling=26.0,
                      max_cooling_energy_per_floor_area=-12.0,
                      max_heating_energy_per_floor_area=12.0,
                      heating_supply_system=supply_system.DirectHeater,
                      cooling_supply_system=supply_system.DirectCooler,
                      heating_emission_system=emission_system.AirConditioning,
                      cooling_emission_system=emission_system.AirConditioning,
                      )

        Office.solve_energy(
            internal_gains, solar_gains, t_out, t_m_prev)
        Office.solve_lighting(ill, occupancy)

        self.assertEqual(round(Office.t_m, 2), 22.43)
        self.assertEqual(Office.energy_demand, 0)
        self.assertEqual(round(Office.cooling_sys_electricity, 2), 0)
        self.assertEqual(round(Office.heating_sys_electricity, 2), 0)
        self.assertEqual(round(Office.lighting_demand, 2), 401.31)

    # ############################ System Variations ########################

    def test_HeatPumpCoolingRequiredHighCOP(self):
        """Warning! Not validated yet and may have errors"""
        t_out = 25
        t_m_prev = 24
        # Internal heat gains, in Watts
        internal_gains = 10

        # Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 4000

        # Illuminance after transmitting through the window
        ill = 44000  # Lumens

        # Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        # Set Zone Parameters
        Office = Zone(window_area=13.5,
                      walls_area=15.19 - 13.5,
                      floor_area=34.3,
                      room_vol=106.33,
                      total_internal_area=142.38,
                      lighting_load=11.7,
                      lighting_control=300,
                      lighting_utilisation_factor=0.45,
                      lighting_maintenance_factor=0.9,
                      u_walls=0.2,
                      u_windows=1.1,
                      ach_vent=1.5,
                      ach_infl=0.5,
                      ventilation_efficiency=0,
                      thermal_capacitance_per_floor_area=165000,
                      t_set_heating=20,
                      t_set_cooling=26,
                      max_cooling_energy_per_floor_area=-12,
                      max_heating_energy_per_floor_area=12,
                      heating_supply_system=supply_system.DirectHeater,
                      cooling_supply_system=supply_system.HeatPumpAir,
                      heating_emission_system=emission_system.AirConditioning,
                      cooling_emission_system=emission_system.AirConditioning,
                      )

        Office.solve_energy(
            internal_gains, solar_gains, t_out, t_m_prev)
        Office.solve_lighting(ill, occupancy)

        self.assertEqual(round(Office.energy_demand, 2), -264.75)
        self.assertEqual(round(Office.cooling_sys_electricity, 2), 55.87)
        self.assertEqual(round(Office.heating_sys_electricity, 2), 0)
        self.assertEqual(round(Office.t_m, 2), 25.15)
        self.assertEqual(round(Office.cop, 2), 4.74)
        self.assertTrue(Office.has_cooling_demand)

        self.assertEqual(Office.lighting_demand, 0)

    def test_HeatPumpCoolingRequired(self):
        """Warning! Not validated yet and may have errors"""
        t_out = 35
        t_m_prev = 24
        # Internal heat gains, in Watts
        internal_gains = 10

        # Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 4000

        # Illuminance after transmitting through the window
        ill = 44000  # Lumens

        # Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        # Set Zone Parameters
        Office = Zone(window_area=13.5,
                      walls_area=15.19 - 13.5,
                      floor_area=34.3,
                      room_vol=106.33,
                      total_internal_area=142.38,
                      lighting_load=11.7,
                      lighting_control=300,
                      lighting_utilisation_factor=0.45,
                      lighting_maintenance_factor=0.9,
                      u_walls=0.2,
                      u_windows=1.1,
                      ach_vent=1.5,
                      ach_infl=0.5,
                      ventilation_efficiency=0,
                      thermal_capacitance_per_floor_area=165000,
                      t_set_heating=20,
                      t_set_cooling=26,
                      max_cooling_energy_per_floor_area=-12,
                      max_heating_energy_per_floor_area=12,
                      heating_supply_system=supply_system.DirectHeater,
                      cooling_supply_system=supply_system.HeatPumpAir,
                      heating_emission_system=emission_system.AirConditioning,
                      cooling_emission_system=emission_system.AirConditioning,
                      )

        Office.solve_energy(
            internal_gains, solar_gains, t_out, t_m_prev)
        Office.solve_lighting(ill, occupancy)

        self.assertEqual(round(Office.energy_demand, 2), -411.6)
        self.assertEqual(round(Office.cooling_sys_electricity, 2), 107.44)
        self.assertEqual(round(Office.heating_sys_electricity, 2), 0)
        self.assertEqual(round(Office.t_m, 2), 25.33)
        self.assertEqual(round(Office.cop, 2), 3.83)
        self.assertTrue(Office.has_cooling_demand)

        self.assertEqual(Office.lighting_demand, 0)

    def test_WaterHeatPumpCoolingRequired(self):
        """Warning! Not validated yet and may have errors"""
        t_out = 35
        t_m_prev = 24
        # Internal heat gains, in Watts
        internal_gains = 10

        # Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 4000

        # Illuminance after transmitting through the window
        ill = 44000  # Lumens

        # Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        # Set Zone Parameters
        Office = Zone(window_area=13.5,
                      walls_area=15.19 - 13.5,
                      floor_area=34.3,
                      room_vol=106.33,
                      total_internal_area=142.38,
                      lighting_load=11.7,
                      lighting_control=300,
                      lighting_utilisation_factor=0.45,
                      lighting_maintenance_factor=0.9,
                      u_walls=0.2,
                      u_windows=1.1,
                      ach_vent=1.5,
                      ach_infl=0.5,
                      ventilation_efficiency=0,
                      thermal_capacitance_per_floor_area=165000,
                      t_set_heating=20,
                      t_set_cooling=26,
                      max_cooling_energy_per_floor_area=-12,
                      max_heating_energy_per_floor_area=12,
                      heating_supply_system=supply_system.DirectHeater,
                      cooling_supply_system=supply_system.HeatPumpWater,
                      heating_emission_system=emission_system.AirConditioning,
                      cooling_emission_system=emission_system.AirConditioning,
                      )

        Office.solve_energy(
            internal_gains, solar_gains, t_out, t_m_prev)
        Office.solve_lighting(ill, occupancy)

        self.assertEqual(round(Office.energy_demand, 2), -411.6)
        self.assertEqual(round(Office.cooling_sys_electricity, 2), 52.12)
        self.assertEqual(round(Office.heating_sys_electricity, 2), 0)
        self.assertEqual(round(Office.t_m, 2), 25.33)
        self.assertEqual(round(Office.cop, 2), 7.9)
        self.assertTrue(Office.has_cooling_demand)

        self.assertEqual(Office.lighting_demand, 0)

    def test_AirHeatPump_HeatingRequired_infl(self):

        t_out = 10
        t_m_prev = 20
        # Internal heat gains, in Watts
        internal_gains = 10

        # Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 2000

        # Illuminance after transmitting through the window
        ill = 44000  # Lumens

        # Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        # Set Zone Parameters
        Office = Zone(window_area=13.5,
                      walls_area=15.19 - 13.5,
                      floor_area=34.3,
                      room_vol=106.33,
                      total_internal_area=142.38,
                      lighting_load=11.7,
                      lighting_control=300,
                      lighting_utilisation_factor=0.45,
                      lighting_maintenance_factor=0.9,
                      u_walls=0.2,
                      u_windows=1.1,
                      ach_vent=1.5,
                      ach_infl=0.5,
                      ventilation_efficiency=0.6,
                      thermal_capacitance_per_floor_area=165000,
                      t_set_heating=20,
                      t_set_cooling=26,
                      max_cooling_energy_per_floor_area=-12,
                      max_heating_energy_per_floor_area=12,
                      heating_supply_system=supply_system.HeatPumpAir,
                      cooling_supply_system=supply_system.DirectCooler,
                      heating_emission_system=emission_system.AirConditioning,
                      cooling_emission_system=emission_system.AirConditioning,
                      )

        Office.solve_energy(
            internal_gains, solar_gains, t_out, t_m_prev)
        Office.solve_lighting(ill, occupancy)

        self.assertEqual(round(Office.t_m, 2), 20.46)
        self.assertTrue(Office.has_heating_demand)
        self.assertEqual(round(Office.energy_demand, 2), 9.1)
        self.assertEqual(round(Office.heating_sys_electricity, 2), 2.43)
        self.assertEqual(round(Office.cooling_sys_electricity, 2), 0)
        self.assertEqual(round(Office.cop, 2), 3.75)
        self.assertEqual(Office.lighting_demand, 0)

    def test_WaterHeatPump_HeatingRequired_infl(self):

        t_out = 10
        t_m_prev = 20
        # Internal heat gains, in Watts
        internal_gains = 10

        # Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 2000

        # Illuminance after transmitting through the window
        ill = 44000  # Lumens

        # Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        # Set Zone Parameters
        Office = Zone(window_area=13.5,
                      walls_area=15.19 - 13.5,
                      floor_area=34.3,
                      room_vol=106.33,
                      total_internal_area=142.38,
                      lighting_load=11.7,
                      lighting_control=300,
                      lighting_utilisation_factor=0.45,
                      lighting_maintenance_factor=0.9,
                      u_walls=0.2,
                      u_windows=1.1,
                      ach_vent=1.5,
                      ach_infl=0.5,
                      ventilation_efficiency=0.6,
                      thermal_capacitance_per_floor_area=165000,
                      t_set_heating=20,
                      t_set_cooling=26,
                      max_cooling_energy_per_floor_area=-12,
                      max_heating_energy_per_floor_area=12,
                      heating_supply_system=supply_system.HeatPumpWater,
                      cooling_supply_system=supply_system.DirectCooler,
                      heating_emission_system=emission_system.AirConditioning,
                      cooling_emission_system=emission_system.AirConditioning,
                      )

        Office.solve_energy(
            internal_gains, solar_gains, t_out, t_m_prev)
        Office.solve_lighting(ill, occupancy)

        self.assertEqual(round(Office.t_m, 2), 20.46)
        self.assertTrue(Office.has_heating_demand)
        self.assertEqual(round(Office.energy_demand, 2), 9.1)
        self.assertEqual(round(Office.heating_sys_electricity, 2), 1.97)
        self.assertEqual(round(Office.cooling_sys_electricity, 2), 0)
        self.assertEqual(round(Office.cop, 2), 4.62)
        self.assertEqual(Office.lighting_demand, 0)

    def test_WaterHeatPump_mixedEmissions_infl(self):

        t_out = 10
        t_m_prev = 20
        # Internal heat gains, in Watts
        internal_gains = 10

        # Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 2000

        # Illuminance after transmitting through the window
        ill = 44000  # Lumens

        # Occupancy for the timestep [people/hour/square_meter]
        occupancy = 0.1

        # Set Zone Parameters
        Office = Zone(window_area=13.5,
                      walls_area=15.19 - 13.5,
                      floor_area=34.3,
                      room_vol=106.33,
                      total_internal_area=142.38,
                      lighting_load=11.7,
                      lighting_control=300,
                      lighting_utilisation_factor=0.45,
                      lighting_maintenance_factor=0.9,
                      u_walls=0.2,
                      u_windows=1.1,
                      ach_vent=1.5,
                      ach_infl=0.5,
                      ventilation_efficiency=0.6,
                      thermal_capacitance_per_floor_area=165000,
                      t_set_heating=20,
                      t_set_cooling=26,
                      max_cooling_energy_per_floor_area=-12,
                      max_heating_energy_per_floor_area=12,
                      heating_supply_system=supply_system.HeatPumpWater,
                      cooling_supply_system=supply_system.HeatPumpAir,
                      heating_emission_system=emission_system.FloorHeating,
                      cooling_emission_system=emission_system.AirConditioning,
                      )

        Office.solve_energy(
            internal_gains, solar_gains, t_out, t_m_prev)
        Office.solve_lighting(ill, occupancy)

        self.assertEqual(round(Office.t_m, 2), 20.46)
        self.assertTrue(Office.has_heating_demand)
        self.assertEqual(round(Office.energy_demand, 2), 20.97)
        self.assertEqual(round(Office.heating_sys_electricity, 2), 4.54)
        self.assertEqual(round(Office.cooling_sys_electricity, 2), 0)
        self.assertEqual(round(Office.cop, 2), 4.62)
        self.assertEqual(Office.lighting_demand, 0)

        t_out = 24
        t_m_prev = 25

        Office.solve_energy(
            internal_gains, solar_gains, t_out, t_m_prev)

        self.assertEqual(round(Office.energy_demand, 2), -191.55)
        self.assertEqual(round(Office.cooling_sys_electricity, 2), 39.61)

    def test_NoVentilation(self):
        # Zone without any ventilation or infiltration (h_ve_adj = 0)
        t_out = 10
        t_m_prev = 22
        # Internal heat gains, in Watts
        internal_gains = 10

        # Solar heat gains after transmitting through the winow, in Watts
        solar_gains = 2000

        # Set Zone Parameters
        Office = Zone(window_area=13.5,
                      walls_area=15.19 - 13.5,
                      floor_area=34.3,
                      room_vol=106.33,
                      total_internal_area=142.38,
                      lighting_load=11.7,
                      lighting_control=300,
                      lighting_utilisation_factor=0.45,
                      lighting_maintenance_factor=0.9,
                      u_walls=0.2,
                      u_windows=1.1,
                      ach_vent=0,
                      ach_infl=0,
                      ventilation_efficiency=0,
                      thermal_capacitance_per_floor_area=165000,
                      t_set_heating=20,
                      t_set_cooling=26,
                      max_cooling_energy_per_floor_area=-12,
                      max_heating_energy_per_floor_area=12,
                      heating_supply_system=supply_system.DirectHeater,
                      cooling_supply_system=supply_system.DirectCooler,
                      heating_emission_system=emission_system.AirConditioning,
                      cooling_emission_system=emission_system.AirConditioning,
                      )

        self.assertEqual(Office.h_ve_adj, 0)

        Office.solve_energy(
            internal_gains, solar_gains, t_out, t_m_prev)

        self.assertEqual(round(Office.t_m, 2), 22.57)
        self.assertEqual(round(Office.t_air, 2), 23.32)
        self.assertEqual(Office.energy_demand, 0)

        # Cooling delivered to the air node
        t_out = 25
        t_m_prev = 24
        solar_gains = 4000

        Office.solve_energy(
            internal_gains, solar_gains, t_out, t_m_prev)

        self.assertTrue(Office.has_cooling_demand)
        self.assertEqual(round(Office.t_air, 2), 26.0)
        self.assertEqual(round(Office.t_m, 2), 25.15)
        self.assertEqual(round(Office.energy_demand, 2), -335.64)


if __name__ == '__main__':
    unittest.main()
