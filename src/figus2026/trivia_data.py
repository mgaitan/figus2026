"""50 multiple-choice trivia questions for the World Cup 2026 album."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SeedQuestion:
    text: str
    correct_answer: str
    wrong_answers: tuple[str, str, str]
    category: str


TRIVIA_QUESTIONS: tuple[SeedQuestion, ...] = (
    SeedQuestion(
        "¿Quién anotó el primer gol de Argentina contra México en el Mundial 2022?",
        "Lionel Messi",
        ("Julián Álvarez", "Enzo Fernández", "Rodrigo De Paul"),
        "argentina",
    ),
    SeedQuestion(
        "¿Cuántos goles hizo Messi en el Mundial Qatar 2022?",
        "7",
        ("5", "8", "6"),
        "argentina",
    ),
    SeedQuestion(
        "¿Cómo se llama popularmente la selección argentina bajo la conducción de Scaloni?",
        "La Scaloneta",
        ("La Albiceleste Eterna", "Los Pampas", "La Bicolor"),
        "argentina",
    ),
    SeedQuestion(
        "¿Quién fue el técnico de Argentina en el Mundial 2022?",
        "Lionel Scaloni",
        ("Jorge Sampaoli", "Diego Simeone", "Marcelo Bielsa"),
        "argentina",
    ),
    SeedQuestion(
        "¿Cuántos mundiales ganó Argentina antes de 2022?",
        "2",
        ("1", "3", "0"),
        "argentina",
    ),
    SeedQuestion(
        "¿En qué año Argentina ganó su primer Mundial?",
        "1978",
        ("1982", "1986", "1974"),
        "argentina",
    ),
    SeedQuestion(
        "¿Quién es el máximo goleador histórico de la selección argentina?",
        "Lionel Messi",
        ("Gabriel Batistuta", "Hernán Crespo", "Diego Maradona"),
        "argentina",
    ),
    SeedQuestion(
        "¿Qué selección le ganó a Argentina en la fase de grupos del Mundial 2022?",
        "Arabia Saudita",
        ("México", "Polonia", "Australia"),
        "argentina",
    ),
    SeedQuestion(
        "¿Cuántos goles hizo Julián Álvarez en el Mundial 2022?",
        "4",
        ("3", "2", "5"),
        "argentina",
    ),
    SeedQuestion(
        "¿Cuántas Copas América ganó Argentina en total?",
        "16",
        ("14", "15", "17"),
        "argentina",
    ),
    SeedQuestion(
        "¿Quién ganó el Balón de Oro del Mundial Qatar 2022?",
        "Lionel Messi",
        ("Kylian Mbappé", "Julián Álvarez", "Enzo Fernández"),
        "mundial-2022",
    ),
    SeedQuestion(
        "¿Quién ganó la Bota de Oro del Mundial Qatar 2022?",
        "Kylian Mbappé",
        ("Lionel Messi", "Julián Álvarez", "Olivier Giroud"),
        "mundial-2022",
    ),
    SeedQuestion(
        "¿Quién ganó el Guante de Oro (mejor arquero) en el Mundial 2022?",
        "Emiliano Martínez",
        ("Hugo Lloris", "Yassine Bounou", "Dominik Livaković"),
        "mundial-2022",
    ),
    SeedQuestion(
        "¿En qué país se jugó el Mundial 2022?",
        "Qatar",
        ("Arabia Saudita", "Emiratos Árabes Unidos", "Bahréin"),
        "mundial-2022",
    ),
    SeedQuestion(
        "¿En qué ciudad se jugó la final del Mundial 2022?",
        "Lusail",
        ("Doha", "Al Rayyan", "Al Wakrah"),
        "mundial-2022",
    ),
    SeedQuestion(
        "¿Cuántos goles hizo Mbappé en el Mundial 2022?",
        "8",
        ("6", "7", "5"),
        "mundial-2022",
    ),
    SeedQuestion(
        "¿Qué selección africana llegó por primera vez a las semifinales de un Mundial?",
        "Marruecos",
        ("Senegal", "Ghana", "Nigeria"),
        "mundial-2022",
    ),
    SeedQuestion(
        "¿Qué selección eliminó a Brasil en cuartos de final del Mundial 2022?",
        "Croacia",
        ("Argentina", "Francia", "Marruecos"),
        "mundial-2022",
    ),
    SeedQuestion(
        "¿Cuántos goles marcó Francia en la final del Mundial 2022?",
        "3",
        ("2", "4", "1"),
        "mundial-2022",
    ),
    SeedQuestion(
        "¿Cuántos equipos participarán en el Mundial 2026?",
        "48",
        ("32", "40", "36"),
        "mundial-2026",
    ),
    SeedQuestion(
        "¿En qué países se jugará el Mundial 2026?",
        "Estados Unidos, Canadá y México",
        ("Estados Unidos, México y Brasil", "Estados Unidos, Canadá y Costa Rica", "Canadá, México y Cuba"),
        "mundial-2026",
    ),
    SeedQuestion(
        "¿Cuántas sedes tendrá el Mundial 2026 en Estados Unidos?",
        "11",
        ("8", "10", "12"),
        "mundial-2026",
    ),
    SeedQuestion(
        "¿En qué estadio se jugará la final del Mundial 2026?",
        "MetLife Stadium (Nueva York/Nueva Jersey)",
        ("Rose Bowl (Los Ángeles)", "Azteca (Ciudad de México)", "SoFi Stadium (Los Ángeles)"),
        "mundial-2026",
    ),
    SeedQuestion(
        "¿Cuántos mundiales ganó Brasil?",
        "5",
        ("4", "6", "3"),
        "selecciones",
    ),
    SeedQuestion(
        "¿En qué año Brasil ganó su último Mundial?",
        "2002",
        ("1998", "2006", "1994"),
        "selecciones",
    ),
    SeedQuestion(
        "¿Cuántos mundiales ganó Alemania?",
        "4",
        ("3", "5", "6"),
        "selecciones",
    ),
    SeedQuestion(
        "¿En qué año España ganó su único Mundial?",
        "2010",
        ("2006", "2014", "2018"),
        "selecciones",
    ),
    SeedQuestion(
        "¿Cuántos mundiales ganó Uruguay?",
        "2",
        ("1", "3", "0"),
        "selecciones",
    ),
    SeedQuestion(
        "¿Cuál fue la primera selección campeona del mundo?",
        "Uruguay",
        ("Argentina", "Italia", "Brasil"),
        "selecciones",
    ),
    SeedQuestion(
        "¿En qué año se jugó el primer Mundial de fútbol?",
        "1930",
        ("1928", "1934", "1926"),
        "selecciones",
    ),
    SeedQuestion(
        "¿Qué selección ganó el Mundial 2018?",
        "Francia",
        ("Argentina", "Croacia", "Bélgica"),
        "selecciones",
    ),
    SeedQuestion(
        "¿Qué selección ganó la Eurocopa 2024?",
        "España",
        ("Inglaterra", "Francia", "Alemania"),
        "selecciones",
    ),
    SeedQuestion(
        "¿En qué país se jugó la Eurocopa 2024?",
        "Alemania",
        ("Francia", "España", "Italia"),
        "selecciones",
    ),
    SeedQuestion(
        "¿Quién ganó la Copa América 2024?",
        "Argentina",
        ("Colombia", "Brasil", "Uruguay"),
        "selecciones",
    ),
    SeedQuestion(
        "¿Quién ganó la Copa América 2021?",
        "Argentina",
        ("Brasil", "Colombia", "Perú"),
        "selecciones",
    ),
    SeedQuestion(
        "¿Cuál es el máximo goleador de la historia de los Mundiales?",
        "Miroslav Klose (16 goles)",
        ("Ronaldo Nazário (15 goles)", "Gerd Müller (14 goles)", "Just Fontaine (13 goles)"),
        "jugadores",
    ),
    SeedQuestion(
        "¿Cuántos Balones de Oro tiene Lionel Messi?",
        "8",
        ("7", "6", "9"),
        "jugadores",
    ),
    SeedQuestion(
        "¿Cuántos goles tiene Cristiano Ronaldo en Mundiales?",
        "8",
        ("7", "9", "6"),
        "jugadores",
    ),
    SeedQuestion(
        "¿Qué número usa Cristiano Ronaldo en Portugal?",
        "7",
        ("10", "9", "11"),
        "jugadores",
    ),
    SeedQuestion(
        "¿En qué posición juega Alphonso Davies?",
        "Lateral izquierdo",
        ("Extremo derecho", "Mediocampista central", "Delantero"),
        "jugadores",
    ),
    SeedQuestion(
        "¿A qué club pertenece Vinicius Junior?",
        "Real Madrid",
        ("Barcelona", "PSG", "Manchester City"),
        "jugadores",
    ),
    SeedQuestion(
        "¿Cuántos mundiales disputó Messi antes de ganar en 2022?",
        "4",
        ("3", "5", "2"),
        "jugadores",
    ),
    SeedQuestion(
        "¿Quién fue el Mejor Jugador Joven de la Eurocopa 2024?",
        "Lamine Yamal",
        ("Jude Bellingham", "Florian Wirtz", "Pedri"),
        "jugadores",
    ),
    SeedQuestion(
        "¿Con cuántos años ganó Lamine Yamal la Eurocopa 2024?",
        "16",
        ("17", "15", "18"),
        "jugadores",
    ),
    SeedQuestion(
        "¿Quién es el capitán de la selección de Inglaterra?",
        "Harry Kane",
        ("Jude Bellingham", "Jordan Pickford", "Declan Rice"),
        "jugadores",
    ),
    SeedQuestion(
        "¿Qué jugador ganó el Balón de Oro 2023?",
        "Lionel Messi",
        ("Erling Haaland", "Kylian Mbappé", "Vinicius Junior"),
        "jugadores",
    ),
    SeedQuestion(
        "¿Quién es el técnico de España?",
        "Luis de la Fuente",
        ("Luis Enrique", "Julen Lopetegui", "Pep Guardiola"),
        "tecnicos",
    ),
    SeedQuestion(
        "¿Quién es el técnico de Francia?",
        "Didier Deschamps",
        ("Zinedine Zidane", "Laurent Blanc", "Raymond Domenech"),
        "tecnicos",
    ),
    SeedQuestion(
        "¿Quién fue el técnico de México en el Mundial 2022?",
        'Gerardo "Tata" Martino',
        ("Juan Carlos Osorio", "Miguel Herrera", "Javier Aguirre"),
        "tecnicos",
    ),
    SeedQuestion(
        "¿Qué técnico dirige actualmente a Canadá?",
        "Jesse Marsch",
        ("John Herdman", "Octavio Zambrano", "Patrick Vieira"),
        "tecnicos",
    ),
)
