from insert import insert_author
from utils import read_csv

def import_author_from_csv(filename: str) -> None:
    authors = read_csv(filename)
    for author in authors:
        insert_author(*author)