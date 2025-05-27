import csv
from client_data import ClientData


def load_csv_data(file_path) -> ClientData:
    """
    Charge les données d'un fichier CSV et les retourne sous forme de dictionnaire.
    Args:
        file_path (str): Le chemin du fichier CSV à charger.
    Returns:
        dict: Un dictionnaire contenant les données du fichier CSV.
    """
    data = {}
    with open(file_path, mode='r') as file:
        rows = csv.reader(file, delimiter=',')

        # Lire l'en-tête du fichier CSV
        header = next(rows)

        # Initialiser le dictionnaire avec des listes vides pour chaque colonne
        for column in header:
            data[column] = []

        # Ajouter les données à chaque colonne
        for row in rows:
            for i, column in enumerate(header):
                data[column].append(row[i])

    return ClientData(columns=header, data=data)


def month_convert(month: str) -> int:
    """
    Convertit le nom d'un mois en entier.
    Args:
        month (str): Le nom du mois à convertir.
    Returns:
        int: Le numéro du mois correspondant.
    """
    month_map = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr': 4,
        'may': 5,
        'jun': 6,
        'jul': 7,
        'aug': 8,
        'sep': 9,
        'oct': 10,
        'nov': 11,
        'dec': 12
    }

    return month_map.get(month.lower(), 0)


def preprocess_data(data: ClientData) -> ClientData:
    """
    Nettoie et prépare les données pour l'analyse.

    Args:
        data (ClientData): Les données à nettoyer.

    Returns:
        ClientData: Un nouvel objet ClientData avec les données nettoyées.
    """
    # Reconstruire un dictionnaire pour les données nettoyées
    cleaned_data = {}
    for column in data.columns:
        col_data = getattr(data, column)
        cleaned_data[column] = col_data.data.copy()

    # Convertir 'month' en numérique
    if 'month' in data.columns:
        cleaned_data['month'] = [month_convert(m) for m in cleaned_data['month']]

    # Convertir autres variables catégorielles avec peu de modalités
    for column in data.columns:
        col_data = getattr(data, column)
        if col_data.type == 'str' and column != 'month':  # Ne pas traiter month deux fois
            unique_values = col_data.unique()
            # Petit nombre de modalités
            if len(unique_values) <= 5:
                # paire valeur -> index
                value_map = {val: idx for idx, val in enumerate(sorted(unique_values))}
                cleaned_data[column] = [value_map[val] for val in cleaned_data[column]]

    # Remplacer pdays=999 par -1
    if 'pdays' in data.columns:
        cleaned_data['pdays'] = [-1 if val == 999 else val for val in cleaned_data['pdays']]

    # Identifier les lignes avec plus de 10 valeurs manquantes
    missing_values = ['unknown', None]
    n_rows = len(cleaned_data[data.columns[0]])  # Nombre de lignes
    rows_to_keep = []

    for i in range(n_rows):
        missing_count = sum(1 for column in data.columns
                            if str(cleaned_data[column][i]).strip() in missing_values)
        if missing_count <= 10:
            rows_to_keep.append(i)

    # Filtrer les données pour garder seulement les lignes valides
    for column in data.columns:
        cleaned_data[column] = [cleaned_data[column][i] for i in rows_to_keep]

    # Afficher le nombre de lignes supprimées
    print(f"Nombre de lignes supprimées: {n_rows - len(rows_to_keep)}")

    # Créer et retourner un nouvel objet ClientData
    return ClientData(columns=data.columns, data=cleaned_data)
