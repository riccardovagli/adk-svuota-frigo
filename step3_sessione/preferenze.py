from google.adk.tools import ToolContext


def leggi_preferenze(tool_context: ToolContext) -> dict:
    """Legge le preferenze della cena nella sessione corrente.

    Returns:
        Numero di commensali, alimentazione e tempo disponibile.
        I dati non ancora dichiarati sono restituiti come null.
        Il tempo predefinito è 15 minuti.
    """
    return {
        "stato": "ok",
        "preferenze": {
            "commensali": tool_context.state.get("commensali"),
            "alimentazione": tool_context.state.get("alimentazione"),
            "tempo_minuti": tool_context.state.get("tempo_minuti", 15),
        },
    }


def aggiorna_preferenze(
    tool_context: ToolContext,
    commensali: int = 0,
    alimentazione: str = "",
    tempo_minuti: int = 0,
) -> dict:
    """Aggiorna soltanto le preferenze esplicitamente indicate.

    Usa questo strumento per decisioni certe dell'utente.
    Non trasformare ipotesi o possibilità in preferenze confermate.

    Args:
        commensali: Numero totale aggiornato di persone, non un incremento.
            Usa 0 oppure ometti il parametro per lasciare il dato invariato.
        alimentazione: "vegetariana" oppure "nessuna".
            "nessuna" significa nessuna preferenza alimentare dichiarata.
            Usa una stringa vuota oppure ometti il parametro
            per lasciare il dato invariato.
        tempo_minuti: Tempo totale disponibile per preparazione e cottura.
            Usa 0 oppure ometti il parametro per lasciare il dato invariato.

    Returns:
        Esito e preferenze aggiornate, oppure un errore senza modifiche.
    """
    if (
        isinstance(commensali, bool)
        or not isinstance(commensali, int)
        or commensali < 0
    ):
        return {
            "stato": "errore",
            "messaggio": (
                "I commensali devono essere un intero positivo. "
                "Usa 0 soltanto per lasciare il dato invariato."
            ),
        }

    if (
        isinstance(tempo_minuti, bool)
        or not isinstance(tempo_minuti, int)
        or tempo_minuti < 0
    ):
        return {
            "stato": "errore",
            "messaggio": (
                "Il tempo deve essere un intero positivo. "
                "Usa 0 soltanto per lasciare il dato invariato."
            ),
        }

    if alimentazione not in ("", "vegetariana", "nessuna"):
        return {
            "stato": "errore",
            "messaggio": (
                "Le opzioni previste sono 'vegetariana' e 'nessuna'."
            ),
        }

    # Tutti i controlli precedono le modifiche.
    if commensali != 0:
        tool_context.state["commensali"] = commensali

    if alimentazione != "":
        tool_context.state["alimentazione"] = alimentazione

    if tempo_minuti != 0:
        tool_context.state["tempo_minuti"] = tempo_minuti

    return leggi_preferenze(tool_context)