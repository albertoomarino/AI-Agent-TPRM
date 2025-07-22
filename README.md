# AI Agent for TPRM (Third-Party Risk Management)

## Overview

This project implements an AI-based monitoring agent for assessing the reliability of third-party ICT vendors over time. The system is designed to support the IORC (Integrated Operational Resilience Centre) in financial institutions, with features aligned to regulatory frameworks like DORA.

The agent collects financial data, derives behavioral indicators, and computes a dynamic Trust Score (0–10) for each supplier. It also visualizes trends and flags suppliers that become potentially risky during long-term contracts.

## Getting Started

1. **Create and activate a virtual environment (recommended)**

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Install dependencies

    ```bash
    pip install -r requirements.txt
    ```

3. Run the script

    ```bash
    python3 monitor.py
    ```

4. Check the `monitoring/` folder

    You'll find:

    - `CSV` files with daily metrics and trust scores
    - `PNG` plots of trust score trends

## Parametri considerati

### Dati ottenuti da Yahoo Finance

- **Open**: prezzo di apertura. È il prezzo al quale l'azione ha iniziato a essere scambiata all'inizio della giornata di Borsa (es. alle 09:30 in USA).
- **High**: prezzo massimo dell’intervallo. È il prezzo più alto a cui l'azione è stata venduta durante la giornata.
- **Low**: prezzo minimo dell’intervallo. È il prezzo più basso registrato durante la giornata.
- **Close**: prezzo di chiusura. È il prezzo finale dell'azione alla fine della giornata di Borsa (es. alle 16:00).
- **Volume**: volume di azioni scambiate. È il numero totale di azioni vendute e comprate in quel giorno.
- **Dividends**: dividendi distribuiti (se presenti). Alcune aziende pagano soldi agli azionisti ogni tanto. Se succede quel giorno, questo valore indica quanto (es. "Oggi Microsoft ha dato 0,50 $ per azione agli azionisti").
- **Stock Splits**: split azionari (se presenti). A volte un’azienda divide ogni azione in più pezzi (es. 1 diventa 2) per renderle più accessibili (es. "Ora ogni vecchia azione equivale a 2 nuove azioni, ognuna vale la metà").

### Calcoli aggiuntivi per costruire indicatori

- Calcolo 1: **Percent Change** (Variazione percentuale). `hist["Percent Change"] = hist["Close"].pct_change() * 100`. Misura quanto è cambiato il prezzo finale di oggi rispetto a ieri, in percentuale. Se il prezzo cambia troppo velocemente (es. +5% o -7%), può significare instabilità o notizie forti.

- Calcolo 2: **Close_MA_3** (Media mobile a 3 giorni). È la media dei prezzi di chiusura degli ultimi 3 giorni, aggiornata giorno per giorno. Serve a "lisciare" l'andamento: ci aiuta a capire la direzione generale, senza farci distrarre da piccole fluttuazioni.

- Calcolo 3: **Close_STD_3** (Volatilità). Misura quanto variano i prezzi negli ultimi 3 giorni. Un’azienda con alta volatilità è più rischiosa, perché il suo valore cambia rapidamente.

- Calcolo 4: **Volume_MA_3 + Volume_Spike** (Attività anomala). Calcola la media del volume degli ultimi 3 giorni. Verifica se oggi il volume è più del doppio di quella media. Un volume anomalo può significare che è successo qualcosa di grosso: notizie, vendite in massa, speculazioni...

- Calcolo 5: **Consecutive_Drops** (3 giorni di fila in calo). Conta se l’azienda ha chiuso in perdita per 3 giorni consecutivi. Un calo prolungato indica una tendenza negativa, e può segnalare una crisi o una perdita di fiducia del mercato.

- Calcolo finale: **Trust Score**. Parte da un punteggio massimo = 10. Poi toglie punti in base ai segnali di rischio visti sopra.

| Situazione                   | Penalità | Perché                    |
|------------------------------|----------|---------------------------|
| Cambiamento > ±1%            | -1       | Troppo instabile          |
| Volatilità > 3               | -2       | Oscilla troppo            |
| Volume anomalo               | -1       | Qualcosa di sospetto      |
| 3 giorni consecutivi in calo | -2       | Tendenza al peggioramento |

- Trust Score 8-10: Fornitore stabile e affidabile
- Trust Score 5-7: Da monitorare, segnali misti
- Trust Score 0-4: Rischio potenziale
