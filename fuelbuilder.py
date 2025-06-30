import json

# JSON file read isotopes data
with open('nistdataiso.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

def get_isotope(mass_number, symbol):
    for iso in data:
        if iso['Isotope.1'].startswith(symbol) and str(int(iso['Isotope.1'].split()[1])) == str(mass_number):
            return {
                'mass_number': mass_number,
                'atomic_mass': iso['Relative Atomic Mass'],
                'abundance': iso['Isotopic  Composition']
            }
    return None

# Constants
gd2o3_frac=5
uo2_frac=95
gd2o3_molarmass=362.5
uo2_molarmass=270.03

# Gd isotopes
gd_isotopes = [152, 154, 155, 156, 157, 158, 160]
gd_results = []
for num in gd_isotopes:
    iso = get_isotope(num, 'Gd')
    if iso and iso['abundance']:
        serp_val = 2 * gd2o3_frac * iso['atomic_mass'] * iso['abundance'] / (100 * gd2o3_molarmass)
        gd_results.append((num, serp_val))

# U isotopes
u_isotopes = [234, 235, 238]
uo2_results = []
for num in u_isotopes:
    iso = get_isotope(num, 'U')
    if iso and iso['abundance']:
        serp_val = uo2_frac * iso['atomic_mass'] * iso['abundance'] / (100 * uo2_molarmass)
        uo2_results.append((num, serp_val))

# O isotopes
o_isotopes = [16, 17, 18]
o_results = []
for num in o_isotopes:
    iso = get_isotope(num, 'O')
    if iso and iso['abundance']:
        serp_val = (2 * uo2_frac * iso['atomic_mass'] * iso['abundance'] / (100 * uo2_molarmass)) + \
                   (3 * gd2o3_frac * iso['atomic_mass'] * iso['abundance'] / (100 * gd2o3_molarmass))
        o_results.append((num, serp_val))

# Print 
for num, val in uo2_results:
    print(f"92{num}.09c -{val:.5E}")
for num, val in gd_results:
    print(f"64{num}.09c -{val:.5E}")
for num, val in o_results:
    print(f"80{num}.09c -{val:.5E}")
