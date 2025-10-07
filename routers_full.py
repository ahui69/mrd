#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import annotations
import os, time, typing as T
from fastapi import APIRouter, Request, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel
import typing as T, os, time
import monolit as M
from pydantic import BaseModel
import monolit as M

router = APIRouter(prefix="/api")

# --- auth ---
AUTH_TOKEN = os.getenv("AUTH_TOKEN") or os.getenv("AUTH") or "changeme"
def _auth(req: Request):
    tok = (req.headers.get("Authorization","") or "").replace("Bearer ","").strip()
    if not tok or tok != AUTH_TOKEN:
        raise HTTPException(401, "unauthorized")

# --- MODELE ---
class ChatMsg(BaseModel):
    role: str
    content: str

class ChatBody(BaseModel):
    user: T.Optional[str] = "user"
    messages: T.List[ChatMsg]
    options: T.Dict[str, T.Any] = {}

class AssistantBody(BaseModel):
    user: T.Optional[str] = "user"
    messages: T.List[ChatMsg]
    # preferencje i flage narzędzi
    allow_research: bool = True
    allow_news: bool = True
    allow_sports: bool = True
    save_memory: bool = True
    topk: int = 8

# --- HEALTH ---
@router.get("/health")
def health():
    return {"ok": True, "db_exists": True, "time": int(time.time())}

# --- LLM CHAT (STM+LTM+autonauka + call_llm) ---
@router.post("/llm/chat")
async def llm_chat(body: ChatBody, req: Request, _=Depends(_auth)):
    if not hasattr(M, "call_llm"):
        raise HTTPException(500, "call_llm() not available")
    msgs = [{"role": m.role, "content": m.content} for m in body.messages]
    last_user = next((m["content"] for m in reversed(msgs) if m["role"]=="user"), "")
    # STM
    stm_ctx = ""
    try:
        if hasattr(M, "stm_get_context"):
            stm = M.stm_get_context(limit=8) or []
            if stm: stm_ctx = "\n".join([f"{m['role']}: {m['content']}" for m in stm])
    except: pass
    # LTM
    ltm_ctx = ""
    try:
        if last_user and hasattr(M, "ltm_search_hybrid"):
            facts = M.ltm_search_hybrid(last_user, 8) or []
            if facts: ltm_ctx = "\n".join([f.get("text","") for f in facts if f.get("text")])
    except: pass
    # Autonauka (gdy brak LTM)
    auto_ctx = ""
    try:
        if not ltm_ctx.strip() and hasattr(M, "autonauka"):
            a = await M.autonauka(last_user, topk=8)
            auto_ctx = (a or {}).get("context","")
    except: pass
    # sklej system ctx
    sys_parts = []
    if stm_ctx:  sys_parts.append("STM:\n"+stm_ctx)
    if ltm_ctx:  sys_parts.append("LTM:\n"+ltm_ctx)
    if auto_ctx: sys_parts.append("RESEARCH:\n"+auto_ctx)
    llm_messages: T.List[T.Dict[str,str]] = []
    if sys_parts:
        llm_messages.append({"role":"system","content":"\n\n".join(sys_parts)})
    llm_messages.extend(msgs)
    out = M.call_llm(llm_messages)
    text = out.get("text") if isinstance(out, dict) else out
    return {"ok": True, "answer": text}

# --- RESEARCH ---
@router.get("/research/sources")
async def research_sources(q: str, topk: int = 8, deep: bool = False, _=Depends(_auth)):
    if not hasattr(M, "autonauka"):
        raise HTTPException(500, "autonauka() not available")
    data = await M.autonauka(q, topk=topk, deep_research=deep)
    return {"ok": True, **(data or {})}

@router.get("/search/answer")
def search_answer(q: str, deep: bool = False, _=Depends(_auth)):
    if not hasattr(M, "answer_with_sources"):
        raise HTTPException(500, "answer_with_sources() not available")
    return {"ok": True, **M.answer_with_sources(q, deep_research=deep)}

# --- LTM ---
@router.post("/ltm/add")
def ltm_add_api(body: T.Dict[str, T.Any], _=Depends(_auth)):
    if not hasattr(M, "ltm_add"):
        raise HTTPException(500, "ltm_add() not available")
    M.ltm_add(body.get("text",""), tags=body.get("tags",""), conf=float(body.get("conf",0.7)))
    return {"ok": True}

@router.get("/ltm/search")
def ltm_search(q: str, limit: int = 5, _=Depends(_auth)):
    if not hasattr(M, "ltm_search_hybrid"):
        raise HTTPException(500, "ltm_search_hybrid() not available")
    return {"ok": True, "items": M.ltm_search_hybrid(q, limit)}

