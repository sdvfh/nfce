import requests
import xmltodict
from pymongo import MongoClient
from utils import mongo_uri, path

client = MongoClient(mongo_uri)
db = client["nfce"]
collection = db["raw"]

entries = (path["data"] / "inputs.txt").read_text().splitlines()

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

with open(path["data"] / "inputs.txt", "w") as file:
    file.truncate(0)
