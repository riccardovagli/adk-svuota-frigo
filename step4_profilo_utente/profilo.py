from google.adk.tools import ToolContext


def leggi_profilo(tool_context: ToolContext) -> dict:
    """Legge il nome e l'alimentazione abituale dell'utente."""
    return {
        "stato": "ok",
        "profilo": {
            "nome_utente": tool_context.state.get(
                "user:nome_utente"
            ),
            "alimentazione": tool_context.state.get(
                "user:alimentazione"
            ),
        },
    }


def aggiorna_profilo(
    tool_context: ToolContext,
    nome_utente: str = "",
    alimentazione: str = "",
) -> dict:
    """Registra informazioni personali dichiarate dall'utente.

    Non usare per preferenze limitate alla cena corrente.

    Args:
        nome_utente: Nome dichiarato dall'utente.
            Ometti o usa una stringa vuota per non modificarlo.
        alimentazione: Preferenza abituale: "vegetariana"
            oppure "nessuna". Ometti o usa una stringa vuota
            per non modificarla.
    """
    if not isinstance(nome_utente, str):
        return {
            "stato": "errore",
            "messaggio": "Il nome deve essere una stringa.",
        }

    if not isinstance(alimentazione, str):
        return {
            "stato": "errore",
            "messaggio": "L'alimentazione deve essere una stringa.",
        }

    nome_utente = nome_utente.strip()
    alimentazione = alimentazione.strip().lower()

    if alimentazione not in ("", "vegetariana", "nessuna"):
        return {
            "stato": "errore",
            "messaggio": (
                "Le opzioni previste sono "
                "'vegetariana' e 'nessuna'."
            ),
        }

    # Aggiorniamo lo stato solo dopo tutti i controlli.
    if nome_utente:
        tool_context.state["user:nome_utente"] = nome_utente

    if alimentazione:
        tool_context.state["user:alimentazione"] = alimentazione

    return leggi_profilo(tool_context)