@router.post("/ltm/delete")
def ltm_delete(body: T.Dict[str, T.Any], _=Depends(_auth)):
    if not hasattr(M, "ltm_delete"):
        raise HTTPException(500, "ltm_delete() not available")
    return {"ok": True, **M.ltm_delete(body.get("id",""))}

@router.post("/ltm/reindex")
def ltm_reindex(_=Depends(_auth)):
    if not hasattr(M, "ltm_reindex"):
        raise HTTPException(500, "ltm_reindex() not available")
    return {"ok": True, **M.ltm_reindex()}

# --- MEMORY (STM) ---
@router.post("/memory/add")
def memory_add(body: T.Dict[str,T.Any], _=Depends(_auth)):
    if not hasattr(M, "stm_add"):
        raise HTTPException(500, "stm_add() not available")
    M.stm_add(body.get("role","user"), body.get("content",""))
    return {"ok": True}

@router.get("/memory/context")
def memory_context(limit: int = 20, _=Depends(_auth)):
    if not hasattr(M, "stm_get_context"):
        raise HTTPException(500, "stm_get_context() not available")
    return {"ok": True, "items": M.stm_get_context(limit=limit)}

# --- NEWS ---
@router.get("/news/duck")
async def news_duck(q: str, limit: int = 10, _=Depends(_auth)):
    if not hasattr(M, "duck_news"):
        raise HTTPException(500, "duck_news() not available")
    return {"ok": True, **(await M.duck_news(q, limit))}

# --- SPORTS ---
@router.get("/sports/scores")
def sports_scores(league: str = "nba", _=Depends(_auth)):
    if not hasattr(M, "sports_scores"):
        raise HTTPException(500, "sports_scores() not available")
    return {"ok": True, **M.sports_scores(league)}

# --- SYSTEM ---
@router.get("/system/stats")
def system_stats(_=Depends(_auth)):
    if hasattr(M, "system_stats"):
        return {"ok": True, **M.system_stats()}
    return {"ok": True, "uptime_s": int(time.time())}

@router.post("/system/optimize")
def system_optimize(_=Depends(_auth)):
    if not hasattr(M, "optimize_db"):
        raise HTTPException(500, "optimize_db() not available")
    return {"ok": True, **M.optimize_db()}

@router.post("/system/backup")
def system_backup(_=Depends(_auth)):
    if not hasattr(M, "backup_all_data"):
        raise HTTPException(500, "backup_all_data() not available")
    return {"ok": True, **M.backup_all_data()}

# --- SEMANTIC ---
@router.post("/semantic/analyze")
def semantic_analyze(body: T.Dict[str,T.Any], _=Depends(_auth)):
    if not hasattr(M, "semantic_analyze"):
        raise HTTPException(500, "semantic_analyze() not available")
    return {"ok": True, **M.semantic_analyze(body.get("text",""))}

@router.post("/semantic/analyze_conversation")
def semantic_analyze_conv(body: T.Dict[str,T.Any], _=Depends(_auth)):
    if not hasattr(M, "semantic_analyze_conversation"):
        raise HTTPException(500, "semantic_analyze_conversation() not available")
    return {"ok": True, **M.semantic_analyze_conversation(body.get("messages",[]))}

@router.post("/semantic/enhance_response")
def semantic_enhance(body: T.Dict[str,T.Any], _=Depends(_auth)):
    if not hasattr(M, "semantic_enhance_response"):
        raise HTTPException(500, "semantic_enhance_response() not available")
    return {"ok": True, **M.semantic_enhance_response(body.get("answer",""), body.get("context",""))}

