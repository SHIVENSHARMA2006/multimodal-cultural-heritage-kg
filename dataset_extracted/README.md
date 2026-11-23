# Manipur (Meitei) Cultural-Heritage Seed Dataset

Seed dataset for a multimodal cultural-heritage knowledge graph pilot (Manipuri/Meitei).
Built 2026-10-24 from publicly available sources. Every row is traceable to a URL in `sources_registry.csv`.

## Files
| File | Rows | Purpose |
|---|---|---|
| `manipur_heritage_claims.csv` | 197 | Main dataset. One atomic, source-attributed claim per row (short paraphrases, not copied text). |
| `sources_registry.csv` | 73 | Every source: URL, publisher, type, reliability tier (A/B/C), retrieval date, caveats. |
| `divergence_cases.csv` | 23 | Gold set for the divergence detector: 19 real source disagreements + 4 agreement controls. |
| `gold_qa_set.csv` | 41 | Evaluation questions: single-fact, alias, cross-source, conflict, and unanswerable (hallucination probes). |
| `media_manifest.csv` | 13 | Pointers to real audio / image / manuscript / video sources (9 verified to exist, 4 with access unverified), with licence caveats. |
| `fetch_commons_images.py` | - | Run locally: downloads licence-checked Commons images + provenance manifest (logic tested offline; not run against the live API from the build sandbox). |

## Key columns (claims)
- `entity_id / entity_name / entity_aliases` - aliases cover real spelling variants (e.g. Garib Niwaz / Gharib Nawaz / Gareeb Nawaz / Pamheiba) for entity-linking tests.
- `entity_name_meitei_script` - only filled where the Meitei-script name appeared in a retrieved source (5 entities). Have a native speaker verify.
- `relation` - CIDOC-CRM-style property names (informal; map to real CRM properties in your schema).
- `evidence_modality` - text | audio_corpus_metadata | archive_catalogue_record | image_collection_pointer | video_pointer.
- `source_reliability_tier` - A = government / intergovernmental / academic publisher / dataset owner / national library; B = cited encyclopedia, scholarly paper, established media; C = tertiary (exam-prep, travel, simple-wikipedia). Tier-C is kept ONLY to document competing claims.
- `divergence_group_id` - links claims that disagree (D*) or agree (A*, negative controls). A claim carries one group id; group D04b also reuses claims tagged D04 (see `divergence_cases.csv`).
- `split` - assigned by ENTITY (train/dev/test), so no entity leaks across splits.

## Divergence grades
- `hard` - genuine factual/interpretive conflict -> system should surface all perspectives.
- `soft` - precision, counting-basis, or version differences -> report range / note, do not treat as a clash.
- `none` - sources agree (A01-A04) -> answer directly. D08a and D11b are deliberate *negative controls* (apparent conflicts that are not).

## Limitations - read before using
1. **Verification depth.** Claims were extracted from search-result excerpts of each source, not full-page reads. Treat as a research-grade seed; do a human verification pass before using as final gold labels (start with tier-C rows and every `D*` group).
2. **Text-heavy.** Images, audio and manuscript scans are NOT bundled - see `media_manifest.csv` for where to get them and `fetch_commons_images.py` for images. The multimodal claim of the project is only supported once media is acquired, with licences/consent checked. Heritage-relevant oral audio is the scarcest: best leads are the Imasi/Jalakeli oral-history project and the UNT CoRSAL Meitei recordings (1980s fieldwork).
3. **No oral testimony.** No community-recorded oral accounts exist in this set (Q39 tests that the system abstains). Real oral data needs consented collection with community partners.
4. **Not enough to train a model from scratch.** ~200 claims / 41 questions is suited to evaluation, few-shot/prompt design, adapter tuning of extraction prompts, and tuning the divergence threshold - not full model training. Scale via the sources in the registry.
5. **Source mix.** Many tier-B rows are Wikipedia-derived (CC BY-SA); two source URLs use mirror-style domains exactly as retrieved (S11, S18, S68) - verify before citing. S11 sits on a 'testing' subdomain and contains a likely error ('Kiyamba of Bengal'), kept deliberately as a divergence case (D07b).
6. **Sensitive topics.** Puya Meithaba and the 1891 war are contested/emotive; claims are attributed and neutral, and the dataset takes no position on which account is correct. Ongoing regional tensions make community review essential before any public release.
7. **Language.** All claims/questions are English. Meitei-language (Meitei Mayek) query versions should be produced and validated by native speakers (IndicTrans2 can draft).
8. **Licensing.** Claims are paraphrased facts; source texts remain under their own licences. Confirm reuse terms of AI4Bharat corpora (check each dataset card) and every Commons file before redistributing media.

## Suggested use
- Entity linking: test alias resolution (`entity_aliases`) and Meitei-script names.
- Extraction: feed source text -> compare extracted triples to `claim_value_normalized`.
- Divergence detector: run on `divergence_cases.csv` (hard vs soft vs none) and report precision/recall, especially false alarms on A* and D08a/D11b.
- RAG evaluation: `gold_qa_set.csv` with `expected_behavior` = answer | present_all_perspectives | abstain_not_in_kg.
