"""Prototype squad data used while the scraper is still young."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SeedPlayer:
    name: str
    position: str
    scarcity: int = 100
    image_url: str | None = None


@dataclass(frozen=True)
class SeedCountry:
    code: str
    name: str
    wikipedia_url: str
    stripe_colors: tuple[str, ...]
    players: tuple[SeedPlayer, ...]


WIKIPEDIA_TEAMS: tuple[SeedCountry, ...] = (
    SeedCountry(
        code="ARG",
        name="Argentina",
        wikipedia_url="https://en.wikipedia.org/wiki/Argentina_national_football_team#Current_squad",
        stripe_colors=("#75aadb", "#ffffff", "#75aadb"),
        players=(
            SeedPlayer(
                "Emiliano Martinez",
                "Goalkeeper",
                80,
                "https://upload.wikimedia.org/wikipedia/commons/4/41/St._Louis_City_vs_Aston_Villa_%28Jul_2025%29_14_%28Emiliano_Mart%C3%ADnez%29.jpg",
            ),
            SeedPlayer(
                "Cristian Romero",
                "Defender",
                90,
                "https://upload.wikimedia.org/wikipedia/commons/9/9a/Cristian_Romero_WC2022.jpg",
            ),
            SeedPlayer(
                "Enzo Fernandez",
                "Midfielder",
                85,
                "https://upload.wikimedia.org/wikipedia/commons/0/0a/Enzo_Fern%C3%A1ndez_2025_FIFA_Club_World_Cup_Final.jpg",
            ),
            SeedPlayer(
                "Rodrigo De Paul",
                "Midfielder",
                95,
                "https://upload.wikimedia.org/wikipedia/commons/d/df/Rodrigo_De_Paul_NYCFC_Miami_24_Sep_2025-018_%28cropped%29.jpg",
            ),
            SeedPlayer(
                "Julian Alvarez",
                "Forward",
                70,
                "https://upload.wikimedia.org/wikipedia/commons/3/34/Juli%C3%A1n_%C3%81lvarez_%28footballer%29_2023.jpg",
            ),
            SeedPlayer(
                "Lionel Messi",
                "Forward",
                25,
                "https://upload.wikimedia.org/wikipedia/commons/6/6b/Lionel_Messi_White_House_2026_%283x4_cropped%29.jpg",
            ),
        ),
    ),
    SeedCountry(
        code="BRA",
        name="Brazil",
        wikipedia_url="https://en.wikipedia.org/wiki/Brazil_national_football_team#Current_squad",
        stripe_colors=("#009739", "#ffdf00", "#002776"),
        players=(
            SeedPlayer(
                "Alisson",
                "Goalkeeper",
                85,
                "https://upload.wikimedia.org/wikipedia/commons/4/4f/20180610_FIFA_Friendly_Match_Austria_vs._Brazil_850_1625.jpg",
            ),
            SeedPlayer(
                "Marquinhos",
                "Defender",
                90,
                "https://upload.wikimedia.org/wikipedia/commons/d/dc/FC_Salzburg_gegen_Paris_Saint-Germain_UEFA_Champions_League_49_%28cropped%29.jpg",
            ),
            SeedPlayer(
                "Bruno Guimaraes",
                "Midfielder",
                95,
                "https://upload.wikimedia.org/wikipedia/commons/8/8e/Bruno_Guimar%C3%A3es.png",
            ),
            SeedPlayer(
                "Lucas Paqueta",
                "Midfielder",
                100,
                "https://upload.wikimedia.org/wikipedia/commons/d/dc/Lucas_Paquet%C3%A1_of_West_Ham.jpeg",
            ),
            SeedPlayer(
                "Vinicius Junior",
                "Forward",
                45,
                "https://upload.wikimedia.org/wikipedia/commons/c/c6/2023_05_06_Final_de_la_Copa_del_Rey_-_52879242230_%28cropped%29.jpg",
            ),
            SeedPlayer(
                "Rodrygo",
                "Forward",
                65,
                "https://upload.wikimedia.org/wikipedia/commons/0/05/Rodrygo_2023_%28cropped%29.jpg",
            ),
        ),
    ),
    SeedCountry(
        code="FRA",
        name="France",
        wikipedia_url="https://en.wikipedia.org/wiki/France_national_football_team#Current_squad",
        stripe_colors=("#0055a4", "#ffffff", "#ef4135"),
        players=(
            SeedPlayer(
                "Mike Maignan",
                "Goalkeeper",
                90,
                "https://upload.wikimedia.org/wikipedia/commons/e/e1/Mike_Maignan_2022_Salzburg_vs_AC_Milan_2022-09-06.jpg",
            ),
            SeedPlayer(
                "William Saliba",
                "Defender",
                85,
                "https://upload.wikimedia.org/wikipedia/commons/8/8a/1_william_saliba_arsenal_2025_%28cropped%29.jpg",
            ),
            SeedPlayer(
                "Aurelien Tchouameni",
                "Midfielder",
                90,
                "https://upload.wikimedia.org/wikipedia/commons/0/0f/2025_04_26_Final_de_la_Copa_del_Rey_-_Aur%C3%A9lien_Tchouam%C3%A9ni.jpg",
            ),
            SeedPlayer(
                "Antoine Griezmann",
                "Forward",
                70,
                "https://upload.wikimedia.org/wikipedia/commons/6/6e/FRA-ARG_%2810%29_%28cropped%29.jpg",
            ),
            SeedPlayer(
                "Kylian Mbappe",
                "Forward",
                30,
                "https://upload.wikimedia.org/wikipedia/commons/6/66/Picture_with_Mbapp%C3%A9_%28cropped_and_rotated%29.jpg",
            ),
            SeedPlayer(
                "Ousmane Dembele",
                "Forward",
                75,
                "https://upload.wikimedia.org/wikipedia/commons/4/4a/Ousmane_Demb%C3%A9l%C3%A9_2018_%28cropped%29.jpg",
            ),
        ),
    ),
)