# --- ASSISTANT: jeden endpoint do wszystkiego ---
@router.post("/assistant/chat")
async def assistant_chat(body: AssistantBody, _=Depends(_auth)):
    if not hasattr(M, "call_llm"):
        raise HTTPException(500, "call_llm() not available")

    # 1) wyciągnij ostatnią wiadomość użytkownika
    msgs = [{"role": m.role, "content": m.content} for m in body.messages]
    last_user = next((m["content"] for m in reversed(msgs) if m["role"] == "user"), "").strip()

    # 2) STM kontekst (krótkoterminowy)
    stm_ctx = ""
    if hasattr(M, "stm_get_context"):
        try:
            stm = M.stm_get_context(limit=8) or []
            if stm:
                stm_ctx = "\n".join([f"{m['role']}: {m['content']}" for m in stm])
        except:
            pass

    # 3) Wykrywanie zamiaru (intent)
    intent = "chat"
    if last_user:
        lu = last_user.lower()
        if body.allow_news and any(w in lu for w in ("news", "wiadomości", "aktualności", "co nowego")):
            intent = "news"
        elif body.allow_sports and any(w in lu for w in ("wyniki", "mecz", "mecze", "liga", "score")):
            intent = "sports"
        elif body.allow_research and any(w in lu for w in ("wyszukaj", "źródła", "research", "źródło", "źrodła")):
            intent = "research"

    # 4) Narzędzia wg intencji
    research_ctx, research_sources = "", []
    news_items, sports = [], {}

    if intent == "research" and hasattr(M, "autonauka") and last_user:
        try:
            r = await M.autonauka(last_user, topk=max(1, int(body.topk or 8)))
            research_ctx = (r or {}).get("context", "")
            research_sources = (r or {}).get("sources", []) or []
        except:
            pass

    if intent == "news" and hasattr(M, "duck_news") and last_user:
        try:
            n = await M.duck_news(last_user, limit=max(5, min(15, body.topk)))
            news_items = (n or {}).get("items", [])
        except:
            pass

    if intent == "sports" and hasattr(M, "sports_scores"):
        try:
            # heurystyka: wyciągnij ligę ze słów kluczowych
            league = "nba"
            for key in ("nba","nfl","nhl","mlb","epl","laliga","seriea","bundesliga"):
                if key in last_user.lower():
                    league = key
                    break
            sports = M.sports_scores(league)
        except:
            pass

    # 5) Zbuduj system prompt
    sys_parts = []
    if stm_ctx: sys_parts.append("STM:\n" + stm_ctx)
    if research_ctx: sys_parts.append("RESEARCH:\n" + research_ctx)
    if news_items:
        lines = [f"- {it.get('title','')} — {it.get('url','')}" for it in news_items[:body.topk]]
        sys_parts.append("NEWS:\n" + "\n".join(lines))
    if sports and sports.get("ok"):
        lines = []
        for g in sports.get("games", [])[:body.topk]:
            lines.append(f"{g['away']['abbr']} {g['away']['score']} : {g['home']['score']} {g['home']['abbr']} — {g['state']}")
        if lines:
            sys_parts.append("SPORTS:\n" + "\n".join(lines))

    llm_messages: T.List[T.Dict[str,str]] = []
    if sys_parts:
        llm_messages.append({"role": "system", "content": "\n\n".join(sys_parts)})
    llm_messages.extend(msgs)

    # 6) LLM odpowiedź
    out = M.call_llm(llm_messages)
    answer = out.get("text") if isinstance(out, dict) else out

    # 7) Memory update
    if body.save_memory:
        try:
            if hasattr(M, "stm_add") and last_user:
                M.stm_add("user", last_user)
            if hasattr(M, "stm_add") and answer:
                M.stm_add("assistant", answer)
        except:
            pass

    return {
        "ok": True,
        "answer": answer,
        "intent": intent,
        "sources": research_sources,
        "news": news_items,
        "sports": sports if sports else None,
    }

# --- FILES ---
MAX_UPLOAD_BYTES = int(os.getenv("MAX_UPLOAD_BYTES","20000000"))  # 20MB

@router.post("/files/upload")
async def files_upload(files: T.List[UploadFile] = File(...), _=Depends(_auth)):
    saved = []
    os.makedirs(M.UPLOADS_DIR, exist_ok=True)
    for f in files or []:
        try:
            name = (f.filename or "file").replace("..",".").replace("/","_")
            path = os.path.join(M.UPLOADS_DIR, name)
            buf = await f.read()
            if len(buf) > MAX_UPLOAD_BYTES:
                raise ValueError("file_too_large")
            with open(path, "wb") as out:
                out.write(buf)
            saved.append({
                "name": name,
                "size": os.path.getsize(path),
                "url": f"/uploads/{name}",
            })
        except Exception as e:
            saved.append({"name": f.filename, "error": str(e)})
    return {"ok": True, "files": saved}

# --- STT (Whisper via OpenAI-compatible API) ---
@router.post("/stt/transcribe")
async def stt_transcribe(audio: UploadFile = File(...), lang: str = "pl", _=Depends(_auth)):
    import httpx
    api = (M.LLM_BASE_URL or "").rstrip("/")
    key = M.LLM_API_KEY or os.getenv("LLM_API_KEY", "")
    if not api or not key:
        raise HTTPException(400, "LLM_BASE_URL or LLM_API_KEY missing")
    url = f"{api}/audio/transcriptions"
    data = {
        "model": (None, "whisper-large-v3"),
        "language": (None, lang),
        "response_format": (None, "json")
    }
    files = {"file": (audio.filename or "audio.webm", await audio.read(), audio.content_type or "audio/webm")}
    headers = {"Authorization": f"Bearer {key}"}
    async with httpx.AsyncClient(timeout=60.0) as c:
        try:
            r = await c.post(url, headers=headers, data=data, files=files)
            r.raise_for_status()
            j = r.json()
            text = j.get("text") or j.get("result") or ""
            return {"ok": True, "text": text}
        except Exception as e:
            return {"ok": False, "error": str(e)}
