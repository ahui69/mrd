from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
import typing as T, os, time
import monolit as M

# używa tego samego auth co monolit (nagłówek Authorization: Bearer ...)
AUTH_TOKEN = os.getenv("AUTH_TOKEN") or os.getenv("AUTH") or "changeme"
def _auth(req: Request):
    tok = (req.headers.get("Authorization","") or "").replace("Bearer ","").strip()
    if not tok or tok != AUTH_TOKEN:
        raise HTTPException(401, "unauthorized")

writer_router = APIRouter(prefix="/api/write")

# ---------- util ----------
def _llm(messages: T.List[T.Dict[str,str]], timeout_s: int = 60) -> str:
    if not hasattr(M, "call_llm"):
        raise HTTPException(500, "call_llm() not available")
    out = M.call_llm(messages, timeout_s=timeout_s)
    return (out.get("text") if isinstance(out, dict) else out) or ""

async def _research(query: str, topk: int = 8, deep: bool = False):
    ctx, cites = "", []
    if hasattr(M, "autonauka") and query:
        try:
            r = await M.autonauka(query, topk=topk, deep_research=deep)
            ctx = (r or {}).get("context","") or ""
            cites = (r or {}).get("sources",[]) or []
        except:  # niech content generuje się nawet gdy research padnie
            ctx, cites = "", []
    return ctx, cites

def _save_ltm(text: str, tags: str = "", conf: float = 0.7):
    if text and hasattr(M, "ltm_add"):
        try: M.ltm_add(text, tags=tags, conf=conf)
        except: pass

# ---------- modele ----------
class CreativeBody(BaseModel):
    topic: str
    language: str = "pl"
    tone: str = "neutralny"
    format: str = "article"   # article|post|ad|faq|guide
    min_words: int = 120
    max_words: int = 220
    seo_keywords: T.List[str] = []
    use_research: bool = True
    save_to_ltm: bool = True
    tags: str = "writer,creative"

class RewriteBody(BaseModel):
    text: str
    language: str = "pl"
    tone: str = "neutralny"
    keep_length: bool = True
    remove_redundancy: bool = True
    improve_style: bool = True
    save_to_ltm: bool = False
    tags: str = "writer,rewrite"

class SEOBody(BaseModel):
    topic: str
    language: str = "pl"
    tone: str = "profesjonalny"
    depth: str = "longform"     # short|standard|longform
    include_outline: bool = True
    include_meta: bool = True
    include_faq: bool = True
    seo_keywords: T.List[str] = []
    use_research: bool = True
    save_to_ltm: bool = True
    tags: str = "writer,seo"

class SocialBody(BaseModel):
    goal: str                  # teaser / launch / promo / info
    platform: str = "ig"       # ig|tt|fb|li|x
    tone: str = "conversational"
    variants: int = 3
    language: str = "pl"
    hashtags: T.List[str] = []
    save_to_ltm: bool = False
    tags: str = "writer,social"

class BatchBody(BaseModel):
    items: T.List[CreativeBody]

# ---------- prompts ----------
SYS_WRITER = """Jesteś profesjonalnym polskim copywriterem i redaktorem.
- Pisz precyzyjnie, naturalnym językiem.
- Unikaj water, powtórzeń, frazesów.
- Gdy są słowa kluczowe SEO, wpleć je naturalnie.
- Jeśli dostaniesz KONTEKST RESEARCH, traktuj go jako fakty do wykorzystania i zacytowania.
- Zawsze dbaj o klarowną strukturę i poprawną polszczyznę.
"""

def _compose_research_block(ctx: str, cites: T.List[dict]) -> str:
    if not ctx and not cites: return ""
    lines = ["\n[RESEARCH CONTEXT]\n", ctx.strip()]
    if cites:
        lines.append("\n[ŹRÓDŁA]")
        for s in cites[:12]:
            t = s.get("title") or s.get("url") or ""
            u = s.get("url") or ""
            lines.append(f"- {t} — {u}")
    return "\n".join(lines).strip()

# ---------- endpoints ----------
@writer_router.post("/creative")
async def write_creative(body: CreativeBody, _=Depends(_auth)):
    ctx, cites = await _research(body.topic, topk=8, deep=body.use_research)
    sysmsg = SYS_WRITER
    research_block = _compose_research_block(ctx, cites)
    kw = ", ".join(body.seo_keywords) if body.seo_keywords else ""
    msg = f"""Napisz treść w języku {body.language}.
Format: {body.format}. Ton: {body.tone}.
Długość docelowa: {body.min_words}-{body.max_words} słów.
Temat: {body.topic}.
Słowa kluczowe (opcjonalnie): {kw or 'brak'}.
Wymagania:
- lead 1–2 zdania; logiczne akapity; zakończenie z wnioskiem.
- zero plagiatu; zero halucynacji.
- jeśli jest blok RESEARCH, cytuj najważniejsze fakty w tekście.
{research_block}
"""
    out = _llm([{"role":"system","content":sysmsg},
                {"role":"user","content":msg}])
    if body.save_to_ltm: _save_ltm(out, tags=body.tags)
    return {"ok": True, "text": out, "sources": cites, "meta": {
        "topic": body.topic, "format": body.format, "tone": body.tone
    }}

