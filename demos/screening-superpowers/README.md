# Screening Superpowers Dashboard

A static artifact browser for the Screening Superpowers fixture. After the fixture runs, open the dashboard locally to see how an agent or scientist would review consensus rankings, failure rows, method summaries, and candidate dossiers.

## Hand A Mission To An Agent

```text
Use the BioSymphony Structure Factory skill. Run the screening-superpowers fixture, open the demos/screening-superpowers/ dashboard, and walk through the consensus ranking, failure report, method summary, and candidate dossiers. Explain how this same dashboard shape applies to a real provider-backed screening campaign.
```

## Run It Yourself

Generate fixture artifacts:

```bash
make screening-check
```

Serve the repo root so the browser can fetch `.runtime/screening-superpowers-fixture/`:

```bash
python3 -m http.server 8765
```

Open:

```text
http://localhost:8765/demos/screening-superpowers/
```

The page also supports loading a local `.runtime/screening-superpowers-fixture` folder through the file picker, useful when opening `index.html` directly.

## Validation

The dashboard is static: no provider calls, downloads, build step, or external JavaScript dependencies. The companion parser validates the same artifact set from the command line:

```bash
python3 scripts/structure_factory/screening_dashboard.py \
  --artifact-root .runtime/screening-superpowers-fixture \
  --json
```

Fixture scores are `fixture_or_demo` evidence intended for schema, ranking, and dossier-promotion review. Real screening hits come from provider-backed runs and stay at `computational_candidate` until independent validation arrives.
