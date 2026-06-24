from simulator.solar_model import solar_model

solar = solar_model()

for i in range(5*60,19*60, 5):
    hour = i // 60
    minute = i % 60

    x = solar.set_panel_irradiance(i)
    print(f"{hour:02d}:{minute:02d} → {x}")