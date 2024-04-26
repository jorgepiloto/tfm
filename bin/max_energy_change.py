from astropy import units as u
from matplotlib import pyplot as plt
import numpy as np
from labellines import labelLines

from poliastro.bodies import Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune
from poliastro.plotting.util import BODY_COLORS

BODY_VELOCITIES = {
    Mercury: 47.4 * u.km / u.s,
    Venus: 35.0 * u.km / u.s,
    Earth: 29.8 * u.km / u.s,
    Mars: 24.1 * u.km / u.s,
    Jupiter: 13.1 * u.km / u.s,
    Saturn: 9.7 * u.km / u.s,
    Uranus: 6.8 * u.km / u.s,
    Neptune: 5.4 * u.km / u.s,
}



PLANETS = [Mercury, Venus, Earth, Mars, Jupiter, Saturn, Uranus, Neptune]

def max_deflection_angle(k, vh, r):
    return 2 * np.rad2deg(np.arcsin(k / (k + vh ** 2 * r)))

def max_f(epsilon, max_psi):
    max_psi = np.deg2rad(max_psi)

    if epsilon >= (np.pi - max_psi):
        f = (np.cos(epsilon) + 1) / 2
    else:
        f = (np.cos(epsilon) - np.cos(max_psi + epsilon)) / 2
    return f
    
def max_energy_at_vh(planet, vh):
    r = 2 * planet.R.to_value(u.km)
    k = planet.k.to_value(u.km ** 3 / u.s ** 2)
    max_psi = max_deflection_angle(k, vh, r)
    E_star = 2 * vp * vh
    epsilon = np.pi / 2
    return max_f(epsilon, max_psi) * E_star

vh_list = np.linspace(0, 25, 100)

fig, ax = plt.subplots(figsize=(10, 7))
ax.set_xlabel(r"Hyperbolic velocity ${v}_{\infty}$ (km/s)")
ax.set_ylabel(r"Maximum energy increase (km$^2$/s$^2$)")
ax.set_xlim(0, 25)
ax.set_ylim(0, 200)

for planet in PLANETS:
    vp = BODY_VELOCITIES[planet].to_value(u.km / u.s)
    energy = []
    for vh in vh_list:
        energy.append(max_energy_at_vh(planet, vh))

    ax.plot(vh_list, energy, label=planet.name, color=BODY_COLORS[planet.name],
            lw=2.5)

labelLines(ax.get_lines(), align=True, fontsize=14)
ax.grid(True)
plt.savefig("fig/static/max_energy.png", bbox_inches="tight")
