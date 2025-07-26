import json
# % --- Fuel with Gd: Serpent Mamual PDf Page-51
# % --- Fuel consisting of enriched UO2 and burnable absorber.
# % Atomic densities given in units of 1/(barn*cm):
# mat UO2Gd sum % Atomic density from composition
# 92234.09c 4.2940E-06 % Atomic density of U-234
# 92235.09c 5.6226E-04 % Atomic density of U-235
# 92238.09c 2.0549E-02 % Atomic density of U-238
# 64154.09c 4.6173E-05 % Atomic density of Gd-154
# 64155.09c 2.9711E-04 % Atomic density of Gd-155
# 64156.09c 4.1355E-04 % Atomic density of Gd-156
# 64157.09c 3.1518E-04 % Atomic density of Gd-157
# 64158.09c 4.9786E-04 % Atomic density of Gd-158
# 64160.09c 4.3764E-04 % Atomic density of Gd-160
# 8016.09c 4.5243E-02 % Atomic density of O-16

# https://www.nist.gov/pml/atomic-weights-and-isotopic-compositions-relative-atomic-masses
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
gd2o3_frac=8
uo2_frac=92
gd2o3_molarmass=362.5
gd2o3_density=7.41 #g/cm³
uo2_density=10.97 #g/cm³
uo2_molarmass=270.03
barn=1.00E-24
avagadro=6.02E+23

# Gd isotopes
gd_isotopes = [152, 154, 155, 156, 157, 158, 160]
gd_results = []
for num in gd_isotopes:
    iso = get_isotope(num, 'Gd')
    if iso and iso['abundance']:
        serp_val = 2 * gd2o3_frac * gd2o3_density * iso['abundance']*avagadro*barn/ (100 * gd2o3_molarmass)
        gd_results.append((num, serp_val))

# U isotopes
u_isotopes = [234, 235, 238]
uo2_results = []
for num in u_isotopes:
    iso = get_isotope(num, 'U')
    if iso and iso['abundance']:
        serp_val = uo2_frac * uo2_density * iso['abundance']*avagadro*barn / (100 * uo2_molarmass)
        uo2_results.append((num, serp_val))

# O isotopes
o_isotopes = [16, 17, 18]
o_results = []
for num in o_isotopes:
    iso = get_isotope(num, 'O')
    if iso and iso['abundance']:
        serp_val = (2 * uo2_frac * uo2_density * iso['abundance']*avagadro*barn / (100 * uo2_molarmass)) + \
                   (3 * gd2o3_frac * gd2o3_density * iso['abundance']*avagadro*barn / (100 * gd2o3_molarmass))
        o_results.append((num, serp_val))

# # Print 
for num, val in uo2_results:
    print(f"92{num}.09c {val:.5E}")
for num, val in gd_results:
    print(f"64{num}.09c {val:.5E}")
for num, val in o_results:
    print(f"80{num}.09c {val:.5E}")