import football_scrapper
from database import Database


if __name__ == "__main__":
    # matches = football_scrapper.read_wiki_match(ignore_keys=["attendance"])
    matches = football_scrapper.read_wiki_match()
    Database("database/football.db").insert_matches(matches, 53, is_test=True)
