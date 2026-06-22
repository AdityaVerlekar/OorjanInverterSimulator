class solar_model:
    def __init__(self):
        self.power_curve = {
            6: 20,
            7: 160,
            8: 300,
            9: 440,
            10: 587,
            11: 733,
            12: 880,
            13: 792,
            14: 704,
            15: 616,
            16: 411,
            17: 205,
            18: 0
        }
        self.time = 0
        self.DC_voltage = 70  #2x 35V panels in series FIXME should voltage change by time
        self.DC_power = 0
        self.DC_current = 0




    def get_panel_power(self, time):
        if(time<6 or time>18):
            self.DC_power = 0
            return 0

        if(time%1==0):
            self.DC_power = self.power_curve[time]
            return self.DC_power

        t1 = time//1
        t2 = t1+1

        p1 = self.power_curve[t1]
        p2 = self.power_curve[t2]

        self.DC_power = round(p1 + (time - t1) / (t2 - t1) * (p2 - p1))
        return self.DC_power

    def get_panel_voltage(self):
        return self.DC_voltage #FIXME should voltage change by time

    def get_panel_current(self):
        self.DC_current = self.DC_power/self.DC_voltage
        return self.DC_current







#https://www.waaree.com/upload/media/ahnay_series_bi_53_560_590_wel_epd_560_590_156_mpb_hc_02_19032024_1768194194.pdf