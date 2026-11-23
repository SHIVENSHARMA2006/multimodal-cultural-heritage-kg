import sys
import os
sys.path.insert(0, ".")
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

from eval.evaluate import HeritageEvaluator
import csv

ev = HeritageEvaluator()
questions = list(csv.DictReader(open('eval/gold_qa_set.csv', encoding='utf-8-sig')))

for q in questions:
    q_trans = ev.translator.process_query(q['question'])
    ent = q_trans.get('primary_entity')
    if ent:
        ctx = ev.retriever.retrieve_context(ent, relation_hint=q_trans.get('detected_relation'))
        ans = ev.generator.generate_answer(q['question'], ctx, detected_relation=q_trans.get('detected_relation'))
    else:
        ctx = {'entity': None, 'assignments': []}
        ans = ev.generator.generate_answer(q['question'], ctx)
    if ans['behavior'] != q['expected_behavior']:
        ent_name = ent.canonical_name if ent else "None"
        rel_name = q_trans.get('detected_relation')
        print(f"{q['qa_id']} EXP: {q['expected_behavior']} ACT: {ans['behavior']} Q: {q['question']} :: Ent: {ent_name} :: Rel: {rel_name}")
