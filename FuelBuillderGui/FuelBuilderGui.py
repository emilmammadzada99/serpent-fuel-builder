import sys
import json
from PyQt5 import QtWidgets, uic

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("mainse.ui", self)  # UI dosyanı yükle

        with open('nistdataiso.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        # Buton tıklama bağlantısı
        self.pushButton_calculate.clicked.connect(self.calculate_isotopes)

        # Varsayılan değerler
        self.lineEdit_gd2o3_frac.setText("5")
        self.lineEdit_uo2_frac.setText("95")
        self.lineEdit_u235_enrichment.setText("3.0")  # U235 enrichment varsayılan %3

    def get_isotope(self, mass_number, symbol):
        for iso in self.data:
            if iso['Isotope.1'].startswith(symbol) and str(int(iso['Isotope.1'].split()[1])) == str(mass_number):
                return {
                    'mass_number': mass_number,
                    'atomic_mass': float(iso['Relative Atomic Mass']),
                    'abundance': float(iso['Isotopic  Composition'])
                }
        return None

    def calculate_first(self, gd2o3_frac, uo2_frac, u234_ab, u235_ab, u238_ab):
        gd2o3_molarmass = 362.5
        uo2_molarmass = 270.03

        gd_isotopes = [152, 154, 155, 156, 157, 158, 160]
        gd_results = []
        for num in gd_isotopes:
            iso = self.get_isotope(num, 'Gd')
            if iso and iso['abundance']:
                serp_val = 2 * gd2o3_frac * iso['atomic_mass'] * iso['abundance'] / (100 * gd2o3_molarmass)
                gd_results.append((num, serp_val))

        u_isotopes = [234, 235, 238]
        u_abundances = [u234_ab, u235_ab, u238_ab]
        uo2_results = []
        for num, abundance in zip(u_isotopes, u_abundances):
            iso = self.get_isotope(num, 'U')
            if iso:
                serp_val = uo2_frac * iso['atomic_mass'] * abundance / (100 * uo2_molarmass)
                uo2_results.append((num, serp_val))

        o_isotopes = [16, 17, 18]
        o_results = []
        for num in o_isotopes:
            iso = self.get_isotope(num, 'O')
            if iso and iso['abundance']:
                serp_val = (2 * uo2_frac * iso['atomic_mass'] * iso['abundance'] / (100 * uo2_molarmass)) + \
                           (3 * gd2o3_frac * iso['atomic_mass'] * iso['abundance'] / (100 * gd2o3_molarmass))
                o_results.append((num, serp_val))

        output = ""
        for num, val in uo2_results:
            output += f"92{num}.09c -{val:.5E}\n"
        for num, val in gd_results:
            output += f"64{num}.09c -{val:.5E}\n"
        for num, val in o_results:
            output += f"80{num}.09c -{val:.5E}\n"
        return output

    def calculate_second(self, gd2o3_frac, uo2_frac, u234_ab, u235_ab, u238_ab):
        gd2o3_molarmass = 362.5
        gd2o3_density = 7.41  # g/cm³
        uo2_density = 10.97  # g/cm³
        uo2_molarmass = 270.03
        barn = 1.00E-24
        avagadro = 6.02E+23

        gd_isotopes = [152, 154, 155, 156, 157, 158, 160]
        gd_results = []
        for num in gd_isotopes:
            iso = self.get_isotope(num, 'Gd')
            if iso and iso['abundance']:
                serp_val = 2 * gd2o3_frac * gd2o3_density * iso['abundance'] * avagadro * barn / (100 * gd2o3_molarmass)
                gd_results.append((num, serp_val))

        u_isotopes = [234, 235, 238]
        u_abundances = [u234_ab, u235_ab, u238_ab]
        uo2_results = []
        for num, abundance in zip(u_isotopes, u_abundances):
            iso = self.get_isotope(num, 'U')
            if iso:
                serp_val = uo2_frac * uo2_density * abundance * avagadro * barn / (100 * uo2_molarmass)
                uo2_results.append((num, serp_val))

        o_isotopes = [16, 17, 18]
        o_results = []
        for num in o_isotopes:
            iso = self.get_isotope(num, 'O')
            if iso and iso['abundance']:
                serp_val = (2 * uo2_frac * uo2_density * iso['abundance'] * avagadro * barn / (100 * uo2_molarmass)) + \
                           (3 * gd2o3_frac * gd2o3_density * iso['abundance'] * avagadro * barn / (100 * gd2o3_molarmass))
                o_results.append((num, serp_val))

        output = ""
        for num, val in uo2_results:
            output += f"92{num}.09c {val:.5E}\n"
        for num, val in gd_results:
            output += f"64{num}.09c {val:.5E}\n"
        for num, val in o_results:
            output += f"8{num}.09c {val:.5E}\n"

        return output

    def calculate_isotopes(self):
        try:
            gd2o3_frac = float(self.lineEdit_gd2o3_frac.text())
        except ValueError:
            gd2o3_frac = 5
        try:
            uo2_frac = float(self.lineEdit_uo2_frac.text())
        except ValueError:
            uo2_frac = 95
        try:
            u235_enrichment = float(self.lineEdit_u235_enrichment.text())
            if not (0 <= u235_enrichment <= 100):
                u235_enrichment = 3.0  # default değer
        except ValueError:
            u235_enrichment = 3.0

        u234_iso = self.get_isotope(234, 'U')
        u234_abundance = u234_iso['abundance'] if u234_iso else 0.0055  # doğal bolluk varsayımı

        u235_abundance = u235_enrichment
        u238_abundance = 100 - u235_abundance - u234_abundance

        output_old = self.calculate_first(gd2o3_frac, uo2_frac, u234_abundance, u235_abundance/100, u238_abundance/100)
        output_new = self.calculate_second(gd2o3_frac, uo2_frac, u234_abundance, u235_abundance/100, u238_abundance/100)

        self.plainTextEdit_output.setPlainText(output_old)
        self.plainTextEdit_output_2.setPlainText(output_new)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
