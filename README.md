# BufferPesa — Kenya Commercial Scorecard

Dash/Plotly dashboard built from the verified vet-list PDF and invoice-level data.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Open http://127.0.0.1:8050 in your browser. Leave the terminal running — closing it stops the server.

## What changed from v1

- **Regions corrected**: "Daniel" and "Harold" are KAM (Key Account Manager) names, not regions.
  Real regions are Kajiado, Kiambu, Voi, Lake Basin, Nairobi.
- **"Wundanyi"** is a sub-county within Voi, not its own region.
- **Pipeline count is 47** (verified from the vet-list PDF), not the earlier 46 estimate.
- **Invoices Created vs Funded are now separate funnels**:
  - *Invoices Created* (28 invoices, 48,465 KSH, 26 farmers across 7 vets) — vets using
    BufferPesa as a tracking tool; not all of these were sold/factored.
  - *Invoices Funded* (2 invoices, 700 + 500 = 1,200 KSH total) — actually financed by BufferPesa.
- Business type categories are grouped from messy free-text organization names
  (e.g. "VPP", "Private Vpp", "Private-BVM" → "Private Practice / VPP"). Revisit the
  `classify_org()` function in app.py if you want finer-grained categories.

## Known open items

- Business-type grouping is a judgment call — adjust `classify_org()` if categories don't match your taxonomy.
- Full vet pipeline table is sortable/filterable in the browser (click column headers, type in the filter row).
