import pandas as pd  # Βιβλιοθήκη που μας επιτρέπει να διαβάζουμε και να επεξεργαζόμαστε δεδομένα, κυρίως σε μορφή πίνακα (dataframes).
import matplotlib.pyplot as plt  # Βιβλιοθήκη για τη δημιουργία γραφημάτων (plots).
import matplotlib.dates as mdates  # Βοηθητική βιβλιοθήκη για την εμφάνιση ημερομηνιών και ωρών στα γραφήματα.
from matplotlib.backends.backend_pdf import PdfPages  # Μας επιτρέπει να αποθηκεύουμε πολλά γραφήματα σε ένα αρχείο PDF.

def main():
    """
    Κύρια συνάρτηση (main) που διαβάζει τα δεδομένα, τα καθαρίζει, και καλεί άλλες συναρτήσεις
    για τη δημιουργία και αποθήκευση γραφημάτων.
    """

    # Δημιουργούμε ένα λεξικό (dictionary) που ονομάζεται 'data'.
    # Κάθε "κλειδί" (π.χ. "Cosmote_A") είναι το όνομα που αντιστοιχεί σε ένα συγκεκριμένο CSV αρχείο.
    # Η τιμή (value) είναι το περιεχόμενο του CSV ως πίνακας (DataFrame) της βιβλιοθήκης pandas.
    # pd.read_csv(...) διαβάζει το αρχείο CSV και το μετατρέπει σε DataFrame.
    data = {
        "Cosmote_A": pd.read_csv("./data/group15_Cosmote_A.csv", keep_default_na=True, na_values=["", " "]),
        "Cosmote_B": pd.read_csv("./data/group15_Cosmote_B.csv", keep_default_na=True, na_values=["", " "]),
        "Cosmote_C": pd.read_csv("./data/group15_Cosmote_C.csv", keep_default_na=True, na_values=["", " "]),
        "Vodafone_A": pd.read_csv("./data/group15_Vodafone_A.csv", keep_default_na=True, na_values=["", " "]),
        "Vodafone_B": pd.read_csv("./data/group15_Vodafone_B.csv", keep_default_na=True, na_values=["", " "]),
        "Vodafone_C": pd.read_csv("./data/group15_Vodafone_C.csv", keep_default_na=True, na_values=["", " "]),
        "Nova_A": pd.read_csv("./data/group15_Nova_A.csv", keep_default_na=True, na_values=["", " "]),
        "Nova_B": pd.read_csv("./data/group15_Nova_B.csv", keep_default_na=True, na_values=["", " "]),
        "Nova_C": pd.read_csv("./data/group15_Nova_C.csv", keep_default_na=True, na_values=["", " "])
    }
    # Το "keep_default_na=True" και το "na_values=["", " "]" ορίζουν ότι κενά πεδία (π.χ. "") θα θεωρούνται ως NaN (Not a Number).
    # Στη Python, το NaN αντιπροσωπεύει τιμές που λείπουν (missing data).

    # Επεξεργαζόμαστε τα δεδομένα σε κάθε DataFrame ξεχωριστά, μέσα σε ένα for-loop.
    for key, df in data.items():
        # 1) Αφαιρούμε τυχόν κενά διαστήματα από τα ονόματα στηλών (π.χ. " LTE RSRP " -> "LTE RSRP").
        df.columns = df.columns.str.strip()
        # 2) Μετατρέπουμε τη στήλη "Time" σε μορφή ημερομηνίας/ώρας (datetime).
        # Το format="%m/%d/%Y %H:%M:%S" δείχνει πώς διαβάζουμε την ημερομηνία (μήνας/μέρα/έτος ώρα:λεπτό:δευτερόλεπτο).
        # Το errors='coerce' θα μετατρέψει σε NaT (Not a Time) όποιες τιμές δεν συμφωνούν με το format.
        df["Time"] = pd.to_datetime(df["Time"], format="%m/%d/%Y %H:%M:%S", errors='coerce')

    # Καλούμε τις συναρτήσεις (που ορίζονται πιο κάτω) για να παράξουν τα γραφήματα και να τα αποθηκεύσουν σε αρχεία PDF.
    plot_lte_rsrp(data, "lte_rsrp_plots.pdf")           # Σχήμα 1
    plot_lte_pucch_tx_power(data, "lte_pucch_tx_power_plots.pdf")  # Σχήμα 2
    plot_avg_rsrp_per_location(data, "avg_rsrp_per_location.pdf")  # Σχήμα 3
    plot_avg_tx_power_per_location(data, "avg_tx_power_per_location.pdf")  # Σχήμα 4
    plot_rsrp_std_per_location(data, "rsrp_std_per_location.pdf")  # Σχήμα 5
    plot_tx_power_std_per_location(data, "tx_power_std_per_location.pdf")  # Σχήμα 6
    plot_missing_data_for_tx_power(data, "missing_data_tx_power.pdf")      # Σχήμα 7

