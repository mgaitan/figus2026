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
    players: tuple[SeedPlayer, ...]


WIKIPEDIA_TEAMS: tuple[SeedCountry, ...] = (
    SeedCountry(
        code="ARG",
        name="Argentina",
        wikipedia_url="https://en.wikipedia.org/wiki/Argentina_national_football_team#Current_squad",
        players=(
            SeedPlayer("Emiliano Martinez", "Goalkeeper", 80),
            SeedPlayer("Cristian Romero", "Defender", 90),
            SeedPlayer("Enzo Fernandez", "Midfielder", 85),
            SeedPlayer("Rodrigo De Paul", "Midfielder", 95),
            SeedPlayer("Julian Alvarez", "Forward", 70),
            SeedPlayer("Lionel Messi", "Forward", 25),
        ),
    ),
    SeedCountry(
        code="BRA",
        name="Brazil",
        wikipedia_url="https://en.wikipedia.org/wiki/Brazil_national_football_team#Current_squad",
        players=(
            SeedPlayer("Alisson", "Goalkeeper", 85),
            SeedPlayer("Marquinhos", "Defender", 90),
            SeedPlayer("Bruno Guimaraes", "Midfielder", 95),
            SeedPlayer("Lucas Paqueta", "Midfielder", 100),
            SeedPlayer("Vinicius Junior", "Forward", 45),
            SeedPlayer("Rodrygo", "Forward", 65),
        ),
    ),
    SeedCountry(
        code="FRA",
        name="France",
        wikipedia_url="https://en.wikipedia.org/wiki/France_national_football_team#Current_squad",
        players=(
            SeedPlayer("Mike Maignan", "Goalkeeper", 90),
            SeedPlayer("William Saliba", "Defender", 85),
            SeedPlayer("Aurelien Tchouameni", "Midfielder", 90),
            SeedPlayer("Antoine Griezmann", "Forward", 70),
            SeedPlayer("Kylian Mbappe", "Forward", 30),
            SeedPlayer("Ousmane Dembele", "Forward", 75),
        ),
    ),
)
