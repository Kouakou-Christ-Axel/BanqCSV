from banq import load_csv_data, preprocess_data
from utils import filter_by_age, calculate_subscription_rate, most_common_job

data = load_csv_data('bank.csv')

cleaned_data = preprocess_data(data)

filtered_data = filter_by_age(cleaned_data, 30, 40)

# Afficher les 5 premières lignes du tableau filtré
print(filtered_data)

print(f"Taux de souscription pour les clients âgés de 30 à 40 ans : {calculate_subscription_rate(filtered_data):.2%}")

print(f"Le métier le plus courant parmi les clients âgés de 30 à 40 ans : {most_common_job(filtered_data)}")

# Afficher les statistiques de la colonne 'age'
print("Statistiques de la colonne 'age' :")
age_column = filtered_data.age
print(age_column.stats())

# Afficher les statistiques du tableau
print("Statistiques de data :")
print("*" * 20)
data.stats()

print("*" * 20)
print("sauvegarde des données dans le fichier 'bank_cleaned.csv'")

filtered_data.save_csv('bank_filtered.csv')