def plot_lte_rsrp(data, output_pdf):
    """
    Συνάρτηση που δημιουργεί ένα γράφημα (plot) για την τιμή "LTE RSRP" (Λαμβανόμενη Ισχύς)
    σε σχέση με τον χρόνο, για όλους τους παρόχους μαζί.
    """
    colors = {"Cosmote": "blue", "Vodafone": "red", "Nova": "green"}
    # Ανοίγουμε ένα "PdfPages" αντικείμενο για να γράψουμε σε ένα PDF αρχείο.
    with PdfPages(output_pdf) as pdf:
        # Ορίζουμε το μέγεθος του γραφήματος (14 πλάτος x 7 ύψος).
        plt.figure(figsize=(14, 7))

        # Για κάθε (key, df) στο λεξικό data:
        for key, df in data.items():
            # Αποσπούμε τον πάροχο από το key (π.χ. "Cosmote_A" -> "Cosmote").
            provider = key.split("_")[0]
            # Φτιάχνουμε το γράφημα (line plot) βάζοντας στη θέση του x την στήλη "Time" και στο y την "LTE RSRP".
            plt.plot(df["Time"], df["LTE RSRP"],
                     label=provider,  # Το label είναι το όνομα που θα εμφανιστεί στο υπόμνημα (legend).
                     color=colors.get(provider, "black"),  # Παίρνουμε το χρώμα από το dictionary colors.
                     alpha=0.7)  # Ημιδιαφάνεια.

        # Ρυθμίζουμε τον τίτλο των αξόνων και του γραφήματος.
        plt.xlabel("Time")
        plt.ylabel("LTE RSRP (dBm)")
        plt.title("Σχήμα 1: Λαμβανόμενη ισχύς vs Χρόνος")
        plt.legend()
        # Προσθήκη πλέγματος στο background.
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.xticks(rotation=45)  # Περιστρέφουμε τις ετικέτες στον άξονα Χ κατά 45 μοίρες για να χωρούν καλύτερα.

        # Εδώ χρησιμοποιούμε τη βιβλιοθήκη matplotlib.dates για να διαμορφώσουμε τον άξονα του χρόνου.
        plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=1))  # Ανά λεπτό.
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))  # Εμφάνιση ως ώρα:λεπτό:δευτερόλεπτο.

        plt.tight_layout()  # Προσπαθεί να "μαζέψει" τα στοιχεία του γραφήματος για να μην αλληλεπικαλύπτονται.
        pdf.savefig()       # Αποθηκεύουμε το γράφημα στο αρχείο PDF.
        plt.close()         # Κλείνουμε το γράφημα για να μην "μπλεχτούν" με το επόμενο.

    print(f"Το γράφημα αποθηκεύτηκε στο {output_pdf}")

def plot_lte_pucch_tx_power(data, output_pdf):
    """
    Συνάρτηση που δημιουργεί ένα γράφημα της τιμής "LTE PUCCH TX Power" (Εκπεμπόμενη Ισχύς)
    σε σχέση με τον χρόνο, για όλους τους παρόχους.
    """
    colors = {"Cosmote": "blue", "Vodafone": "red", "Nova": "green"}
    with PdfPages(output_pdf) as pdf:
        plt.figure(figsize=(14, 7))
        plotted_providers = set()  # Χρησιμοποιείται για να αποφύγουμε επαναλήψεις στο υπόμνημα (legend).

        for key, df in data.items():
            provider = key.split("_")[0]
            # Θέλουμε να εμφανίσουμε το όνομα του provider μόνο την πρώτη φορά που εμφανίζεται.
            # Αν ήδη τον έχουμε βάλει στο plotted_providers, το label θα είναι None (δεν θα εμφανίζεται).
            label = provider if provider not in plotted_providers else None

            plt.plot(df["Time"], df["LTE PUCCH TX Power"],
                     label=label,
                     color=colors.get(provider, "black"),
                     alpha=0.7)

            if label:
                plotted_providers.add(provider)

        plt.xlabel("Time")
        plt.ylabel("LTE PUCCH TX Power (dBm)")
        plt.title("Σχήμα 2: Εκπεμπόμενη ισχύς vs Χρόνος")
        plt.legend()
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.xticks(rotation=45)

        plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=1))
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))

        plt.tight_layout()
        pdf.savefig()
        plt.close()

    print(f"Το ραβδόγραμμα αποθηκεύτηκε στο {output_pdf}")

