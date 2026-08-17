---
name: create-module
description: Create a research-use just-dna genetics annotation module from papers, attached supplements, variant lists, or a genomics topic. Use when evidence must be researched, converted into module_spec.yaml plus CSV tables, validated, and compiled.
---

# Create a just-dna module

Build an evidence-backed module without turning uncertain research into clinical advice. Use the
bundled `just-dna-agents-mcp` compiler tools and BioContext KB research tools; treat the runtime
schema and validator as the final source of truth.

## Workflow

1. Define the requested topic, source material, and output directory. If the user names a paper or
   supplement that is not available, obtain it or ask for the missing attachment before extracting
   claims.
2. Triage the evidence. Reviews can identify original studies but cannot replace them. Route a PGS
   Catalog scoring request to `just-prs`; do not translate a polygenic score into a handful of SNP
   claims.
3. Call `get_spec_format` before authoring. Follow the returned field definitions instead of a
   remembered schema.
4. Research each candidate variant and study. Verify GRCh38 forward-strand alleles with Ensembl and
   confirm that every PMID resolves to the intended paper in Europe PMC. Never invent or infer a
   citation.
5. For broad or high-stakes requests, perform two or three independent evidence passes, in parallel
   when delegated agents are available and sequentially otherwise. Reconcile conflicts before
   writing rows.
6. Write `module_spec.yaml`, `variants.csv`, and `studies.csv` in the chosen spec directory. Include
   the neutral reference genotype required for SNP modules. Represent missing evidence as unknown,
   not as a negative finding.
7. Call `validate_spec`. Fix every validation error and re-run validation until it succeeds.
8. Call `compile_module` only after validation passes. Report the spec directory, compiled output,
   validation result, sources used, exclusions, and unresolved limitations.

## Evidence rules

- Research and education only; do not diagnose, prescribe, or make deterministic predictions.
- Prefer original studies, validated guidelines, and attached supplementary tables over summaries.
- A database match is supporting context, not proof that a paper made the claimed association.
- Preserve effect direction, population, phenotype, and uncertainty from the source.
- Drop a row when its allele orientation, result, or source cannot be supported.
- Do not claim completion merely because files were written; validation and compilation are required.

## Completion report

State clearly whether validation passed, whether compilation succeeded, where artifacts were written,
which sources support the module, and which candidates were excluded or remain uncertain.
