import tsl2591

tsl = tsl2591.Tsl2591()
full, ir = tsl.get_full_luminosity()
lux = tsl.calculate_lux(full, ir)
print lux, full, ir