def plot_avg_rsrp_per_location(data, output_pdf):
    """
    Συνάρτηση που υπολογίζει και εμφανίζει την μέση τιμή (average) της στήλης "LTE RSRP" (λαμβανόμενη ισχύς)
    για κάθε πάροχο και για κάθε τοποθεσία (A, B, C).
    Έπειτα εμφανίζει αυτά τα δεδομένα ως ραβδόγραμμα (bar chart).
    """
    import numpy as np
    from matplotlib.backends.backend_pdf import PdfPages

    providers = ["Cosmote", "Vodafone", "Nova"]
    locations = ["A", "B", "C"]

    # Δημιουργούμε ένα λεξικό που θα αποθηκεύει τη μέση τιμή της LTE RSRP ανά πάροχο και τοποθεσία.
    means = {loc: {prov: np.nan for prov in providers} for loc in locations}

    # Γεμίζουμε το λεξικό με τις μέσες τιμές (mean) από τα δεδομένα.
    for key, df in data.items():
        provider = key.split("_")[0]
        location = key.split("_")[1]
        if provider in providers and location in locations:
            # Με την df["LTE RSRP"].mean() παίρνουμε τη μέση τιμή της στήλης "LTE RSRP".
            means[location][provider] = df["LTE RSRP"].mean()

    # Ετοιμάζουμε τον άξονα x για το γράφημα. Χρησιμοποιούμε τις 3 τοποθεσίες (A, B, C).
    x = np.arange(len(locations))  # π.χ. [0,1,2] αν len(locations) = 3.
    width = 0.25  # Πλάτος κάθε μπάρας για να τοποθετηθούν δίπλα δίπλα.

    # Παίρνουμε τις μέσες τιμές για κάθε πάροχο, με τη σειρά των τοποθεσιών [A, B, C].
    cosmote_means = [means[loc]["Cosmote"] for loc in locations]
    vodafone_means = [means[loc]["Vodafone"] for loc in locations]
    nova_means = [means[loc]["Nova"] for loc in locations]

    with PdfPages(output_pdf) as pdf:
        plt.figure(figsize=(10, 6))

        # Δεδομένου ότι έχουμε 3 μπάρες για κάθε τοποθεσία,
        # μετατοπίζουμε ελαφρώς τη θέση των μπαρών στον άξονα x:
        plt.bar(x - width, cosmote_means, width, label="Cosmote", color="blue", alpha=0.7)
        plt.bar(x, vodafone_means, width, label="Vodafone", color="red", alpha=0.7)
        plt.bar(x + width, nova_means, width, label="Nova", color="green", alpha=0.7)

        # Ρυθμίζουμε τον άξονα Χ να δείχνει "A, B, C" στις αντίστοιχες θέσεις 0,1,2.
        plt.xticks(x, locations)

        plt.xlabel("Σημείο Μέτρησης")
        plt.ylabel("Μέση Λαμβανόμενη Ισχύς (dBm)")
        plt.title("Σχήμα 3: Μέση λαμβανόμενη ισχύς ανά σημείο/πάροχο")
        plt.legend()
        plt.grid(axis="y", linestyle="--", alpha=0.6)
        plt.tight_layout()
        pdf.savefig()
        plt.close()

    print(f"Το ραβδόγραμμα της μέσης ληφθείσας ισχύος (RSRP) αποθηκεύτηκε στο '{output_pdf}'.")

