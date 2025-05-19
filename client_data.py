from dataclasses import dataclass
from column_data import ColumnData
import statistics


@dataclass
class ClientData:
    """
    Une classe pour représenter les données d'un client dans un tableau.
    Elle contient les colonnes du tableau, ses dimensions et les données associées.
    Attributes:
        columns (list): La liste des colonnes du tableau.
        dimensions (tuple): Les dimensions du tableau (nombre de lignes, nombre de colonnes).
        data (dict): Un dictionnaire contenant les données du tableau.
    """
    columns: list
    data: dict | None = None
    dimensions: tuple = None

    # Creer un attribut ColumnData pour chaque colonne
    def __post_init__(self):
        """
        Méthode appelée après l'initialisation de l'objet.
        Elle permet de définir les attributs de chaque colonne et de calculer les dimensions du tableau.
        """

        # Créer un attribut ColumnData pour chaque colonne
        for column in self.columns:
            setattr(self, column, ColumnData(column, self.data[column]))

        # Calculer les dimensions du tableau
        setattr(self, 'dimensions', (len(self.data[self.columns[0]]), len(self.columns)))

        # Supprimer l'attribut data pour éviter la redondance
        del self.data

    def __getattr__(self, item):
        """
        Méthode pour accéder aux attributs de l'objet.
        Elle permet d'accéder aux données de chaque colonne en utilisant le nom de la colonne.
        """
        if item in self.columns:
            return getattr(self, item)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")

    def __str__(self):
        """
        Retourner les donnees sous forme de tableau avec les headers
        """
        # Limiter le nombre de lignes affichées
        max_display_rows = 20

        # Determiner la largeur de chaque colonne
        col_widths = {}
        for col in self.columns:
            col_data = getattr(self, col).data
            col_data_strs = [str(item) for item in col_data[:max_display_rows]]
            col_widths[col] = max(len(col), max(len(s) for s in col_data_strs) if col_data_strs else 0)

        # Les séparateurs de colonnes
        separator = "+" + "+".join("-" * (col_widths[col] + 2) for col in self.columns) + "+"

        # Les en-têtes de colonnes
        header = "| " + " | ".join(col.ljust(col_widths[col]) for col in self.columns) + " |"

        # Les lignes de données
        rows = []
        num_rows = min(max_display_rows, self.dimensions[0])

        for i in range(num_rows):
            row_data = []
            for col in self.columns:
                col_data = getattr(self, col).data  # Obtenir les données de la colonne
                value = str(col_data[i]) if i < len(
                    col_data) else ""  # Si la colonne a moins de lignes que max_display_rows
                row_data.append(value.ljust(col_widths[col]))  # Aligner à gauche
            rows.append("| " + " | ".join(row_data) + " |")

        # Construire le tableau
        table = separator + "\n" + header + "\n" + separator + "\n"
        table += "\n".join(rows)
        table += "\n" + separator

        # Add indication if data is truncated
        if self.dimensions[0] > max_display_rows:
            table += f"\n... {self.dimensions[0] - max_display_rows} lignes supplémentaires non affichées ...\n"

        return table

    def get_row(self, index: int) -> dict:
        """
        Retourne une ligne de données sous forme de dictionnaire.
        Args:
            index (int): L'index de la ligne à retourner.
        Returns:
            dict: Un dictionnaire contenant les données de la ligne spécifiée.
        """
        row_data = {}
        for col in self.columns:
            col_data = getattr(self, col).data
            row_data[col] = col_data[index] if index < len(col_data) else None
        return row_data

    def stats(self):
        """
        Affiche les statistiques de chaque colonne.
        Returns:
            str: Une chaîne formatée contenant les statistiques de chaque colonne.
        """
        for col in self.columns:
            col_stats = getattr(self, col).stats()
            print(f"\nStatistiques de la colonne '{col}':")
            print(col_stats)

    def save_csv(self, filename: str):
        """
        Enregistre les données dans un fichier CSV.
        Args:
            filename (str): Le nom du fichier CSV de sortie.
        """
        with open(filename, mode='w') as file:
            # Écrire l'en-tête
            file.write(",".join(self.columns) + "\n")

            # Écrire les données
            for i in range(self.dimensions[0]):
                row_data = []
                for col in self.columns:
                    col_data = getattr(self, col).data
                    value = col_data[i] if i < len(col_data) else ""
                    row_data.append(str(value))
                file.write(",".join(row_data) + "\n")

    def save_json(self, filename: str):
        """
        Enregistre les données dans un fichier JSON.
        Args:
            filename (str): Le nom du fichier JSON de sortie.
        """
        import json
        with open(filename, mode='w') as file:
            json_data = {col: getattr(self, col).data for col in self.columns}
            json.dump(json_data, file, indent=4)

    def save(self, filename: str = "data.csv", mode: str = "csv"):
        """
        Enregistre les données dans un fichier au format spécifié.
        Args:
            mode (str): Le format de fichier (csv ou json).
            filename (str): Le nom du fichier de sortie.
        """
        if mode == "csv":
            self.save_csv(filename)
        elif mode == "json":
            self.save_json(filename)
        else:
            raise ValueError("Format non pris en charge. Utilisez 'csv' ou 'json'.")