@writer_router.post("/rewrite")
async def rewrite_text(body: RewriteBody, _=Depends(_auth)):
    sysmsg = SYS_WRITER
    msg = f"""Przepisz poniższy tekst w języku {body.language}, zachowując sens.
Styl: {body.tone}. {"Utrzymaj długość." if body.keep_length else "Możesz skrócić do bardziej zwartej formy."}
{"Usuń powtórzenia, tautologie, wodolejstwo." if body.remove_redundancy else ""}
{"Popraw styl, rytm zdań, interpunkcję." if body.improve_style else ""}
Tekst:
\"\"\"{body.text.strip()}\"\"\""""
    out = _llm([{"role":"system","content":sysmsg},
                {"role":"user","content":msg}])
    if body.save_to_ltm: _save_ltm(out, tags=body.tags)
    return {"ok": True, "text": out}

@writer_router.post("/seo")
async def write_seo(body: SEOBody, _=Depends(_auth)):
    ctx, cites = await _research(body.topic, topk=10, deep=body.use_research)
    sysmsg = SYS_WRITER
    research_block = _compose_research_block(ctx, cites)
    kw = ", ".join(body.seo_keywords) if body.seo_keywords else ""
    length = {"short":"~600-900","standard":"~1200-1800","longform":"~2000-3000"}.get(body.depth,"~1500")
    msg = f"""Przygotuj SEO-artykuł w języku {body.language} (długość {length} słów).
Ton: {body.tone}. Temat: {body.topic}.
Słowa kluczowe: {kw or 'dobierz sam naturalne warianty'}.
Wymagania:
- nagłówek H1, logiczne H2/H3; krótkie akapity; listy tam gdzie sensowne.
- jeśli dostępny RESEARCH, wpleć fakty i cytuj źródła.
- unikaj keyword-stuffingu; pisz naturalnie dla człowieka.
{"Dodaj konspekt sekcji (outline), meta title + meta description, oraz blok FAQ (3-6 pytań i odpowiedzi)." if body.include_outline or body.include_meta or body.include_faq else ""}
{research_block}
"""
    out = _llm([{"role":"system","content":sysmsg},
                {"role":"user","content":msg}], timeout_s=120)
    if body.save_to_ltm: _save_ltm(out, tags=body.tags)
    return {"ok": True, "text": out, "sources": cites}

@writer_router.post("/social")
async def social_post(body: SocialBody, _=Depends(_auth)):
    sysmsg = SYS_WRITER
    base = f"""Przygotuj {body.variants} wariant(y) krótkiego posta na platformę {body.platform}
w języku {body.language}, ton {body.tone}. Cel: {body.goal}.
Każdy wariant maks 280 znaków (dla bezpieczeństwa).
Hashtagi: {", ".join(body.hashtags) if body.hashtags else "dobierz rozsądnie lub pomiń"}.
Zwróć listę wypunktowaną, jeden wariant = jedna pozycja."""
    out = _llm([{"role":"system","content":sysmsg},
                {"role":"user","content":base}])
    if body.save_to_ltm: _save_ltm(out, tags=body.tags)
    return {"ok": True, "text": out}

@writer_router.post("/batch")
async def write_batch(body: BatchBody, _=Depends(_auth)):
    results = []
    for item in body.items:
        ctx, cites = await _research(item.topic, topk=8, deep=item.use_research)
        research_block = _compose_research_block(ctx, cites)
        kw = ", ".join(item.seo_keywords) if item.seo_keywords else ""
        msg = f"""Napisz treść w języku {item.language}.
Format: {item.format}. Ton: {item.tone}.
Długość: {item.min_words}-{item.max_words} słów.
Temat: {item.topic}. Słowa kluczowe: {kw or 'brak'}.
{research_block}
"""
        text = _llm([{"role":"system","content":SYS_WRITER},
                     {"role":"user","content":msg}])
        if item.save_to_ltm: _save_ltm(text, tags=item.tags)
        results.append({"topic": item.topic, "text": text, "sources": cites})
    return {"ok": True, "items": results}