def plot_avg_tx_power_per_location(data, output_pdf):
    """
    Παρόμοιο με την προηγούμενη συνάρτηση, αλλά εδώ υπολογίζουμε και εμφανίζουμε
    τη μέση τιμή της 'LTE PUCCH TX Power' (εκπεμπόμενη ισχύς) ανά τοποθεσία (A, B, C) και ανά πάροχο.
    """
    import numpy as np
    from matplotlib.backends.backend_pdf import PdfPages

    providers = ["Cosmote", "Vodafone", "Nova"]
    locations = ["A", "B", "C"]

    # Ομοίως, φτιάχνουμε ένα λεξικό για να κρατήσουμε τις μέσες τιμές ανά τοποθεσία/πάροχο.
    means = {loc: {prov: np.nan for prov in providers} for loc in locations}

    # Συμπληρώνουμε τις μέσες τιμές (mean).
    for key, df in data.items():
        provider = key.split("_")[0]
        location = key.split("_")[1]
        if provider in providers and location in locations:
            means[location][provider] = df["LTE PUCCH TX Power"].mean()

    x = np.arange(len(locations))
    width = 0.25

    cosmote_means = [means[loc]["Cosmote"] for loc in locations]
    vodafone_means = [means[loc]["Vodafone"] for loc in locations]
    nova_means = [means[loc]["Nova"] for loc in locations]

    with PdfPages(output_pdf) as pdf:
        plt.figure(figsize=(10, 6))
        plt.bar(x - width, cosmote_means, width, label="Cosmote", color="blue", alpha=0.7)
        plt.bar(x, vodafone_means, width, label="Vodafone", color="red", alpha=0.7)
        plt.bar(x + width, nova_means, width, label="Nova", color="green", alpha=0.7)

        plt.xticks(x, locations)
        plt.xlabel("Σημείο Μέτρησης")
        plt.ylabel("Μέση Εκπεμπόμενη Ισχύς (dBm)")
        plt.title("Σχήμα 4: Μέση εκπεμπόμενη ισχύς ανά σημείο/πάροχο")
        plt.legend()
        plt.grid(axis="y", linestyle="--", alpha=0.6)
        plt.tight_layout()
        pdf.savefig()
        plt.close()

    print(f"Το ραβδόγραμμα της μέσης εκπεμπόμενης ισχύος αποθηκεύτηκε στο '{output_pdf}'.")

def plot_rsrp_std_per_location(data, output_pdf):
    """
    Συνάρτηση που υπολογίζει και εμφανίζει την τυπική απόκλιση (standard deviation) της λαμβανόμενης ισχύος (LTE RSRP)
    για κάθε πάροχο και τοποθεσία. Τυπική απόκλιση είναι ένα μέτρο για το πόσο απλώνονται οι τιμές γύρω από το μέσο όρο.
    """
    import numpy as np
    from matplotlib.backends.backend_pdf import PdfPages

    providers = ["Cosmote", "Vodafone", "Nova"]
    locations = ["A", "B", "C"]

    # Δομή λεξικού για να αποθηκεύσουμε τις τιμές της τυπικής απόκλισης.
    std_values = {loc: {prov: np.nan for prov in providers} for loc in locations}

    for key, df in data.items():
        provider = key.split("_")[0]
        location = key.split("_")[1]
        if provider in providers and location in locations:
            std_values[location][provider] = df["LTE RSRP"].std()

    x = np.arange(len(locations))
    width = 0.25

    cosmote_std = [std_values[loc]["Cosmote"] for loc in locations]
    vodafone_std = [std_values[loc]["Vodafone"] for loc in locations]
    nova_std = [std_values[loc]["Nova"] for loc in locations]

    with PdfPages(output_pdf) as pdf:
        plt.figure(figsize=(10, 6))
        plt.bar(x - width, cosmote_std, width, label="Cosmote", color="blue", alpha=0.7)
        plt.bar(x, vodafone_std, width, label="Vodafone", color="red", alpha=0.7)
        plt.bar(x + width, nova_std, width, label="Nova", color="green", alpha=0.7)

        plt.xticks(x, locations)
        plt.xlabel("Σημείο Μέτρησης")
        plt.ylabel("Τυπική Απόκλιση (dBm)")
        plt.title("Σχήμα 5: Τυπική απόκλιση λαμβανόμενης ισχύος")
        plt.legend()
        plt.grid(axis="y", linestyle="--", alpha=0.6)
        plt.tight_layout()
        pdf.savefig()
        plt.close()

    print(f"Το ραβδόγραμμα της τυπικής απόκλισης (RSRP) αποθηκεύτηκε στο '{output_pdf}'.")

