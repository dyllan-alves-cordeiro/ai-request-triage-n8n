#!/usr/bin/env python3
"""Bounded Vértice IA triage evals; real mode reports actual provider token usage."""
import json, os, re, sys, time
from pathlib import Path
from urllib import request, error

ROOT=Path(__file__).resolve().parent.parent
DATA=json.loads((Path(__file__).parent/'eval-dataset.json').read_text())
KB=json.loads((ROOT/'synthetic-kb.json').read_text())
ALLOWED={'QUALIFICATION','SERVICE_INFO','ACTIVE_CUSTOMER_TICKET','BILLING_CONTRACT','OUT_OF_SCOPE'}

def retrieve(item):
    intent=item['intent']; text=item['inquiry'].lower()
    if intent=='BILLING_CONTRACT': wanted='billing_or_contract'
    elif intent=='QUALIFICATION': wanted='qualification'
    elif intent=='ACTIVE_CUSTOMER_TICKET':
        wanted='active_customer_ticket'
        plan={'starter':'essencial','pro':'profissional','enterprise':'empresarial'}.get(item['plan'])
        if not plan: return []
        return [x for x in KB if x['intent']==wanted and plan in x['title'].lower()]
    elif intent=='SERVICE_INFO': wanted='service_or_price'
    else: return []
    found=[x for x in KB if x['intent']==wanted]
    if intent=='SERVICE_INFO' and any(w in text for w in ('preço','preco','faixa','investimento','custo')):
        return [x for x in found if x['kind']=='price_range'] or found[:1]
    if intent=='SERVICE_INFO' and 'integr' in text:
        return [x for x in found if x['id']=='VTX-CAT-02'] or found[:1]
    return found[:2]

def simulated(item,sources):
    intent=item['intent']; src=sources[0] if sources else None
    return {'classification':item['expected_classification'],'confidence':0.92 if src else 0.9,
      'summary':'Triagem determinística simulada para '+item['category'],
      'proposed_response':src['content'] if src else 'Sem fonte verificada; encaminhar para análise humana.',
      'source_ids':[src['id']] if src else [], 'requires_escalation':item['requires_escalation'],
      'escalation_reason':'HUMAN_REVIEW' if item['requires_escalation'] else None}

def call_openai(item,sources,key,model):
    system=(ROOT/'prompt.txt').read_text()
    prompt=system.replace('{{inquiry}}',item['inquiry']).replace('{{sources}}',json.dumps(sources,ensure_ascii=False)).replace('{{customer}}',json.dumps({'plan':item['plan']},ensure_ascii=False))
    payload={'model':model,'messages':[{'role':'system','content':'Siga as regras do prompt e retorne somente JSON válido.'},{'role':'user','content':prompt}],
      'temperature':0.1,'max_tokens':400,'response_format':{'type':'json_object'}}
    req=request.Request('https://api.openai.com/v1/chat/completions',data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+key,'Content-Type':'application/json'})
    with request.urlopen(req,timeout=15) as res: body=json.loads(res.read())
    out=json.loads(body['choices'][0]['message']['content']); usage=body.get('usage',{})
    return out, int(usage.get('total_tokens',0))

def main():
    mode=os.getenv('EVAL_MODE','simulated').lower(); key=os.getenv('OPENAI_API_KEY',''); model=os.getenv('OPENAI_MODEL','gpt-4o-mini')
    if mode not in ('simulated','real'): raise SystemExit('EVAL_MODE must be simulated or real')
    if mode=='real' and not key: raise SystemExit('real eval requested but OPENAI_API_KEY is unavailable')
    print(f'EVAL MODE: {"OPENAI REAL" if mode=="real" else "SIMULATED"} | model={model if mode=="real" else "mock-v1"} | cases={len(DATA)}')
    total_tokens=0; passed=0; deadline=time.monotonic()+180
    print('| ID | Intent | Expected | Actual | Source | Escalation | Result |')
    print('|---|---|---|---|---|---:|---|')
    for item in DATA:
        sources=retrieve(item)
        try:
            if mode=='real':
                if time.monotonic()>deadline: raise SystemExit('hard stop: 180 second real-eval deadline reached')
                out,tokens=call_openai(item,sources,key,model); total_tokens+=tokens
                if total_tokens>30000: raise SystemExit('hard stop: real eval exceeded 30000 tokens; no further calls made')
            else: out=simulated(item,sources)
        except Exception as exc:
            print(f"provider error at {item['id']}: {type(exc).__name__}",file=sys.stderr); raise SystemExit(2)
        srcids=out.get('source_ids',[]); valid_sources={x['id'] for x in sources}
        billing_guard=item['intent']=='BILLING_CONTRACT' and out.get('classification')=='BILLING_CONTRACT' and out.get('requires_escalation') is True
        ok=(out.get('classification') in ALLOWED and out.get('classification')==item['expected_classification'] and out.get('requires_escalation')==item['requires_escalation'] and all(x in valid_sources for x in srcids) and (item['expected_source'] is None or item['expected_source'] in srcids) and (item['intent']!='BILLING_CONTRACT' or billing_guard))
        passed+=bool(ok)
        print(f"| {item['id']} | {item['intent']} | {item['expected_classification']} | {out.get('classification')} | {','.join(srcids) or 'none'} | {out.get('requires_escalation')} | {'PASS' if ok else 'FAIL'} |")
    print(f'RESULT: {passed}/{len(DATA)}')
    if mode=='real': print(f'OPENAI_TOTAL_TOKENS: {total_tokens}')
    if mode=='real' and total_tokens>30000: raise SystemExit('hard stop: real eval exceeded 30000 tokens')
    if passed!=len(DATA): raise SystemExit(1)
if __name__=='__main__': main()
