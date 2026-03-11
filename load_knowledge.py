#!/usr/bin/env python3
"""Wgraj wiedzę do LTM"""

import requests
import json

API_BASE = "http://localhost:8080"
TOKEN = "0d460626341b9fb28b7923c8018013dda72af180ffdebbfae4c3fb0e7603b9a5"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# Wiedza do wgrania
knowledge = [
    # MODA
    {
        "text": "Haute couture to najwyższa forma mody luksusowej, ręcznie szyte ubrania na zamówienie. Główne domy: Chanel, Dior, Givenchy, Valentino.",
        "tags": ["moda", "haute-couture", "luksus"],
        "source": "fashion-expert"
    },
    {
        "text": "Streetwear to styl pochodzący z lat 80/90, inspirowany kulturą skate i hip-hop. Marki: Supreme, Off-White, BAPE, Stüssy.",
        "tags": ["moda", "streetwear", "kultura"],
        "source": "fashion-trends"
    },
    {
        "text": "Slow fashion to ruch przeciwko fast fashion - promuje etyczną produkcję, wysoką jakość i długowieczność ubrań.",
        "tags": ["moda", "slow-fashion", "ekologia"],
        "source": "sustainable-fashion"
    },
    {
        "text": "Fashion Week odbywa się 4 razy w roku w Paryżu, Mediolanie, Londynie i Nowym Jorku. Najbardziej prestiżowy to Paris Fashion Week.",
        "tags": ["moda", "fashion-week", "wydarzenia"],
        "source": "fashion-calendar"
    },
    
    # PODRÓŻE
    {
        "text": "Santorini w Grecji słynie z białych domów z niebieskimi kopułami, zapierających dech w piersiach zachodów słońca i wulkanicznej plaży Red Beach.",
        "tags": ["podróże", "grecja", "santorini"],
        "source": "travel-guide"
    },
    {
        "text": "Machu Picchu w Peru to starożytne miasto Inków na wysokości 2430m n.p.m. Zbudowane w XV wieku, odkryte w 1911 roku.",
        "tags": ["podróże", "peru", "machu-picchu", "historia"],
        "source": "world-heritage"
    },
    {
        "text": "Tokio to największe miasto świata (38 mln metropolia). Dzielnice: Shibuya (crossing), Shinjuku (neon), Harajuku (moda), Akihabara (tech).",
        "tags": ["podróże", "japonia", "tokio"],
        "source": "city-guide"
    },
    {
        "text": "Islandia to kraj gejzerów, wodospadów i zorzy polarnej. Must-see: Blue Lagoon, Golden Circle, Jökulsárlón (lodowa laguna), Geysir.",
        "tags": ["podróże", "islandia", "natura"],
        "source": "iceland-travel"
    },
    {
        "text": "Bali w Indonezji: Ubud (kultura, tarasy ryżowe), Seminyak (plaże, kluby), Uluwatu (surfing, świątynie), Nusa Penida (wyspy).",
        "tags": ["podróże", "indonezja", "bali"],
        "source": "bali-guide"
    },
    
    # GEOGRAFIA
    {
        "text": "Mount Everest (8849m) to najwyższa góra świata, na granicy Nepalu i Tybetu. Pierwsza zdobyta przez Hillary i Norgaya w 1953.",
        "tags": ["geografia", "góry", "everest"],
        "source": "geography-facts"
    },
    {
        "text": "Amazonia to największy las deszczowy świata (5.5M km²), produkuje 20% tlenu. Rzeka Amazonka ma 6400km długości.",
        "tags": ["geografia", "amazonia", "ekologia"],
        "source": "rainforest-data"
    },
    {
        "text": "Sahara to największa gorąca pustynia (9M km²). Temperatury: dzień 50°C, noc może spaść poniżej 0°C.",
        "tags": ["geografia", "sahara", "pustynia"],
        "source": "desert-climate"
    },
    {
        "text": "Rów Mariański to najgłębsze miejsce na Ziemi (10,994m). Tylko 3 osoby dotarły na dno: Don Walsh, Jacques Piccard (1960), James Cameron (2012).",
        "tags": ["geografia", "ocean", "mariański"],
        "source": "ocean-depths"
    },
    
    # PSYCHOLOGIA
    {
        "text": "Flow state (stan przepływu) to stan całkowitego zaangażowania w aktywność, gdzie tracisz poczucie czasu. Opisany przez Mihály Csíkszentmihályi.",
        "tags": ["psychologia", "flow", "produktywność"],
        "source": "psychology-research"
    },
    {
        "text": "Efekt Dunninga-Krugera: osoby niekompetentne przeceniają swoje umiejętności, eksperci je niedoceniają. Paradoks wiedzy.",
        "tags": ["psychologia", "dunning-kruger", "poznanie"],
        "source": "cognitive-bias"
    },
    {
        "text": "Maslow's hierarchy: fizjologia → bezpieczeństwo → przynależność → szacunek → samorealizacja. Teoria motywacji z 1943.",
        "tags": ["psychologia", "maslow", "motywacja"],
        "source": "maslow-theory"
    },
    {
        "text": "Mindfulness (uważność) to praktyka świadomego bycia w teraźniejszości. Redukuje stres, poprawia koncentrację i regulację emocji.",
        "tags": ["psychologia", "mindfulness", "medytacja"],
        "source": "mindfulness-research"
    },
    {
        "text": "Pareto 80/20: 80% efektów pochodzi z 20% przyczyn. Stosowane w produktywności, biznesie, zarządzaniu czasem.",
        "tags": ["psychologia", "pareto", "produktywność"],
        "source": "pareto-principle"
    },
    
    # KODOWANIE
    {
        "text": "Python: język dynamiczny, interpretowany. Popularne frameworki: Django (web), FastAPI (API), PyTorch (ML), Pandas (data).",
        "tags": ["kodowanie", "python", "programowanie"],
        "source": "python-guide"
    },
    {
        "text": "REST API principles: stateless, client-server, cacheable, uniform interface. HTTP methods: GET, POST, PUT, DELETE, PATCH.",
        "tags": ["kodowanie", "rest", "api"],
        "source": "rest-api-design"
    },
    {
        "text": "Git workflow: git add → git commit → git push. Branche: feature branch → pull request → merge do main. Semantic commits: feat/fix/docs/refactor.",
        "tags": ["kodowanie", "git", "version-control"],
        "source": "git-best-practices"
    },
    {
        "text": "Docker: konteneryzacja aplikacji. Dockerfile → docker build → docker run. Docker Compose dla multi-container apps.",
        "tags": ["kodowanie", "docker", "devops"],
        "source": "docker-tutorial"
    },
    {
        "text": "Big O notation: O(1) constant, O(log n) logarithmic, O(n) linear, O(n²) quadratic, O(2ⁿ) exponential. Ważne dla optymalizacji.",
        "tags": ["kodowanie", "algorytmy", "complexity"],
        "source": "algorithm-complexity"
    },
    {
        "text": "Clean Code principles: DRY (Don't Repeat Yourself), KISS (Keep It Simple), SOLID, meaningful names, small functions, tests.",
        "tags": ["kodowanie", "clean-code", "best-practices"],
        "source": "clean-code-book"
    },
]