def plot_tx_power_std_per_location(data, output_pdf):
    """
    Παρόμοια συνάρτηση με την προηγούμενη, αλλά υπολογίζει και εμφανίζει την τυπική απόκλιση
    της εκπεμπόμενης ισχύος (LTE PUCCH TX Power) για κάθε τοποθεσία και πάροχο.
    """
    import numpy as np
    from matplotlib.backends.backend_pdf import PdfPages

    providers = ["Cosmote", "Vodafone", "Nova"]
    locations = ["A", "B", "C"]

    std_values = {loc: {prov: np.nan for prov in providers} for loc in locations}

    for key, df in data.items():
        provider = key.split("_")[0]
        location = key.split("_")[1]
        if provider in providers and location in locations:
            std_values[location][provider] = df["LTE PUCCH TX Power"].std()

    x = np.arange(len(locations))
    width = 0.25

    cosmote_std = [std_values[loc]["Cosmote"] for loc in locations]
    vodafone_std = [std_values[loc]["Vodafone"] for loc in locations]
    nova_std = [std_values[loc]["Nova"] for loc in locations]

    with PdfPages(output_pdf) as pdf:
        plt.figure(figsize=(10, 6))
        plt.bar(x - width, cosmote_std, width, label="Cosmote", color="blue", alpha=0.7)
        plt.bar(x, vodafone_std, width, label="Vodafone", color="red", alpha=0.7)
        plt.bar(x + width, nova_std, width, label="Nova", color="green", alpha=0.7)

        plt.xticks(x, locations)
        plt.xlabel("Σημείο Μέτρησης")
        plt.ylabel("Τυπική Απόκλιση (dBm)")
        plt.title("Σχήμα 6: Τυπική απόκλιση εκπεμπόμενης ισχύος")
        plt.legend()
        plt.grid(axis="y", linestyle="--", alpha=0.6)
        plt.tight_layout()
        pdf.savefig()
        plt.close()

    print(f"Το ραβδόγραμμα της τυπικής απόκλισης (PUCCH TX Power) αποθηκεύτηκε στο '{output_pdf}'.")

def plot_missing_data_for_tx_power(data, output_pdf):
    """
    Συνάρτηση που υπολογίζει το ποσοστό των "κενών"/ελλιπών δεδομένων (missing data)
    στη στήλη 'LTE PUCCH TX Power' για κάθε πάροχο, και το εμφανίζει σε μορφή ραβδογράμματος.
    """
    import numpy as np
    from matplotlib.backends.backend_pdf import PdfPages

    providers = ["Cosmote", "Vodafone", "Nova"]

    # Αρχικοποιούμε δύο λεξικά για να μετρήσουμε πόσα σύνολα δεδομένων υπάρχουν συνολικά (total_counts)
    # και πόσα από αυτά είναι κενά (missing_counts).
    total_counts = {prov: 0 for prov in providers}
    missing_counts = {prov: 0 for prov in providers}

    # Ελέγχουμε κάθε DataFrame (csv) ξεχωριστά.
    for key, df in data.items():
        provider = key.split("_")[0]
        if provider not in providers:
            continue

        total_counts[provider] += len(df)  # Το len(df) δίνει το πλήθος των γραμμών στο DataFrame.

        if "LTE PUCCH TX Power" not in df.columns:
            # Αν δεν υπάρχει καν η στήλη, θεωρούμε ότι όλα τα δεδομένα σε αυτό το DataFrame είναι "missing".
            missing_counts[provider] += len(df)
        else:
            # Διαφορετικά, μετράμε πόσες γραμμές έχουν NaN (κενή τιμή) στη στήλη "LTE PUCCH TX Power".
            missing_counts[provider] += df["LTE PUCCH TX Power"].isna().sum()

    # Υπολογίζουμε το ποσοστό των ελλιπών δεδομένων ανά πάροχο.
    missing_percentage = {}
    for prov in providers:
        if total_counts[prov] == 0:
            missing_percentage[prov] = 0.0
        else:
            missing_percentage[prov] = (missing_counts[prov] / total_counts[prov]) * 100.0

    x = np.arange(len(providers))  # π.χ. [0, 1, 2] αν έχουμε 3 παρόχους.
    missing_values = [missing_percentage[prov] for prov in providers]

    with PdfPages(output_pdf) as pdf:
        plt.figure(figsize=(8, 6))
        # Σχεδιάζουμε μια μπάρα για κάθε πάροχο, χρησιμοποιώντας διαφορετικό χρώμα.
        plt.bar(x, missing_values, color=["blue", "red", "green"], alpha=0.7)

        plt.xticks(x, providers)
        plt.xlabel("Πάροχος")
        plt.ylabel("Ποσοστό Ελλιπών Δεδομένων (%)")
        plt.title("Σχήμα 7: Missing data στη στήλη 'LTE PUCCH TX Power'")
        plt.grid(axis="y", linestyle="--", alpha=0.6)

        plt.tight_layout()
        pdf.savefig()
        plt.close()

    print(f"Το ραβδόγραμμα του ποσοστού missing data αποθηκεύτηκε στο '{output_pdf}'.")

if __name__ == "__main__":
    # Αν τρέξουμε αυτό το αρχείο απευθείας (αντί να το κάνουμε import σε άλλο),
    # καλούμε τη main() συνάρτηση για να εκτελέσουμε το πρόγραμμά μας.
    main()
