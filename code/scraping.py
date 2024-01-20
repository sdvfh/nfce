from pathlib import Path

import requests
import xmltodict
from pymongo import MongoClient

path = {"root": Path(__file__).parent.parent.resolve()}
path["data"] = path["root"] / "data"
credential = (path["data"] / "credential.txt").read_text().splitlines()
mongo_uri = "mongodb+srv://{0}:{1}@{2}/{3}?retryWrites=true&w=majority".format(
    *credential
)
client = MongoClient(mongo_uri)
db = client["nfce"]
collection = db["raw"]

entries = (path["files"] / "inputs.txt").read_text().splitlines()

for entry in entries:
    if "chNFe" in entry:
        master_key = entry.split("chNFe=")[1].split("&nVersao")[0]
        uri = f"http://nfce.sefaz.pe.gov.br/nfce-web/consultarNFCe?p={master_key}"
        response = requests.get(uri)
    elif not entry.startswith("http"):
        uri = f"http://nfce.sefaz.pe.gov.br/nfce-web/consultarNFCe?p={entry}"
        response = requests.get(uri)
    else:
        uri = entry
        response = requests.get(entry)
    dict_data = xmltodict.parse(response.content)["nfeProc"]
    dict_data["requisicao"] = uri
    db_response = collection.replace_one({"requisicao": uri}, dict_data, upsert=True)
    print(db_response.raw_result)

with open(path["files"] / "inputs.txt", "w") as file:
    file.truncate(0)
