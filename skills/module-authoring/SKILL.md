---
name: genetics-module-authoring
description: Create or assess research-use genetic annotation modules from papers, variant lists, or genomics topics. Use for SNP associations, PGS manifests, and pharmacogenomics star-allele evidence.
---

# Genetics module authoring

Use the `just-dna-agents-mcp` tools to validate and compile module specs. Use
BioContext KB to research evidence, confirm Ensembl forward-strand GRCh38
alleles, and verify every PMID through EuropePMC.

## Route the request

- Unclear paper or topic: first assess whether it contains extractable variant evidence.
- Individual variant associations: use the `$create-module` workflow.
- PGS Catalog score selection: use `just-prs` rather than reducing a score to SNP claims.
- Star-allele pharmacogenomics: preserve the guideline's allele definitions and provenance.
- High-stakes SNP requests: perform independent research and review passes before authoring.
  Use delegated agents in parallel when available, or run the passes sequentially.

## Non-negotiable constraints

- Research use only; never provide clinical advice or deterministic predictions.
- Use GRCh38 coordinates only.
- Verify each ref/alt allele against Ensembl on the forward strand.
- Include a neutral reference genotype for SNP module variants.
- Use real, topic-matched PMIDs only.
- Call `get_spec_format` before authoring and `validate_spec` before completion.

Keep runtime schema validation as the final source of truth.
