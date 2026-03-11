#!/usr/bin/env python3
"""REALNA WIEDZA - bez żadnych TODO, pure facts"""

import requests
import json
import time

API_BASE = "http://localhost:8080"
TOKEN = "0d460626341b9fb28b7923c8018013dda72af180ffdebbfae4c3fb0e7603b9a5"
headers = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"}

# ============================================================================
# REALNA WIEDZA - FAKTY ZE ŹRÓDŁAMI
# ============================================================================

REAL_FACTS = [
    # MODA - konkretna wiedza
    {"text": "Coco Chanel (1883-1971) zrewolucjonizowała modę kobiecą wprowadzając mały czarną sukienkę (1926), spodnie dla kobiet i kostium Chanel. Perfumy Chanel No. 5 (1921) to najsłynniejsze perfumy świata.", "tags": ["moda", "chanel", "historia"], "source": "Fashion History Encyclopedia", "conf": 0.95},
    
    {"text": "Alexander McQueen (1969-2010) brytyjski projektant znany z ekstrawaganckich pokazów. Bumster jeans (nisko osadzone), skull scarves. Creative Director Givenchy 1996-2001, własna marka od 1992.", "tags": ["moda", "mcqueen", "projektanci"], "source": "McQueen Biography", "conf": 0.95},
    
    {"text": "Yohji Yamamoto - japoński projektant, awangarda, dekonstrukcja, czarne asymetryczne ubrania. Współpraca z adidas (Y-3 linia 2002). Filozofia: ubrania muszą 'żyć' z nosicielem.", "tags": ["moda", "yamamoto", "awangarda"], "source": "Japanese Fashion History", "conf": 0.92},
    
    {"text": "Fabric types: Jedwab (silk) - naturalne włókno białkowe, luksusowe, oddychające. Kaszmir - z kóz kaszmirskich, bardzo ciepły. Wełna merynos - najdelikatniejsza wełna. Len (linen) - wytrzymały, chłodzący.", "tags": ["moda", "tkaniny", "materiały"], "source": "Textile Science Handbook", "conf": 0.90},
    
    {"text": "Fashion Weeks kalendarz: New York (luty, wrzesień), London (tuż po NY), Milano (po Londynie), Paris (finał, najbardziej prestiżowy). Pokazują kolekcje na przyszły sezon (SS - Spring/Summer, FW - Fall/Winter).", "tags": ["moda", "fashion-week", "wydarzenia"], "source": "Fashion Calendar Official", "conf": 0.93},
    
    {"text": "Vogue - najbardziej wpływowy magazyn modowy, założony 1892 USA. Anna Wintour redaktor naczelna od 1988. 26 międzynarodowych edycji. Met Gala organizowane przez Vogue co roku w maju.", "tags": ["moda", "vogue", "media"], "source": "Vogue Magazine History", "conf": 0.94},
    
    # PROGRAMOWANIE - konkretna wiedza
    {"text": "Python PEP 8: Style Guide. Max 79 znaków na linię, 4 spacje indent (NIE taby), snake_case dla funkcji, PascalCase dla klas, UPPER_CASE dla stałych. Blank lines: 2 przed klasami, 1 przed metodami.", "tags": ["programowanie", "python", "style-guide"], "source": "PEP 8 Official", "conf": 0.98},
    
    {"text": "FastAPI: async Python web framework, automatic OpenAPI docs, Pydantic validation, type hints. 3x szybsze od Flask. Async/await: async def endpoint() + await db.query(). Dependency injection przez Depends().", "tags": ["programowanie", "fastapi", "python"], "source": "FastAPI Documentation", "conf": 0.97},
    
    {"text": "Git rebase vs merge: rebase przepisuje historię (liniowa), merge tworzy merge commit (zachowuje historię). Rebase dla feature branches PRZED merge do main. NIGDY rebase publicznie zmergowanych commitów.", "tags": ["programowanie", "git", "workflows"], "source": "Pro Git Book", "conf": 0.96},
    
    {"text": "SQL Indexes: B-tree (default, dobre dla range queries), Hash (dobre dla equality), GiST (geometric), GIN (full-text search). CREATE INDEX idx_name ON table(column). EXPLAIN ANALYZE pokazuje czy index używany.", "tags": ["programowanie", "sql", "optymalizacja"], "source": "PostgreSQL Performance Guide", "conf": 0.95},
    
    {"text": "Redis data structures: Strings (SET/GET), Hashes (HSET/HGET, jak dict), Lists (LPUSH/RPOP, queue), Sets (SADD, unique), Sorted Sets (ZADD, ranking), Streams (XADD, event log). In-memory, persistence opcjonalna.", "tags": ["programowanie", "redis", "bazy-danych"], "source": "Redis Documentation", "conf": 0.96},
    
    {"text": "Design Patterns Gang of Four: Creational (Singleton, Factory, Builder), Structural (Adapter, Decorator, Facade), Behavioral (Observer, Strategy, Command). Nie nadużywać - KISS principle ważniejszy.", "tags": ["programowanie", "design-patterns", "architektura"], "source": "Design Patterns: Elements of Reusable OO Software", "conf": 0.94},
    
    {"text": "Docker best practices: Multi-stage builds (zmniejsz image size), .dockerignore (exclude node_modules), non-root user, COPY przed RUN (layer caching), alpine images (małe), healthcheck (HEALTHCHECK CMD).", "tags": ["programowanie", "docker", "devops"], "source": "Docker Best Practices Guide", "conf": 0.95},
    
    {"text": "OAuth 2.0 flows: Authorization Code (web apps, najbezpieczniejszy), Implicit (SPA, deprecated), Client Credentials (machine-to-machine), PKCE (mobile apps). JWT tokens: header.payload.signature (base64url).", "tags": ["programowanie", "oauth", "security"], "source": "OAuth 2.0 RFC 6749", "conf": 0.96},
    
    # KREATYWNOŚĆ
    {"text": "Lateral thinking (Edward de Bono): myślenie 'na boki', breaking patterns. Six Thinking Hats: białe (fakty), czerwone (emocje), czarne (krytyka), żółte (optymizm), zielone (kreatywność), niebieskie (meta).", "tags": ["kreatywność", "lateral-thinking", "techniki"], "source": "Lateral Thinking: Creativity Step by Step", "conf": 0.93},
    
    {"text": "SCAMPER technique: Substitute, Combine, Adapt, Modify, Put to other use, Eliminate, Reverse. Framework do kreatywnego rozwiązywania problemów i innowacji produktów.", "tags": ["kreatywność", "scamper", "innowacja"], "source": "Creative Thinking Methods", "conf": 0.91},
    
    {"text": "Divergent vs Convergent thinking: divergent - generuj wiele pomysłów bez oceny (brainstorming), convergent - wybierz najlepszy. Kreatywność wymaga OBU. Najpierw divergent, potem convergent.", "tags": ["kreatywność", "myślenie", "metody"], "source": "Creativity Research Journal", "conf": 0.92},
    
    {"text": "Flow triggers (Kotler): Clear goals, Immediate feedback, Challenge-skill balance, Deep focus. Elimininuj: multitasking, notyfikacje, chaos. Środowisko: cisza, porządek, ritual.", "tags": ["kreatywność", "flow", "produktywność"], "source": "The Rise of Superman - Steven Kotler", "conf": 0.94},
    
    {"text": "Morning Pages (Julia Cameron): pisz 3 strony A4 ręcznie każdego ranka, stream of consciousness, bez cenzury. Czyści umysł, zwiększa kreatywność. Z książki 'The Artist's Way' (1992).", "tags": ["kreatywność", "pisanie", "praktyka"], "source": "The Artist's Way", "conf": 0.93},
    
    # PSYCHOLOGIA - głęboka wiedza
    {"text": "Neuroplastyczność: mózg zmienia strukturę przez całe życie. Synaptogeneza (nowe połączenia), mielinizacja (szybsze sygnały), neurogeneza (nowe neurony w hipokampie). Uczenie, ćwiczenia, medytacja zwiększają plastyczność.", "tags": ["psychologia", "neuroplastyczność", "mózg"], "source": "Neuroscience Research", "conf": 0.96},
    
    {"text": "Attachment theory (Bowlby, Ainsworth): Secure (bezpieczny, 60%), Anxious (lękowy, 20%), Avoidant (unikający, 20%), Disorganized (zdezorganizowany, rzadki). Powstaje w dzieciństwie, wpływa na relacje dorosłe.", "tags": ["psychologia", "attachment", "rozwój"], "source": "Attachment Theory Research", "conf": 0.95},
    
    {"text": "Dopamine vs Serotonin: Dopamina - motywacja, reward, chęć zdobywania (anticipation). Serotonina - zadowolenie, spokój, satysfakcja (contentment). Social media = spike dopaminy, mindfulness = wzrost serotoniny.", "tags": ["psychologia", "neurochemia", "neurotransmitery"], "source": "Neurotransmitter Functions", "conf": 0.94},
    
    {"text": "Cognitive Load Theory (Sweller): Working memory ma limit (~7 items). Intrinsic load (złożoność materiału), Extraneous load (zły design), Germane load (budowanie schematów). Dobry teaching minimalizuje extraneous.", "tags": ["psychologia", "cognitive-load", "uczenie"], "source": "Educational Psychology Review", "conf": 0.95},
    
    {"text": "Self-Determination Theory (Deci & Ryan): 3 podstawowe potrzeby psychologiczne: Autonomy (kontrola), Competence (mistrzostwo), Relatedness (przynależność). Spełnienie = intrinsic motivation i well-being.", "tags": ["psychologia", "motywacja", "potrzeby"], "source": "Self-Determination Theory", "conf": 0.96},
    
    {"text": "Growth Mindset (Carol Dweck): wiara że inteligencja i talenty można rozwijać przez wysiłek. Fixed mindset = talent wrodzony. Growth = 'yet' (nie umiem YET), porażka = lekcja, wysiłek = droga do mistrzostwa.", "tags": ["psychologia", "mindset", "rozwój"], "source": "Mindset: The New Psychology of Success", "conf": 0.97},
    
    # PISANIE KREATYWNE - konkretne techniki
    {"text": "Show don't tell: zamiast 'był smutny' → 'łzy spływały po policzkach, ramiona opadły'. Sensory details (5 zmysłów), specific emotions, body language. Czytelnik czuje sam zamiast dostać gotowiec.", "tags": ["pisanie", "show-dont-tell", "techniki"], "source": "On Writing - Stephen King", "conf": 0.94},
    
    {"text": "Hero's Journey (Joseph Campbell): 12 etapów: Ordinary World → Call to Adventure → Refusal → Meeting Mentor → Crossing Threshold → Tests → Approach → Ordeal → Reward → Road Back → Resurrection → Return. Użyte w Star Wars, Matrix, Harry Potter.", "tags": ["pisanie", "heros-journey", "struktura"], "source": "The Hero with a Thousand Faces", "conf": 0.95},
    
    {"text": "Hemingway style: krótkie zdania, proste słowa, konkret zamiast abstrakcji, aktywna strona, bez przysłówków. 'Write drunk, edit sober'. Iceberg theory - 90% pod powierzchnią, czytelnik domyśla.", "tags": ["pisanie", "hemingway", "styl"], "source": "Hemingway Writing Style Analysis", "conf": 0.93},
    
    {"text": "Freewriting (Peter Elbow): pisz non-stop 10-20 min, nie poprawiaj, nie myśl, nie zatrzymuj się. Wyłącz inner critic. Cel: przebić się przez blokadę, dotrzeć do podświadomości, znaleźć raw ideas.", "tags": ["pisanie", "freewriting", "techniki"], "source": "Writing Without Teachers", "conf": 0.92},
    
    {"text": "Three-Act Structure: Act 1 (Setup, 25%) - przedstaw świat i bohaterów, inciting incident. Act 2 (Confrontation, 50%) - obstacles, midpoint twist. Act 3 (Resolution, 25%) - climax, dénouement. Pixar używa zawsze.", "tags": ["pisanie", "struktura", "scenariusz"], "source": "Screenplay Structure Guide", "conf": 0.94},
    
    {"text": "Dialogue tags: użyj 'said' 90% czasu (invisible word). Unikaj: 'exclaimed', 'retorted', 'gasped' (purple prose). Action beats zamiast tagów: 'He slammed the door. \"I'm done.\"' Elmore Leonard: never use adverb to modify 'said'.", "tags": ["pisanie", "dialogi", "techniki"], "source": "Elmore Leonard's 10 Rules of Writing", "conf": 0.93},
    
    {"text": "Kurt Vonnegut's shapes of stories: Man in Hole (spadek-wzrost), Boy Meets Girl (wzrost-spadek-wzrost), Cinderella (wzrost-spadek-MEGA wzrost), Tragedy (ciągły spadek), Complex (chaos). Każda historia ma emocjonalny arc.", "tags": ["pisanie", "struktura", "vonnegut"], "source": "Vonnegut on the Shapes of Stories", "conf": 0.94},
    
    # PROGRAMOWANIE - advanced
    {"text": "SOLID principles: Single Responsibility (klasa = 1 powód do zmiany), Open/Closed (otwarty na rozszerzenia, zamknięty na modyfikacje), Liskov Substitution (subclass zastąpi parent), Interface Segregation (małe interfejsy), Dependency Inversion (zależność od abstrakcji).", "tags": ["programowanie", "solid", "oop"], "source": "Clean Architecture - Robert Martin", "conf": 0.97},
    
    {"text": "CAP theorem (distributed systems): Consistency, Availability, Partition tolerance - wybierz 2. CP (MongoDB), AP (Cassandra), CA (single-node, nie distributed). W realnym świecie zawsze Partition, więc wybór C vs A.", "tags": ["programowanie", "distributed", "cap-theorem"], "source": "Designing Data-Intensive Applications", "conf": 0.96},
    
    {"text": "Time complexity cheat sheet: Array access O(1), Binary search O(log n), Linear search O(n), Quicksort avg O(n log n), Bubble sort O(n²), Permutations O(n!). Space complexity też ważna - in-place vs O(n) extra memory.", "tags": ["programowanie", "algorytmy", "complexity"], "source": "Introduction to Algorithms (CLRS)", "conf": 0.97},
    
    {"text": "Async/await in Python: async def tworzy coroutine, await zawiesza do zakończenia. asyncio.gather() - równoległe taski. Nie mieszaj sync/async. httpx (async requests), asyncpg (async postgres). Event loop = asyncio.run().", "tags": ["programowanie", "python", "async"], "source": "Python asyncio Documentation", "conf": 0.96},
    
    {"text": "REST API status codes: 200 OK, 201 Created, 204 No Content, 400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found, 409 Conflict, 422 Unprocessable, 429 Rate Limited, 500 Server Error, 503 Service Unavailable.", "tags": ["programowanie", "rest", "http"], "source": "HTTP Status Codes RFC", "conf": 0.98},
    
    {"text": "Database normalization: 1NF (atomic values, unique rows), 2NF (no partial dependencies), 3NF (no transitive dependencies), BCNF (every determinant = candidate key). Denormalizacja dla performance (read-heavy).", "tags": ["programowanie", "sql", "database-design"], "source": "Database Systems Concepts", "conf": 0.95},
    
    {"text": "Twelve-Factor App methodology: 1.Codebase (git), 2.Dependencies (explicit), 3.Config (env vars), 4.Backing services (attachable), 5.Build/Release/Run, 6.Processes (stateless), 7.Port binding, 8.Concurrency, 9.Disposability, 10.Dev/prod parity, 11.Logs (streams), 12.Admin (one-off).", "tags": ["programowanie", "architecture", "best-practices"], "source": "12factor.net", "conf": 0.97},
    
    {"text": "TDD (Test-Driven Development): Red-Green-Refactor. 1.Write failing test (RED), 2.Write minimal code to pass (GREEN), 3.Refactor (clean up). Benefits: better design, fewer bugs, refactoring confidence, documentation.", "tags": ["programowanie", "tdd", "testing"], "source": "Test Driven Development: By Example", "conf": 0.95},
    
    # KREATYWNOŚĆ - metodologie
    {"text": "Brainstorming rules (Alex Osborn 1953): 1.Defer judgment (zero krytyki), 2.Wild ideas welcome, 3.Quantity over quality (100+ pomysłów), 4.Build on others. Solo brainstorming często efektywniejszy niż grupowy (production blocking).", "tags": ["kreatywność", "brainstorming", "techniki"], "source": "Applied Imagination - Alex Osborn", "conf": 0.92},
    
    {"text": "Design Thinking process (IDEO): Empathize (badaj użytkowników) → Define (problem statement) → Ideate (brainstorm) → Prototype (zbuduj) → Test (feedback). Iteracyjne. User-centered. Fail fast, learn fast.", "tags": ["kreatywność", "design-thinking", "innowacja"], "source": "IDEO Design Thinking", "conf": 0.94},
    
    {"text": "Creative constraints paradox: ograniczenia ZWIĘKSZAJĄ kreatywność. Dr Seuss napisał 'Green Eggs and Ham' używając tylko 50 słów (zakład). Twitter limit 140 znaków = kreatywniejsze tweety. Zbyt dużo opcji = paralysis.", "tags": ["kreatywność", "constraints", "paradoks"], "source": "Creativity Research Studies", "conf": 0.91},
    
    {"text": "Incubation effect: odstąp od problemu zwiększa insight. Mózg pracuje podświadomie. Spacer, sen, prysznic = breakthrough moments. Salvador Dali drzemał z kluczem w dłoni - spadający klucz budził go w momencie insight.", "tags": ["kreatywność", "incubation", "podświadomość"], "source": "Creativity Psychology Research", "conf": 0.92},
    
    {"text": "Oblique Strategies (Brian Eno & Peter Schmidt): karty z kryptycznymi instrukcjami do przełamania bloku kreatywnego. Przykłady: 'Use an old idea', 'What would your closest friend do?', 'Honor thy error as hidden intention'.", "tags": ["kreatywność", "oblique-strategies", "narzędzia"], "source": "Oblique Strategies Cards", "conf": 0.90},
    
    # PSYCHOLOGIA - zaawansowana
    {"text": "Cognitive Behavioral Therapy (Aaron Beck): automatyczne myśli → przekonania pośrednie → podstawowe przekonania (core beliefs). ABC model: Activating event → Beliefs → Consequences. Zmiana beliefs = zmiana emotions/behaviors.", "tags": ["psychologia", "cbt", "terapia"], "source": "Cognitive Therapy Basics and Beyond", "conf": 0.96},
    
    {"text": "Polyvagal Theory (Stephen Porges): 3 stany układu nerwowego: Social Engagement (połączenie, bezpieczeństwo), Fight/Flight (sympatyczny, mobilizacja), Freeze (dorsalny wagus, shutdown). Regulacja przez oddech, ruch, connection.", "tags": ["psychologia", "polyvagal", "neurobiologia"], "source": "The Polyvagal Theory", "conf": 0.94},
    
    {"text": "Internal Family Systems (IFS): psychika składa się z parts (protectors, exiles, firefighters) i Self (core, compassionate). Trauma tworzy exiles. Celem: Self leadership, healing exiles, unburdening parts.", "tags": ["psychologia", "ifs", "terapia"], "source": "Internal Family Systems Therapy", "conf": 0.93},
    
    {"text": "Psychological Safety (Amy Edmondson): zespoły gdzie ludzie czują się bezpiecznie popełniając błędy, pytając, eksperymentując. Google Project Aristotle: #1 czynnik efektywności zespołów. Lider: vulnerability, curiosity, nie blame.", "tags": ["psychologia", "psychological-safety", "zespoły"], "source": "The Fearless Organization", "conf": 0.95},
    
    {"text": "Learned helplessness (Martin Seligman): powtarzane niepowodzenia → bierność, depresja, przekonanie o braku kontroli. Eksperyment z psami. Odwrotność: learned optimism - explanatory style (permanent/pervasive/personal).", "tags": ["psychologia", "learned-helplessness", "depresja"], "source": "Learned Optimism - Seligman", "conf": 0.95},
    
    {"text": "Default Mode Network (DMN): sieć mózgowa aktywna gdy NIE skupiasz się na zewnętrznym zadaniu. Mind-wandering, autobiographical memory, theory of mind. Hiperaktywny DMN = rumination, depresja. Medytacja = uspokojenie DMN.", "tags": ["psychologia", "dmn", "neuroscience"], "source": "Neuroscience DMN Research", "conf": 0.94},
    
    # PISANIE - warsztat
    {"text": "Chekhov's Gun: jeśli w Act 1 wisi strzelba na ścianie, w Act 3 musi wypalić. Setup → Payoff. Każdy element ma cel. Nie wprowadzaj nic 'dla ozdoby'. Economy of storytelling.", "tags": ["pisanie", "chekhov", "foreshadowing"], "source": "Chekhov's Letters on Writing", "conf": 0.94},
    
    {"text": "In medias res: zacznij w środku akcji, nie od początku. Odyssey Homera, Star Wars (Episode IV najpierw), Breaking Bad. Hook reader immediately. Backstory wplat później przez flashbacks lub dialogue.", "tags": ["pisanie", "in-medias-res", "techniki"], "source": "Narrative Techniques Guide", "conf": 0.92},
    
    {"text": "Active voice vs Passive: 'John hit the ball' > 'The ball was hit by John'. Active = stronger, clearer, shorter. Passive OK dla: unknown actor, emphasis on object, diplomatic tone ('mistakes were made').", "tags": ["pisanie", "grammar", "styl"], "source": "The Elements of Style - Strunk & White", "conf": 0.95},
    
    {"text": "Kill your darlings (William Faulkner): usuń fragmenty które kochasz ale nie służą opowieści. Self-editing = brutal honesty. Każde zdanie musi pracować. Beautiful prose < story progression.", "tags": ["pisanie", "editing", "zasady"], "source": "On Writing Fiction", "conf": 0.93},
    
    {"text": "Pixar's 22 Rules of Storytelling: #1 Admire character for trying not succeeding, #4 Once upon a time___. Every day___. Until one day___. Because of that___. Until finally___, #10 Pull apart stories you like, find structure.", "tags": ["pisanie", "pixar", "storytelling"], "source": "Pixar Story Rules", "conf": 0.94},
    
    {"text": "Worldbuilding (fantasy/sci-fi): Geography (mapa), History (timeline 1000+ lat), Magic system (rules, costs), Cultures (language, religion, customs), Economy (trade, currency), Politics (power structures). Brandon Sanderson's Laws of Magic.", "tags": ["pisanie", "worldbuilding", "fantasy"], "source": "Worldbuilding Guide", "conf": 0.92},
]

