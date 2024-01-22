from pathlib import Path

path = {"root": Path(__file__).parent.parent.resolve()}
path["data"] = path["root"] / "data"
credential = (path["data"] / "credential.txt").read_text().splitlines()
mongo_uri = "mongodb+srv://{0}:{1}@{2}/{3}?retryWrites=true&w=majority".format(
    *credential
)
