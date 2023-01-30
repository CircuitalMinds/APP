from pathlib import Path
path = Path(__file__).parent
downloads = path.joinpath("downloads")
metadata = path.joinpath("metadata")
library = path.joinpath("library.csv")
playlist = path.joinpath("playlist.csv")



def getfile(name):
    filepath = path.joinpath()
