# -*- coding: utf-8 -*-
from __future__ import annotations
import os, re, time, json, datetime as dt
from typing import Dict, Any, List
from urllib.parse import urlencode
import httpx
from bs4 import BeautifulSoup

UA = "Mozilla/5.0 MRD69/SPORTS-NEWS"

# -------- ESPN SCORES (public JSON) --------
_LEAGUE_MAP = {
    # kind -> (sports_path, league_path)
    "nba": ("basketball", "nba"),
    "ncaam": ("basketball", "mens-college-basketball"),
    "ncaaw": ("basketball", "womens-college-basketball"),
    "nhl": ("hockey", "nhl"),
    "mlb": ("baseball", "mlb"),
    "nfl": ("football", "nfl"),
    "epl": ("soccer", "eng.1"),
    "laliga": ("soccer", "esp.1"),
    "seriea": ("soccer", "ita.1"),
    "bundesliga": ("soccer", "ger.1"),
}

def _http_json(url: str, params: Dict[str,Any]|None=None, timeout: float=12.0) -> Dict[str,Any]:
    try:
        with httpx.Client(timeout=timeout, headers={"User-Agent":UA}) as c:
            r = c.get(url, params=params or {}, follow_redirects=True)
            if r.status_code == 200:
                return r.json()
    except Exception:
        pass
    return {}

def espn_scores(kind: str="nba", date: str="") -> Dict[str, Any]:
    """Zwraca wyniki meczów z ESPN: kind ∈ nba/nfl/nhl/mlb/epl/...; date=YYYYMMDD (opcjonalnie)."""
    kind = (kind or "nba").lower()
    if kind not in _LEAGUE_MAP:
        return {"ok": False, "error": f"unsupported kind '{kind}'"}
    sports, league = _LEAGUE_MAP[kind]
    if not date:
        date = dt.datetime.now().strftime("%Y%m%d")
    url = f"https://site.api.espn.com/apis/v2/sports/{sports}/{league}/scoreboard"
    j = _http_json(url, {"dates": date})

    games = []
    for ev in (j.get("events") or []):
        cid = ev.get("id", "")
        name = ev.get("name","")
        st = ev.get("status",{}).get("type",{}).get("state","")
        comp = (ev.get("competitions") or [])[0] if (ev.get("competitions")) else {}
        competitors = comp.get("competitors") or []
        home = next((t for t in competitors if (t.get("homeAway")=="home")), {})
        away = next((t for t in competitors if (t.get("homeAway")=="away")), {})
        gs = {
            "id": cid,
            "name": name,
            "state": st,  # pre/in/post
            "start": comp.get("date",""),
            "home": {
                "team": (home.get("team") or {}).get("displayName",""),
                "abbr": (home.get("team") or {}).get("abbreviation",""),
                "score": home.get("score")
            },
            "away": {
                "team": (away.get("team") or {}).get("displayName",""),
                "abbr": (away.get("team") or {}).get("abbreviation",""),
                "score": away.get("score")
            }
        }
        games.append(gs)

    return {"ok": True, "date": date, "kind": kind, "games": games, "count": len(games), "powered_by":"espn"}

# -------- NEWS: Google News RSS + DuckDuckGo --------

def _http_text(url: str, timeout: float=12.0) -> str:
    try:
        with httpx.Client(timeout=timeout, headers={"User-Agent":UA}) as c:
            r = c.get(url, follow_redirects=True)
            if r.status_code == 200:
                return r.text
    except Exception:
        pass
    return ""

def news_search(q: str, limit: int=12, hl: str="pl-PL", gl: str="PL") -> Dict[str,Any]:
    """
    Google News RSS (bez klucza): zwraca najświeższe artykuły.
    """
    q = q.strip()
    url = f"https://news.google.com/rss/search?{urlencode({'q':q,'hl':hl,'gl':gl,'ceid':f'{gl}:{hl.split("-")[0]}'})}"
    xml = _http_text(url)
    items: List[Dict[str,Any]] = []
    try:
        soup = BeautifulSoup(xml, "xml")
        for it in soup.find_all("item")[:max(1, limit)]:
            title = it.title.get_text(strip=True) if it.title else ""
            link = it.link.get_text(strip=True) if it.link else ""
            if not link and it.guid: link = it.guid.get_text(strip=True)
            pub  = it.pubDate.get_text(strip=True) if it.pubDate else ""
            desc = it.description.get_text(" ", strip=True) if it.description else ""
            items.append({"title": title, "url": link, "snippet": desc[:360], "published": pub})
    except Exception:
        pass
    return {"ok": True, "query": q, "items": items, "count": len(items), "powered_by":"googlenews-rss"}

def duck_news(q: str, limit: int=10) -> Dict[str,Any]:
    """
    DuckDuckGo HTML (bez API key) – szybkie newsy/odnośniki.
    """
    url = f"https://html.duckduckgo.com/html/?{urlencode({'q':q})}"
    html_txt = _http_text(url)
    items: List[Dict[str,Any]] = []
    try:
        soup = BeautifulSoup(html_txt, "html.parser")
        for a in soup.select("a.result__a")[:max(1, limit)]:
            title = a.get_text(" ", strip=True)
            href  = a.get("href","")
            box   = a.find_parent("div", class_="result")
            snip  = ""
            if box:
                sn = box.select_one(".result__snippet")
                if sn: snip = sn.get_text(" ", strip=True)
            if title and href:
                items.append({"title": title, "url": href, "snippet": snip[:360]})
    except Exception:
        pass
    return {"ok": True, "query": q, "items": items, "count": len(items), "powered_by":"duckduckgo"}

# -------- Bezpieczny GET proxy (read-only) --------
SAFE_SCHEMES = {"http","https"}
def safe_fetch(url: str, max_bytes: int=2_000_000) -> Dict[str,Any]:
    """
    Minimalny, bezpieczny fetch: tylko http/https, limit rozmiaru.
    """
    from urllib.parse import urlparse
    p = urlparse(url)
    if p.scheme not in SAFE_SCHEMES:
        return {"ok": False, "error":"scheme_not_allowed"}
    try:
        with httpx.Client(timeout=10.0, headers={"User-Agent":UA}) as c:
            r = c.get(url, follow_redirects=True)
            if r.status_code != 200:
                return {"ok": False, "status": r.status_code}
            data = r.text
            if len(data) > max_bytes:
                data = data[:max_bytes] + "…"
            return {"ok": True, "status": 200, "len": len(data), "content": data}
    except Exception as e:
        return {"ok": False, "error": str(e)}
