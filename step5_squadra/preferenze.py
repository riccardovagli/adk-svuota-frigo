from google.adk.tools import ToolContext


def leggi_preferenze(tool_context: ToolContext) -> dict:
    """Legge le preferenze effettive della cena corrente.

    L'alimentazione della cena, quando presente, prevale
    sulla preferenza abituale del profilo.
    """
    alimentazione_cena = tool_context.state.get(
        "alimentazione"
    )
    alimentazione_abituale = tool_context.state.get(
        "user:alimentazione"
    )

    if alimentazione_cena is not None:
        alimentazione = alimentazione_cena
        origine = "cena"
    elif alimentazione_abituale is not None:
        alimentazione = alimentazione_abituale
        origine = "profilo"
    else:
        alimentazione = None
        origine = "non indicata"

    return {
        "stato": "ok",
        "preferenze": {
            "commensali": tool_context.state.get("commensali"),
            "alimentazione": alimentazione,
            "origine_alimentazione": origine,
            "tempo_minuti": tool_context.state.get(
                "tempo_minuti", 15
            ),
        },
    }


def aggiorna_preferenze(
    tool_context: ToolContext,
    commensali: int = 0,
    alimentazione: str = "",
    tempo_minuti: int = 0,
) -> dict:
    """Aggiorna soltanto i dati della cena corrente.

    Args:
        commensali: Numero totale di persone.
            Ometti o usa 0 per non modificarlo.
        alimentazione: "vegetariana" oppure "nessuna",
            valide solo per questa cena.
            Ometti o usa "" per non modificarla.
            Usa "abituale" per tornare alla preferenza
            del profilo, disattivando l'eccezione della cena.
        tempo_minuti: Minuti per preparazione e cottura.
            Ometti o usa 0 per non modificarli.
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
                "Usa 0 solo per non modificarli."
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
                "Usa 0 solo per non modificarlo."
            ),
        }

    if alimentazione not in (
        "", "vegetariana", "nessuna", "abituale"
    ):
        return {
            "stato": "errore",
            "messaggio": (
                "Usa 'vegetariana', 'nessuna' o 'abituale'."
            ),
        }

    # Nessuna modifica viene applicata prima dei controlli.
    if commensali:
        tool_context.state["commensali"] = commensali

    if tempo_minuti:
        tool_context.state["tempo_minuti"] = tempo_minuti

    if alimentazione == "abituale":
        tool_context.state["alimentazione"] = None
    elif alimentazione:
        tool_context.state["alimentazione"] = alimentazione

    return leggi_preferenze(tool_context)