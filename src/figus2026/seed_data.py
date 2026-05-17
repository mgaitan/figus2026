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
    coach: str | None = None
    federation_name: str | None = None
    federation_logo_url: str | None = None


WIKIPEDIA_TEAMS: tuple[SeedCountry, ...] = (
    SeedCountry(
        code="ARG",
        name="Argentina",
        wikipedia_url="https://en.wikipedia.org/wiki/Argentina_national_football_team#Current_squad",
        stripe_colors=("#75aadb", "#ffffff", "#75aadb"),
        coach="Lionel Scaloni",
        federation_name="Asociación del Fútbol Argentino",
        federation_logo_url="https://upload.wikimedia.org/wikipedia/en/c/c1/Argentina_football_badge.svg",
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
        coach="Dorival Júnior",
        federation_name="Confederação Brasileira de Futebol",
        federation_logo_url="https://upload.wikimedia.org/wikipedia/en/0/09/Brazil_football_badge.svg",
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
        coach="Didier Deschamps",
        federation_name="Fédération Française de Football",
        federation_logo_url="https://upload.wikimedia.org/wikipedia/en/e/e2/FFF.svg",
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
    SeedCountry(
        code="USA",
        name="United States",
        wikipedia_url="https://en.wikipedia.org/wiki/United_States_men%27s_national_soccer_team#Current_squad",
        stripe_colors=("#002868", "#ffffff", "#BF0A30"),
        coach="Mauricio Pochettino",
        federation_name="U.S. Soccer Federation",
        federation_logo_url="https://upload.wikimedia.org/wikipedia/commons/a/a6/United_States_Soccer_Federation_%28crest%29.svg",
        players=(
            SeedPlayer("Matt Turner", "Goalkeeper", 95),
            SeedPlayer("Sergiño Dest", "Defender", 85),
            SeedPlayer("Tyler Adams", "Midfielder", 80),
            SeedPlayer("Weston McKennie", "Midfielder", 85),
            SeedPlayer(
                "Christian Pulisic",
                "Forward",
                40,
                "https://upload.wikimedia.org/wikipedia/commons/e/e6/Christian_Pulisic_2022_%28cropped%29.jpg",
            ),
            SeedPlayer("Folarin Balogun", "Forward", 75),
        ),
    ),
    SeedCountry(
        code="MEX",
        name="Mexico",
        wikipedia_url="https://en.wikipedia.org/wiki/Mexico_national_football_team#Current_squad",
        stripe_colors=("#006847", "#ffffff", "#CE1126"),
        coach="Javier Aguirre",
        federation_name="Federación Mexicana de Fútbol",
        federation_logo_url="https://upload.wikimedia.org/wikipedia/en/3/3a/FMF_%28Mexican_Football_Federation%29_logo.svg",
        players=(
            SeedPlayer("Guillermo Ochoa", "Goalkeeper", 70),
            SeedPlayer("César Montes", "Defender", 90),
            SeedPlayer("Edson Álvarez", "Midfielder", 75),
            SeedPlayer("Orbelin Pineda", "Midfielder", 95),
            SeedPlayer("Hirving Lozano", "Forward", 65),
            SeedPlayer("Raúl Jiménez", "Forward", 80),
        ),
    ),
    SeedCountry(
        code="CAN",
        name="Canada",
        wikipedia_url="https://en.wikipedia.org/wiki/Canada_men%27s_national_soccer_team#Current_squad",
        stripe_colors=("#FF0000", "#ffffff", "#FF0000"),
        coach="Jesse Marsch",
        federation_name="Canada Soccer",
        federation_logo_url="https://upload.wikimedia.org/wikipedia/en/2/21/Canada_Soccer_Logo.svg",
        players=(
            SeedPlayer("Maxime Crépeau", "Goalkeeper", 90),
            SeedPlayer("Alistair Johnston", "Defender", 85),
            SeedPlayer("Stephen Eustaquio", "Midfielder", 80),
            SeedPlayer("Tajon Buchanan", "Midfielder", 85),
            SeedPlayer(
                "Alphonso Davies",
                "Defender",
                35,
                "https://upload.wikimedia.org/wikipedia/commons/1/15/Alphonso_Davies_2022_%28cropped%29.jpg",
            ),
            SeedPlayer("Jonathan David", "Forward", 50),
        ),
    ),
    SeedCountry(
        code="ESP",
        name="Spain",
        wikipedia_url="https://en.wikipedia.org/wiki/Spain_national_football_team#Current_squad",
        stripe_colors=("#AA151B", "#F1BF00", "#AA151B"),
        coach="Luis de la Fuente",
        federation_name="Real Federación Española de Fútbol",
        federation_logo_url="https://upload.wikimedia.org/wikipedia/en/d/d7/RFEF.svg",
        players=(
            SeedPlayer("Unai Simón", "Goalkeeper", 85),
            SeedPlayer("Dani Carvajal", "Defender", 80),
            SeedPlayer(
                "Rodri",
                "Midfielder",
                45,
                "https://upload.wikimedia.org/wikipedia/commons/b/b2/Rodri_euro2024.jpg",
            ),
            SeedPlayer("Pedri", "Midfielder", 55),
            SeedPlayer(
                "Lamine Yamal",
                "Forward",
                20,
                "https://upload.wikimedia.org/wikipedia/commons/7/7a/Lamine_Yamal_Euro_2024_final.jpg",
            ),
            SeedPlayer("Álvaro Morata", "Forward", 75),
        ),
    ),
    SeedCountry(
        code="ENG",
        name="England",
        wikipedia_url="https://en.wikipedia.org/wiki/England_national_football_team#Current_squad",
        stripe_colors=("#ffffff", "#003399", "#ffffff"),
        coach="Thomas Tuchel",
        federation_name="The Football Association",
        federation_logo_url="https://upload.wikimedia.org/wikipedia/commons/e/e7/The_FA_logo.svg",
        players=(
            SeedPlayer("Jordan Pickford", "Goalkeeper", 85),
            SeedPlayer("Trent Alexander-Arnold", "Defender", 65),
            SeedPlayer(
                "Jude Bellingham",
                "Midfielder",
                30,
                "https://upload.wikimedia.org/wikipedia/commons/2/2c/Jude_Bellingham_2022_%28cropped%29.jpg",
            ),
            SeedPlayer("Declan Rice", "Midfielder", 70),
            SeedPlayer(
                "Harry Kane",
                "Forward",
                50,
                "https://upload.wikimedia.org/wikipedia/commons/4/48/Harry_Kane_2022_%28cropped%29.jpg",
            ),
            SeedPlayer("Phil Foden", "Forward", 60),
        ),
    ),
    SeedCountry(
        code="GER",
        name="Germany",
        wikipedia_url="https://en.wikipedia.org/wiki/Germany_national_football_team#Current_squad",
        stripe_colors=("#000000", "#ffffff", "#DD0000"),
        coach="Julian Nagelsmann",
        federation_name="Deutscher Fußball-Bund",
        federation_logo_url="https://upload.wikimedia.org/wikipedia/commons/2/2f/DFB-Logo_2024.svg",
        players=(
            SeedPlayer("Manuel Neuer", "Goalkeeper", 65),
            SeedPlayer("Antonio Rüdiger", "Defender", 75),
            SeedPlayer("Joshua Kimmich", "Midfielder", 70),
            SeedPlayer(
                "Florian Wirtz",
                "Midfielder",
                40,
                "https://upload.wikimedia.org/wikipedia/commons/5/5a/Florian_Wirtz_-_UEFA_Euro_2024_%28cropped%29.jpg",
            ),
            SeedPlayer("Kai Havertz", "Forward", 75),
            SeedPlayer("Jamal Musiala", "Forward", 45),
        ),
    ),
    SeedCountry(
        code="POR",
        name="Portugal",
        wikipedia_url="https://en.wikipedia.org/wiki/Portugal_national_football_team#Current_squad",
        stripe_colors=("#006600", "#FF0000", "#006600"),
        coach="Roberto Martínez",
        federation_name="Federação Portuguesa de Futebol",
        federation_logo_url="https://upload.wikimedia.org/wikipedia/en/f/f8/Federa%C3%A7%C3%A3o_Portuguesa_de_Futebol_logo.svg",
        players=(
            SeedPlayer("Rui Patrício", "Goalkeeper", 85),
            SeedPlayer("Rúben Dias", "Defender", 65),
            SeedPlayer("Bruno Fernandes", "Midfielder", 60),
            SeedPlayer("Bernardo Silva", "Midfielder", 65),
            SeedPlayer(
                "Cristiano Ronaldo",
                "Forward",
                15,
                "https://upload.wikimedia.org/wikipedia/commons/8/8c/Cristiano_Ronaldo_2018.jpg",
            ),
            SeedPlayer("Rafael Leão", "Forward", 70),
        ),
    ),
    SeedCountry(
        code="URU",
        name="Uruguay",
        wikipedia_url="https://en.wikipedia.org/wiki/Uruguay_national_football_team#Current_squad",
        stripe_colors=("#75aadb", "#ffffff", "#75aadb"),
        coach="Marcelo Bielsa",
        federation_name="Asociación Uruguaya de Fútbol",
        federation_logo_url="https://upload.wikimedia.org/wikipedia/commons/1/16/Logo_AUF.svg",
        players=(
            SeedPlayer("Sergio Rochet", "Goalkeeper", 90),
            SeedPlayer("José María Giménez", "Defender", 80),
            SeedPlayer("Rodrigo Bentancur", "Midfielder", 75),
            SeedPlayer(
                "Federico Valverde",
                "Midfielder",
                45,
                "https://upload.wikimedia.org/wikipedia/commons/0/09/Federico_Valverde_2022_%28cropped%29.jpg",
            ),
            SeedPlayer("Darwin Núñez", "Forward", 55),
            SeedPlayer("Facundo Torres", "Forward", 85),
        ),
    ),
    SeedCountry(
        code="COL",
        name="Colombia",
        wikipedia_url="https://en.wikipedia.org/wiki/Colombia_national_football_team#Current_squad",
        stripe_colors=("#FCD116", "#003087", "#CE1126"),
        coach="Néstor Lorenzo",
        federation_name="Federación Colombiana de Fútbol",
        federation_logo_url="https://upload.wikimedia.org/wikipedia/commons/4/44/FCF.svg",
        players=(
            SeedPlayer("Camilo Vargas", "Goalkeeper", 90),
            SeedPlayer("Yerry Mina", "Defender", 80),
            SeedPlayer("Juan Cuadrado", "Midfielder", 80),
            SeedPlayer(
                "James Rodríguez",
                "Midfielder",
                50,
                "https://upload.wikimedia.org/wikipedia/commons/5/5c/James_Rodr%C3%ADguez_2018_%28cropped%29.jpg",
            ),
            SeedPlayer(
                "Luis Díaz",
                "Forward",
                45,
                "https://upload.wikimedia.org/wikipedia/commons/0/07/Luis_D%C3%ADaz_%28Colombia%29_2022_%28cropped%29.jpg",
            ),
            SeedPlayer("Jhon Córdoba", "Forward", 85),
        ),
    ),
)
