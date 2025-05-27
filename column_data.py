from dataclasses import dataclass
import statistics


@dataclass
class ColumnData:
    """
    Une classe pour représenter les données d'une colonne dans un tableau.
    Elle contient le nom de la colonne et les données associées.
    Attributes:
        name (str): Le nom de la colonne.
        data (list): Les données de la colonne.
        type (str): Le type de données de la colonne (optionnel).
    """
    name: str
    data: list
    type: str = None

    def __repr__(self):
        """
        Méthode pour représenter l'objet sous forme de chaîne de caractères.
        Elle retourne le nom de la colonne et les données associées.
        """
        return str(self.data)

    def __str__(self):
        """
        Affiche la colonne sous forme de tableau
        """
        # Limiter le nombre de lignes affichées
        max_display_rows = 20

        # Déterminer la largeur de la colonne
        col_data_strs = [str(item) for item in self.data[:max_display_rows]]
        col_width = max(len(self.name), max(len(s) for s in col_data_strs) if col_data_strs else 0)

        # Les séparateurs
        separator = "+" + "-" * (col_width + 2) + "+"

        # L'en-tête
        header = "| " + self.name.ljust(col_width) + " |"

        # Les lignes de données
        rows = []
        num_rows = min(max_display_rows, len(self.data))

        for i in range(num_rows):
            value = str(self.data[i])
            rows.append("| " + value.ljust(col_width) + " |")

        # Construire la colonne
        column = separator + "\n" + header + "\n" + separator + "\n"
        column += "\n".join(rows)
        column += "\n" + separator

        # Indication si les données sont tronquées
        if len(self.data) > max_display_rows:
            column += f"\n... {len(self.data) - max_display_rows} lignes supplémentaires non affichées ...\n"

        return column

    def __post_init__(self):
        """
        Méthode appelée après l'initialisation de l'objet.
        Elle permet de définir le type de données de la colonne si ce n'est pas déjà fait.
        """
        if self.type is None:
            # Verifier si le type string peut être converti en int
            try:
                self.data = [int(value) for value in self.data]
                self.type = 'int'
            except ValueError:
                # Si la conversion échoue, essayer de convertir en float
                try:
                    self.data = [float(value) for value in self.data]
                    self.type = 'float'
                except ValueError:
                    # Si la conversion échoue, garder le type string
                    self.type = 'str'

    def unique(self):
        """
        Retourne une liste des valeurs uniques dans la colonne.
        """
        return list(set(self.data))

    def value_counts(self):
        """
        Retourne un dictionnaire avec les valeurs uniques et leur fréquence dans la colonne.
        """
        counts = {}
        for value in self.unique(): # Obtenir les valeurs uniques
            counts[value] = self.data.count(value) # Compter les occurrences de chaque valeur unique
        return counts

    def stats(self):
        """
        Retourne un dictionnaire avec les statistiques de la colonne.
        """
        if self.type in ['int', 'float']:
            return {
                'mean': statistics.mean(self.data),
                'median': statistics.median(self.data),
                'mode': statistics.mode(self.data),
                'min': min(self.data),
                'max': max(self.data),
                'std_dev': statistics.stdev(self.data)
            }
        else:
            return None