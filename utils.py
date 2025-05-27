from client_data import ClientData


def filter_by_age(data: ClientData, min_age: int, max_age: int) -> ClientData:
    """
    Filtre les données des clients en fonction de leur âge.
    Args:
        data (ClientData): Les données des clients à filtrer.
        min_age (int): L'âge minimum pour le filtre.
        max_age (int): L'âge maximum pour le filtre.
    Returns:
        ClientData: Les données filtrées des clients.
    """

    filtered_data = {col: [] for col in data.columns}
    for i in range(data.dimensions[0]):  # le nombre de lignes
        age = int(data.age.data[i])  # Convertir l'âge en entier
        if min_age <= age <= max_age:
            for col in data.columns:
                filtered_data[col].append(getattr(data, col).data[i])  # Obtenir la valeur de la colonne
    return ClientData(columns=data.columns, data=filtered_data)


def calculate_subscription_rate(data: ClientData) -> float:
    """
    Calcule le taux de souscription.
    Args:
        data (ClientData): Les données des clients.
    Returns:
        float: Le taux de souscription.
    """

    total_clients = data.dimensions[0]
    subscribed_clients = sum(
        1 for i in range(total_clients) if data.y.data[i] == 1)  # compte le nombre de clients ayant souscrit
    return subscribed_clients / total_clients if total_clients > 0 else 0.0


def most_common_job(data: ClientData) -> str:
    """
    Trouve le métier le plus courant parmi les clients.
    Args:
        data (ClientData): Les données des clients.
    Returns:
        str: Le métier le plus courant.
    """

    job_counts = {}
    for i in range(data.dimensions[0]):  # le nombre de lignes
        job = data.job.data[i]
        if job in job_counts:
            job_counts[job] += 1
        else:
            job_counts[job] = 1
    return max(job_counts, key=job_counts.get)  # max retourne la clé avec la valeur maximale
