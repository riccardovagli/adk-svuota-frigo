import json
import math
from pathlib import Path


DISPENSA_PATH = Path(__file__).parent / "dispensa.json"


def leggi_dispensa() -> dict:
    """Legge gli ingredienti disponibili con quantità e unità di misura.

    Returns:
        Esito dell'operazione e contenuto della dispensa, oppure un errore.
    """
    try:
        dispensa = json.loads(
            DISPENSA_PATH.read_text(encoding="utf-8")
        )
    except (OSError, ValueError):
        return {
            "stato": "errore",
            "messaggio": "Non riesco a leggere il file della dispensa."
        }

    return {
        "stato": "ok",
        "ingredienti": dispensa
    }


def registra_consumo(consumi: dict[str, float]) -> dict:
    """Sottrae dalla dispensa le quantità effettivamente consumate.

    Da usare soltanto dopo che l'utente ha confermato gli ingredienti
    e le quantità utilizzati. Non chiamare per una semplice proposta
    di ricetta.

    Args:
        consumi: Mappa tra nomi esatti degli ingredienti e quantità
            consumate. Usa le unità indicate nella dispensa.
            Esempio: {"uova": 2, "zucchine": 150}.

    Returns:
        Esito e dispensa aggiornata, oppure un errore senza modifiche.
    """
    risultato = leggi_dispensa()

    if risultato["stato"] != "ok":
        return risultato

    dispensa = risultato["ingredienti"]

    if not consumi:
        return {
            "stato": "errore",
            "messaggio": "Non hai indicato ingredienti da aggiornare."
        }

    # Prima controlliamo TUTTI gli ingredienti.
    for ingrediente, quantita in consumi.items():
        if ingrediente not in dispensa:
            return {
                "stato": "errore",
                "messaggio": f"Ingrediente non presente: {ingrediente}."
            }

        if (
            isinstance(quantita, bool)
            or not isinstance(quantita, (int, float))
            or not math.isfinite(quantita)
            or quantita <= 0
        ):
            return {
                "stato": "errore",
                "messaggio": (
                    f"La quantità di {ingrediente} deve essere "
                    "un numero positivo e finito."
                )
            }

        scorta = dispensa[ingrediente]

        if scorta["unita"] in ("pezzi", "rametti"):
            if not float(quantita).is_integer():
                return {
                    "stato": "errore",
                    "messaggio": (
                        f"Per {ingrediente} indica un numero intero "
                        f"di {scorta['unita']}."
                    )
                }

        if quantita > scorta["quantita"]:
            return {
                "stato": "errore",
                "messaggio": (
                    f"Quantità insufficiente di {ingrediente}: "
                    f"disponibili {scorta['quantita']} "
                    f"{scorta['unita']}."
                )
            }

    # Aggiorniamo soltanto dopo aver superato tutti i controlli.
    for ingrediente, quantita in consumi.items():
        dispensa[ingrediente]["quantita"] -= quantita

    try:
        temporaneo = DISPENSA_PATH.with_suffix(".tmp")
        temporaneo.write_text(
            json.dumps(dispensa, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        temporaneo.replace(DISPENSA_PATH)
    except OSError:
        return {
            "stato": "errore",
            "messaggio": "Non sono riuscito a salvare la dispensa."
        }

    return {
        "stato": "ok",
        "messaggio": "Consumo registrato.",
        "ingredienti": dispensa
    }