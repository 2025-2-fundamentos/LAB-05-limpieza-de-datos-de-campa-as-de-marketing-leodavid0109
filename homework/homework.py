"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """
    import os

    df = _read_all_data()

    out_dir = os.path.join("files", "output")
    os.makedirs(out_dir, exist_ok=True)

    client = _clean_client(df)
    client.to_csv(os.path.join(out_dir, "client.csv"), index=False)

    campaign = _clean_campaign(df)

    campaign.to_csv(os.path.join(out_dir, "campaign.csv"), index=False)

    economics = _clean_economics(df)
    economics.to_csv(os.path.join(out_dir, "economics.csv"), index=False)

    return


if __name__ == "__main__":
    clean_campaign_data()

# pylint: disable=import-outside-toplevel


def _read_all_data():
    import os
    import pandas as pd

    input_dir = os.path.join("files", "input")
    dfs = []
    for fname in sorted(os.listdir(input_dir)):
        if not fname.endswith(".zip"):
            continue
        path = os.path.join(input_dir, fname)
        df = pd.read_csv(path, compression="zip", index_col=0)
        dfs.append(df)
    if dfs:
        return pd.concat(dfs, ignore_index=True)
    import pandas as _pd

    return _pd.DataFrame()


def _clean_client(df):
    import pandas as pd

    client = df[
        [
            "client_id",
            "age",
            "job",
            "marital",
            "education",
            "credit_default",
            "mortgage",
        ]
    ].copy()

    client["job"] = client["job"].astype(str).str.replace(".", "", regex=False)
    client["job"] = client["job"].astype(str).str.replace("-", "_", regex=False)

    client["education"] = client["education"].astype(str).str.replace(".", "_", regex=False)
    client.loc[client["education"].str.lower() == "unknown", "education"] = pd.NA

    client["credit_default"] = client["credit_default"].astype(str).map(lambda x: 1 if x.lower() == "yes" else 0)

    client["mortgage"] = client["mortgage"].astype(str).map(lambda x: 1 if x.lower() == "yes" else 0)

    return client


def _clean_campaign(df):
    import pandas as pd

    camp = df[
        [
            "client_id",
            "number_contacts",
            "contact_duration",
            "previous_campaign_contacts",
            "previous_outcome",
            "campaign_outcome",
            "month",
            "day",
        ]
    ].copy()

    camp["previous_outcome"] = camp["previous_outcome"].astype(str).map(lambda x: 1 if x.lower() == "success" else 0)

    camp["campaign_outcome"] = camp["campaign_outcome"].astype(str).map(lambda x: 1 if x.lower() == "yes" else 0)

    month_map = {
        "jan": 1,
        "feb": 2,
        "mar": 3,
        "apr": 4,
        "may": 5,
        "jun": 6,
        "jul": 7,
        "aug": 8,
        "sep": 9,
        "oct": 10,
        "nov": 11,
        "dec": 12,
        "january": 1,
        "february": 2,
        "march": 3,
        "april": 4,
        "june": 6,
        "july": 7,
        "august": 8,
        "september": 9,
        "october": 10,
        "november": 11,
        "december": 12,
    }

    def make_date(row):
        m = str(row["month"]).strip().lower()
        mon = month_map.get(m)
        if mon is None:
            try:
                mon = int(m)
            except Exception:
                mon = 1
        try:
            day = int(row["day"])
        except Exception:
            day = 1
        return f"2022-{mon:02d}-{day:02d}"

    camp["last_contact_date"] = camp.apply(make_date, axis=1)

    camp = camp.drop(columns=["month", "day"])

    return camp


def _clean_economics(df):
    econ = df[["client_id", "cons_price_idx", "euribor_three_months"]].copy()
    return econ


if __name__ == "__main__":
    clean_campaign_data()