print("🚀 Rozpoczynam wgrywanie wiedzy do LTM...\n")

success = 0
fail = 0

for idx, item in enumerate(knowledge, 1):
    try:
        resp = requests.post(
            f"{API_BASE}/api/ltm/add",
            headers=headers,
            json={
                "text": item["text"],
                "tags": item["tags"],
                "source": item["source"],
                "user_id": "system"
            }
        )
        if resp.status_code == 200:
            print(f"✅ [{idx}/{len(knowledge)}] {item['tags'][0]}: {item['text'][:60]}...")
            success += 1
        else:
            print(f"❌ [{idx}/{len(knowledge)}] Error {resp.status_code}")
            fail += 1
    except Exception as e:
        print(f"❌ [{idx}/{len(knowledge)}] Exception: {e}")
        fail += 1

print(f"\n📊 Wgrano: {success} OK, {fail} FAIL")
print(f"\n🔍 Test wyszukiwania...")

# Test wyszukiwania
queries = ["moda", "podróże tokio", "psychologia flow", "python api"]
for q in queries:
    try:
        resp = requests.get(
            f"{API_BASE}/api/ltm/search",
            headers=headers,
            params={"q": q, "topk": 2}
        )
        if resp.status_code == 200:
            results = resp.json()
            print(f"\n🔎 '{q}': znaleziono {len(results.get('results', []))} wyników")
            for r in results.get('results', [])[:1]:
                print(f"   → {r.get('text', '')[:80]}...")
    except Exception as e:
        print(f"❌ Search error: {e}")

print("\n✅ GOTOWE!")
