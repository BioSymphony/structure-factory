# Support

Use public GitHub issues only for public-safe bugs, docs, examples, and feature requests.

Do not post:

- credentials, tokens, signed URLs, provider IDs, billing records, or logs
- private paths, private tracker URLs, or internal run notes
- private structures, unpublished sequences, patient data, generated structures, raw maps, raw cryo-EM movies, or model weights

For vulnerabilities or accidental private-data exposure, use GitHub Private vulnerability reporting.

For local validation, include only public-safe output from:

```bash
bsf harness-check .
bsf audit .
make release-check
```
