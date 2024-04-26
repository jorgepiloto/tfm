from astropy import units as u
import numpy as np
import matplotlib.pyplot as plt
from labellines import labelLines

from poliastro.bodies import Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune
from poliastro.plotting.util import BODY_COLORS


planets = [Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune]


def max_deflection_angle(k, vh, r):
    return 2 * np.rad2deg(np.arcsin(k / (k + vh ** 2 * r)))

vh_values = np.linspace(0, 25, 100) * u.km / u.s

fig, ax = plt.subplots(figsize=(10, 7))
ax.set_xlabel(r"Hyperbolic velocity ${v}_{\infty}$ (km/s)")
ax.set_ylabel(r"Maximum deflection angle (deg)")
ax.set_xlim(0, 25)
ax.set_ylim(0, 180)
ax.set_xticks(range(0, 26, 5))
ax.set_yticks(range(0, 181, 30))
ax.grid(True)

for planet in planets:
    r = 2 * planet.R.to_value(u.km)
    k = planet.k.to_value(u.km ** 3 / u.s ** 2)
    deflection_angles = []
    for vh in vh_values:
      deflection_angles.append(max_deflection_angle(k, vh.to_value(u.km/u.s), r))

    ax.plot(vh_values, deflection_angles, label=planet.name,
            color=BODY_COLORS[planet.name], lw=2.5)

labelLines(ax.get_lines(), align=True, fontsize=14)
ax.legend(shadow=True)
plt.savefig("fig/static/deflection_angle.png", bbox_inches="tight")
