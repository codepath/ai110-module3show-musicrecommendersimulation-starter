# assets

Rendered system-architecture images live here.

The **source of truth** is [`diagrams/architecture.mmd`](../diagrams/architecture.mmd)
(Mermaid). Regenerate the PNG from it with:

```bash
npx -y @mermaid-js/mermaid-cli -i diagrams/architecture.mmd -o assets/architecture.png
```

or paste the `.mmd` contents into <https://mermaid.live> and export a PNG here.
