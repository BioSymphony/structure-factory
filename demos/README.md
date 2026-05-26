# Demos

Curated narratives and lightweight dashboards from completed Structure Factory campaigns. Read one of these to see what a finished mission looks like: target choice, lane structure, dossier shape, evidence mode, and the review surface an agent or scientist gets at the end.

Demo folders stay lightweight by design. Raw data, generated structure archives, provider logs, credentials, and model weights live in operator-controlled infrastructure outside the repo.

| Demo | Start Here | What You See | Evidence Mode | Local Entry |
| --- | --- | --- | --- | --- |
| `screening-superpowers` | Open `demos/screening-superpowers/index.html` after running the fixture | local dashboard shape for screening contracts and candidate dossiers | `public_synthetic_demo` | `make screening-check` |
| `t2r14-open-dossier` | Read `demos/t2r14-open-dossier/README.md` | open public-coordinate dossier packet shape | `public_demo` | `make demo-t2r14-check` |
| `poltheta-map-model-dossier` | Read `demos/poltheta-map-model-dossier/README.md` | public map/model dossier plan and prep checks | `public_demo` | `make demo-poltheta-prep-check` |
| `structure-jury-dual-dossier` | Read `demos/structure-jury-dual-dossier/README.md` | dual model-jury dossier packet shape | `public_demo` | `make demo-structure-jury-prep-check` |

Any provider launch requires a private/operator-gated packet outside public git.
