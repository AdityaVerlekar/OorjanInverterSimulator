from random import *
class solar_model:
    def __init__(self):
        '''
        self.power_curve = {
            6*60: 20,
            7*60: 160,
            8*60: 300,
            9*60: 440,
            10*60: 587,
            11*60: 733,
            12*60: 880,
            13*60: 792,
            14*60: 704,
            15*60: 616,
            16*60: 411,
            17*60: 205,
            18*60: 0
        }
        '''

        randomness_factor = 3 #within 3% of value

        self.irradiance_curve = {
            5 * 60: 0,
            6 * 60: round(30 * (1 + (random() * 2 - 1) * (randomness_factor / 100))),
            7 * 60: round(220 * (1 + (random() * 2 - 1) * (randomness_factor / 100))),
            8 * 60: round(435 * (1 + (random() * 2 - 1) * (randomness_factor / 100))),
            9 * 60: round(630 * (1 + (random() * 2 - 1) * (randomness_factor / 100))),
            10 * 60: round(790 * (1 + (random() * 2 - 1) * (randomness_factor / 100))),
            11 * 60: round(900 * (1 + (random() * 2 - 1) * (randomness_factor / 100))),
            12 * 60: round(955 * (1 + (random() * 2 - 1) * (randomness_factor / 100))),
            13 * 60: round(940 * (1 + (random() * 2 - 1) * (randomness_factor / 100))),
            14 * 60: round(870 * (1 + (random() * 2 - 1) * (randomness_factor / 100))),
            15 * 60: round(740 * (1 + (random() * 2 - 1) * (randomness_factor / 100))),
            16 * 60: round(560 * (1 + (random() * 2 - 1) * (randomness_factor / 100))),
            17 * 60: round(350 * (1 + (random() * 2 - 1) * (randomness_factor / 100))),
            18 * 60: round(138 * (1 + (random() * 2 - 1) * (randomness_factor / 100))),
            19 * 60: 0
        }

        self.time = 0
        self.DC_voltage = 39 #adjusted for high 40C temperature
        self.DC_power = 0
        self.DC_current = 0
        self.irradiance = 0
        self.peak_power = 525

        # https://rooftopsolarindia.com/datasheet/waaree-energies/datasheet-waaree-solar-mono-perc-m10-515W-520W-525W-530W-535W-540W-545W.pdf
        # solar cell area = 2.385 m^2
        #

    def set_panel_irradiance(self, time):
        if(time<5*60 or time>19*60):
            self.DC_power = 0
            return 0

        if(time%60==0):
            self.irradiance = self.irradiance_curve[time]
            return self.irradiance

        t1 = (time//60)*60 #round down to nearest hour
        t2 = t1+60 #round up to nearest hour

        i1 = self.irradiance_curve[t1]
        i2 = self.irradiance_curve[t2]


        irr = round((i1 + (time - t1) / (t2 - t1) * (i2 - i1))*(1 + (random() * 2 - 1) * (0.01)))
        self.irradiance = irr
        return self.irradiance

    def get_panel_power(self):
        self.DC_power = round(self.irradiance*self.peak_power/1000)
        return self.DC_power

    def get_panel_voltage(self):
        return self.DC_voltage

    def get_panel_current(self):
        self.DC_current = self.DC_power/self.DC_voltage
        return self.DC_current