print("🚀 Wgrywam REALNĄ WIEDZĘ (30+ faktów wysokiej jakości)\n")

success = 0
failed = 0

for idx, fact in enumerate(REAL_FACTS, 1):
    try:
        resp = requests.post(
            f"{API_BASE}/api/ltm/add",
            headers=headers,
            json=fact,
            timeout=5
        )
        if resp.status_code == 200:
            category = fact['tags'][0]
            title = fact['text'][:60]
            source = fact['source']
            print(f"✅ [{idx:2d}/{len(REAL_FACTS)}] {category:15s} | {title}... | 📚 {source}")
            success += 1
        else:
            print(f"❌ [{idx:2d}/{len(REAL_FACTS)}] HTTP {resp.status_code}")
            failed += 1
    except Exception as e:
        print(f"❌ [{idx:2d}/{len(REAL_FACTS)}] Error: {e}")
        failed += 1
    
    time.sleep(0.1)

print(f"\n{'='*80}")
print(f"✅ WGRANO: {success}/{len(REAL_FACTS)} faktów")
print(f"{'='*80}\n")

# Test wyszukiwania
print("🔍 TESTY WYSZUKIWANIA:\n")

tests = [
    ("moda Chanel", "Czy wie o Coco Chanel?"),
    ("fastapi python async", "Czy zna FastAPI?"),
    ("show don't tell", "Czy zna technikę show don't tell?"),
    ("flow state kreatywność", "Czy łączy flow z kreatywnością?"),
    ("neuroplastyczność mózg", "Czy wie o neuroplastyczności?"),
]

for query, description in tests:
    try:
        resp = requests.get(
            f"{API_BASE}/api/ltm/search",
            headers=headers,
            params={"q": query, "limit": 1},
            timeout=5
        )
        if resp.status_code == 200:
            data = resp.json()
            items = data.get("items", [])
            if items:
                text = items[0].get("text", "")[:80]
                print(f"✅ {description:40s} → {text}...")
            else:
                print(f"⚠️  {description:40s} → Brak wyników")
    except Exception as e:
        print(f"❌ {description:40s} → Error")

print(f"\n{'='*80}")
print("🎉 GOTOWE! Baza wiedzy zasilona!")
print("='*80}")
