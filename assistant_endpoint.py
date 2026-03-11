#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
assistant_endpoint.py - All-in-one chat assistant endpoint
Ogarnnia wszystko automatycznie: STM, LTM, research, semantykę
"""

from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import os, time, json, asyncio

router = APIRouter(prefix="/api/chat")

# Auth
AUTH_TOKEN = os.getenv("AUTH_TOKEN") or os.getenv("AUTH") or "changeme"
def _auth(req: Request):
    tok = (req.headers.get("Authorization","") or "").replace("Bearer ","").strip()
    if not tok or tok != AUTH_TOKEN:
        raise HTTPException(401, "unauthorized")

# --- Modele ---
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    user_id: Optional[str] = "default"
    # Opcje
    use_memory: bool = True          # STM + LTM
    use_research: bool = True        # Autonauka/web research
    use_semantic: bool = True        # Analiza semantyczna
    save_to_memory: bool = True      # Zapisz do STM
    research_depth: str = "standard" # quick|standard|deep
    max_context_messages: int = 10   # Ile wiadomości z STM
    # Opcjonalne
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None

class ChatResponse(BaseModel):
    ok: bool
    answer: str
    sources: Optional[List[Dict]] = []
    context_used: Dict[str, Any] = {}
    metadata: Dict[str, Any] = {}

# --- Helper functions ---
def _get_stm_context(limit: int = 10):
    """Pobierz kontekst z pamięci krótkoterminowej"""
    try:
        import monolit as M
        if hasattr(M, "stm_get_context"):
            return M.stm_get_context(limit=limit) or []
    except:
        pass
    return []

def _get_ltm_context(query: str, limit: int = 8):
    """Pobierz kontekst z pamięci długoterminowej"""
    try:
        import monolit as M
        if hasattr(M, "ltm_search_hybrid"):
            return M.ltm_search_hybrid(query, limit) or []
    except:
        pass
    return []

async def _get_research_context(query: str, depth: str = "standard"):
    """Pobierz research/autonauka"""
    try:
        import monolit as M
        if hasattr(M, "autonauka"):
            topk = {"quick": 5, "standard": 8, "deep": 12}.get(depth, 8)
            deep = depth == "deep"
            res = await M.autonauka(query, topk=topk, deep_research=deep)
            return res or {}
    except:
        pass
    return {}

def _semantic_analyze(text: str):
    """Analiza semantyczna tekstu"""
    try:
        import monolit as M
        if hasattr(M, "semantic_analyze"):
            return M.semantic_analyze(text)
    except:
        pass
    return {}

def _save_to_stm(role: str, content: str):
    """Zapisz do pamięci krótkoterminowej"""
    try:
        import monolit as M
        if hasattr(M, "stm_add"):
            M.stm_add(role, content)
    except:
        pass

def _call_llm(messages: List[Dict], **kwargs):
    """Wywołaj LLM"""
    try:
        import monolit as M
        if hasattr(M, "call_llm"):
            return M.call_llm(messages, **kwargs)
    except Exception as e:
        raise HTTPException(500, f"LLM error: {str(e)}")

# --- Main endpoint ---
@router.post("/assistant", response_model=ChatResponse)
async def chat_assistant(body: ChatRequest, req: Request, _=Depends(_auth)):
    """
    🤖 ALL-IN-ONE CHAT ASSISTANT
    
    Automatycznie obsługuje:
    - 🧠 STM (Short-term memory) - ostatnie rozmowy
    - 💾 LTM (Long-term memory) - fakty z bazy wiedzy
    - 🔍 Research/Autonauka - wyszukiwanie w sieci gdy potrzeba
    - 🎯 Analiza semantyczna - zrozumienie kontekstu
    - 💬 Zapis do pamięci - automatyczne uczenie się
    
    Użycie:
    ```
    POST /api/chat/assistant
    {
        "messages": [
            {"role": "user", "content": "Cześć, jak się masz?"}
        ],
        "use_memory": true,
        "use_research": true,
        "save_to_memory": true
    }
    ```
    """
    
    # Rate limiting
    try:
        from middleware import rate_limiter
        user_id = body.user_id or req.client.host
        allowed, retry_after = rate_limiter.check_limit(user_id, "llm")
        if not allowed:
            raise HTTPException(429, f"Rate limit exceeded. Retry after {retry_after}s")
    except ImportError:
        pass
    
    # Check cache
    cache_key_params = {
        "messages": [{"role": m.role, "content": m.content} for m in body.messages],
        "user_id": body.user_id
    }
    try:
        from middleware import llm_cache
        cached = llm_cache.get("assistant", cache_key_params)
        if cached and not body.use_research:  # Don't cache research queries
            cached["from_cache"] = True
            return cached
    except ImportError:
        pass
    
    start_time = time.time()
    context_used = {
        "stm": False,
        "ltm": False,
        "research": False,
        "semantic": False
    }
    sources = []
    
    # Pobierz ostatnią wiadomość użytkownika
    user_messages = [m for m in body.messages if m.role == "user"]
    last_user_msg = user_messages[-1].content if user_messages else ""
    
    # === 1. PAMIĘĆ KRÓTKOTERMINOWA (STM) ===
    stm_context = ""
    if body.use_memory:
        stm_msgs = _get_stm_context(limit=body.max_context_messages)
        if stm_msgs:
            context_used["stm"] = True
            stm_context = "\n".join([
                f"{m.get('role', 'user')}: {m.get('content', '')}" 
                for m in stm_msgs[-body.max_context_messages:]
            ])
    
    # === 2. ANALIZA SEMANTYCZNA ===
    semantic_info = {}
    if body.use_semantic and last_user_msg:
        semantic_info = _semantic_analyze(last_user_msg)
        if semantic_info:
            context_used["semantic"] = True
    
    # === 3. PAMIĘĆ DŁUGOTERMINOWA (LTM) ===
    ltm_context = ""
    if body.use_memory and last_user_msg:
        ltm_facts = _get_ltm_context(last_user_msg, limit=8)
        if ltm_facts:
            context_used["ltm"] = True
            ltm_context = "\n".join([
                f"- {f.get('text', '')}" 
                for f in ltm_facts if f.get('text')
            ])
    
    # === 4. RESEARCH/AUTONAUKA (gdy brak LTM lub semantic wskazuje) ===
    research_context = ""
    needs_research = (
        body.use_research and 
        last_user_msg and 
        (not ltm_context.strip() or semantic_info.get("needs_research", False))
    )
    
    if needs_research:
        research_data = await _get_research_context(last_user_msg, body.research_depth)
        if research_data and research_data.get("context"):
            context_used["research"] = True
            research_context = research_data.get("context", "")
            sources = research_data.get("sources", [])[:8]
    
    # === 5. ZŁÓŻ KONTEKST SYSTEMOWY ===
    system_parts = [
        "Jesteś pomocnym asystentem AI. Odpowiadaj konkretnie, pomocnie i naturalnie."
    ]
    
    if stm_context:
        system_parts.append(f"\n📜 HISTORIA ROZMOWY (STM):\n{stm_context}")
    
    if ltm_context:
        system_parts.append(f"\n💾 FAKTY Z PAMIĘCI (LTM):\n{ltm_context}")
    
    if research_context:
        system_parts.append(f"\n🔍 RESEARCH/ŹRÓDŁA:\n{research_context}")
        if sources:
            system_parts.append("\n📚 ŹRÓDŁA:")
            for i, src in enumerate(sources[:5], 1):
                title = src.get("title", "")[:80]
                url = src.get("url", "")
                system_parts.append(f"[{i}] {title} - {url}")
    
    if semantic_info:
        intent = semantic_info.get("intent", "")
        entities = semantic_info.get("entities", [])
        if intent:
            system_parts.append(f"\n🎯 INTENCJA: {intent}")
        if entities:
            system_parts.append(f"📌 KLUCZOWE: {', '.join(entities[:5])}")
    
    system_message = "\n".join(system_parts)
    
    # === 6. PRZYGOTUJ WIADOMOŚCI DLA LLM ===
    llm_messages = [
        {"role": "system", "content": system_message}
    ]
    
    # Dodaj wiadomości od użytkownika (bez duplikacji z STM)
    for msg in body.messages:
        llm_messages.append({
            "role": msg.role,
            "content": msg.content
        })
    
    # === 7. WYWOŁAJ LLM ===
    llm_kwargs = {}
    if body.temperature is not None:
        llm_kwargs["temperature"] = body.temperature
    if body.max_tokens is not None:
        llm_kwargs["max_tokens"] = body.max_tokens
    
    llm_response = _call_llm(llm_messages, **llm_kwargs)
    
    # Wyciągnij tekst odpowiedzi
    if isinstance(llm_response, dict):
        answer = llm_response.get("text", "") or llm_response.get("content", "")
    else:
        answer = str(llm_response)
    
    # === 8. ZAPISZ DO PAMIĘCI (STM) ===
    if body.save_to_memory:
        # Zapisz pytanie użytkownika
        if last_user_msg:
            _save_to_stm("user", last_user_msg)
        # Zapisz odpowiedź asystenta
        if answer:
            _save_to_stm("assistant", answer)
    
    # === 9. METADATA ===
    elapsed = time.time() - start_time
    metadata = {
        "processing_time_s": round(elapsed, 2),
        "context_sources": context_used,
        "stm_messages_used": len(stm_context.split('\n')) if stm_context else 0,
        "ltm_facts_used": len(ltm_context.split('\n')) if ltm_context else 0,
        "research_sources": len(sources),
        "semantic_analyzed": bool(semantic_info),
        "timestamp": int(time.time())
    }
    
    response = ChatResponse(
        ok=True,
        answer=answer,
        sources=sources,
        context_used=context_used,
        metadata=metadata
    )
    
    # Cache response
    try:
        from middleware import llm_cache
        if not body.use_research:  # Only cache non-research
            llm_cache.set("assistant", cache_key_params, response.dict())
    except ImportError:
        pass
    
    return response

# === STREAMING VERSION ===
@router.post("/assistant/stream")
async def chat_assistant_stream(body: ChatRequest, req: Request, _=Depends(_auth)):
    """
    🤖 STREAMING CHAT ASSISTANT
    Server-Sent Events (SSE) - real-time streaming response
    
    Use with EventSource in browser:
    ```javascript
    const es = new EventSource('/api/chat/assistant/stream');
    es.onmessage = (e) => {
        const data = JSON.parse(e.data);
        if (data.type === 'chunk') {
            console.log(data.content);
        }
    };
    ```
    """
    
    # Rate limiting
    try:
        from middleware import rate_limiter
        user_id = body.user_id or req.client.host
        allowed, retry_after = rate_limiter.check_limit(user_id, "llm")
        if not allowed:
            raise HTTPException(429, f"Rate limit exceeded. Retry after {retry_after}s")
    except ImportError:
        pass
    
    async def generate():
        try:
            # Start event
            yield f"data: {json.dumps({'type': 'start', 'timestamp': time.time()})}\n\n"
            
            # Get context (same as non-streaming)
            user_messages = [m for m in body.messages if m.role == "user"]
            last_user_msg = user_messages[-1].content if user_messages else ""
            
            # STM
            stm_context = ""
            if body.use_memory:
                stm_msgs = _get_stm_context(limit=body.max_context_messages)
                if stm_msgs:
                    stm_context = "\n".join([f"{m.get('role', 'user')}: {m.get('content', '')}" for m in stm_msgs[-body.max_context_messages:]])
            
            # Send progress
            yield f"data: {json.dumps({'type': 'progress', 'step': 'memory_loaded'})}\n\n"
            
            # LTM
            ltm_context = ""
            if body.use_memory and last_user_msg:
                ltm_facts = _get_ltm_context(last_user_msg, limit=8)
                if ltm_facts:
                    ltm_context = "\n".join([f"- {f.get('text', '')}" for f in ltm_facts if f.get('text')])
            
            yield f"data: {json.dumps({'type': 'progress', 'step': 'knowledge_loaded'})}\n\n"
            
            # Build system message
            system_parts = ["Jesteś pomocnym asystentem AI."]
            if stm_context:
                system_parts.append(f"\n📜 HISTORIA:\n{stm_context}")
            if ltm_context:
                system_parts.append(f"\n💾 WIEDZA:\n{ltm_context}")
            
            system_message = "\n".join(system_parts)
            
            # Prepare messages
            llm_messages = [{"role": "system", "content": system_message}]
            for msg in body.messages:
                llm_messages.append({"role": msg.role, "content": msg.content})
            
            # Call LLM
            yield f"data: {json.dumps({'type': 'progress', 'step': 'generating'})}\n\n"
            
            llm_response = _call_llm(llm_messages)
            if isinstance(llm_response, dict):
                answer = llm_response.get("text", "") or llm_response.get("content", "")
            else:
                answer = str(llm_response)
            
            # Stream answer in chunks
            chunk_size = 30
            for i in range(0, len(answer), chunk_size):
                chunk = answer[i:i+chunk_size]
                yield f"data: {json.dumps({'type': 'chunk', 'content': chunk})}\n\n"
                await asyncio.sleep(0.03)  # Small delay for streaming effect
            
            # Save to memory
            if body.save_to_memory:
                if last_user_msg:
                    _save_to_stm("user", last_user_msg)
                if answer:
                    _save_to_stm("assistant", answer)
            
            # End event with metadata
            yield f"data: {json.dumps({'type': 'complete', 'answer': answer, 'length': len(answer)})}\n\n"
            
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )

# === HELPER ENDPOINTS ===
@router.get("/history")
async def get_chat_history(limit: int = 20, _=Depends(_auth)):
    """Pobierz historię rozmów (STM)"""
    messages = _get_stm_context(limit=limit)
    return {
        "ok": True,
        "messages": messages,
        "count": len(messages)
    }

@router.delete("/history")
async def clear_chat_history(_=Depends(_auth)):
    """Wyczyść historię rozmów"""
    try:
        import monolit as M
        if hasattr(M, "stm_clear"):
            M.stm_clear()
            return {"ok": True, "message": "Historia wyczyszczona"}
    except:
        pass
    return {"ok": False, "message": "STM nie dostępne"}

@router.post("/feedback")
async def chat_feedback(
    message_id: str,
    rating: int,  # 1-5
    comment: Optional[str] = None,
    _=Depends(_auth)
):
    """Feedback dla odpowiedzi (do uczenia się)"""
    # TODO: Zapisz feedback do LTM z tagiem feedback
    try:
        import monolit as M
        if hasattr(M, "ltm_add"):
            feedback_text = f"[FEEDBACK] Rating: {rating}/5"
            if comment:
                feedback_text += f" - {comment}"
            M.ltm_add(feedback_text, tags="feedback,learning", conf=0.5)
            return {"ok": True, "message": "Feedback zapisany"}
    except:
        pass
    return {"ok": False, "message": "Nie udało się zapisać"}
