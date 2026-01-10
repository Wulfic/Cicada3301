
deor_runes = "DEASIXCUDEADLPNRNGJREAPERIALXGUEATHEAEONGHWAEIAEOEPTHEAJLAEIRSIOLEAUIUAHNGEANGJUESFYNGMEANLEOGDIAGOWWEOIEWPIA"
print(f"String: {deor_runes}")
print(f"Length: {len(deor_runes)}")

import math
side = math.sqrt(len(deor_runes))
print(f"Sqrt: {side}")

# SIX CUBITS -> 6 or 18?
# Length might be close to 108.

for w in range(2, 20):
    grid = [deor_runes[i:i+w] for i in range(0, len(deor_runes), w)]
    diag = ""
    for i in range(min(len(grid), w)):
         if i < len(grid[i]):
             diag += grid[i][i]
    print(f"Width {w} Diagonal: {diag}")

