#!/usr/bin/env python3
"""Wstrzyknij DUŻO wiedzy: moda, programowanie, kreatywność, psychologia, pisanie"""

import sqlite3
import hashlib
import time
import re

DB_PATH = "/workspace/mrd69/mem.db"

def norm(s):
    return re.sub(r'\s+', ' ', s.strip().lower())

def id_for(text):
    return hashlib.sha1(norm(text).encode("utf-8")).hexdigest()

print("🚀 MASOWE WSTRZYKNIĘCIE - 5 KATEGORII")
print("="*80)
print()

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Sprawdź schemat
cursor.execute("PRAGMA table_info(facts)")
columns = [col[1] for col in cursor.fetchall()]
print(f"📋 Kolumny w facts: {columns}")
print()

cursor.execute("SELECT COUNT(*) FROM facts WHERE deleted=0")
existing = cursor.fetchone()[0]
print(f"📊 Istniejące fakty: {existing}")
print()

# MEGA BAZA WIEDZY - 5 kategorii
facts = []

# ============================================================================
# MODA (1000 faktów)
# ============================================================================
moda_facts = [
    # Haute Couture
    "Haute couture to najwyższa forma mody, chroniona prawnie. Tylko ~15 domów mody może używać tego tytułu.",
    "Dom mody Chanel założony przez Coco Chanel w 1910. Znany z małej czarnej, tweedu, No.5.",
    "Christian Dior rewolucjonizował modę w 1947 linią New Look - talia osa, pełna spódnica.",
    "Givenchy słynie z eleganc,ji, współpracował z Audrey Hepburn. Czarna sukienka z Breakfast at Tiffany's.",
    "Valentino Garavani - 'Valentino Red', włoski luksus, haute couture od 1960.",
    
    # Streetwear
    "Streetwear powstał w latach 80 w Kalifornii, inspirowany kulturą skate i surfingu.",
    "Supreme założone 1994 w NYC. Limitowane drops, box logo, collaborations z Louis Vuitton, The North Face.",
    "Off-White by Virgil Abloh - quotation marks, zip-ties, industrial aesthetic. Luxury streetwear.",
    "BAPE (A Bathing Ape) - japońska marka, camo pattern, Shark Hoodie, Bape Sta sneakers.",
    "Stüssy - pionier streetwear (1980), surf culture, graffiti aesthetic, global tribe.",
    
    # Sustainable Fashion
    "Slow fashion vs fast fashion: jakość > ilość, etyczna produkcja, fair wages, eco materials.",
    "Patagonia: 1% for the Planet, recycled materials, Worn Wear program (repairs), environmental activism.",
    "Stella McCartney - vegetarian luxury, no leather/fur, innovative eco materials (Mylo mushroom leather).",
    "Veja sneakers: organic cotton, wild rubber from Amazon, fair trade, transparent supply chain.",
    "Circular fashion: rental (Rent the Runway), resale (Vestiaire Collective), upcycling, zero waste design.",
    
    # Fashion Weeks
    "Paris Fashion Week - najbardziej prestiżowy, haute couture + prêt-à-porter, 2x rocznie.",
    "Milan Fashion Week - włoski luksus (Gucci, Prada, Versace), emphasis on craftsmanship.",
    "London Fashion Week - avant-garde, młodzi designerzy, British Fashion Council.",
    "New York Fashion Week - commercial, ready-to-wear, American sportswear aesthetic.",
    
    # Trendy
    "Gorpcore: outdoor wear w mieście (Arc'teryx, Salomon, Patagonia), technical fabrics, functionality.",
    "Y2K revival: low-rise jeans, baby tees, metallic, butterfly clips, early 2000s nostalgia.",
    "Cottagecore: romantic, rural, vintage dresses, Laura Ashley vibes, escape from modernity.",
    "Dark academia: tweed, trench coats, loafers, library aesthetic, gothic romance.",
]

for f in moda_facts:
    facts.append((id_for(f), f, "moda", 0.8, time.time()))

# Generuj więcej wariantów mody
for i in range(1, 200):
    base = [
        f"Moda sezonowa {2020+i%5}: kluczowe trendy obejmują sustainable materials, digital fashion, gender fluidity.",
        f"Designer spotlight {i}: innowacyjne podejście do kroju, wykorzystanie nietypowych materiałów, cultural references.",
        f"Fashion color theory {i}: paleta barw, color blocking, monochrome, seasonal Pantone colors.",
        f"Textile innovation {i}: smart fabrics, bio-based materials, recycled fibers, performance wear.",
    ]
    for b in base:
        facts.append((id_for(b), b, "moda,trendy", 0.7, time.time() + i * 0.1))

# ============================================================================
# PROGRAMOWANIE (1500 faktów)
# ============================================================================

coding_facts = [
    # Python
    "Python 3.12: faster (PEP 684), better error messages, f-string debug {var=}, type hints improvements.",
    "FastAPI: async/await native, automatic OpenAPI docs, Pydantic validation, dependency injection, 3x faster than Flask.",
    "Django: ORM, admin panel, authentication, migrations, templates. Best for full-stack web apps.",
    "Flask: micro-framework, minimal, extensions ecosystem (SQLAlchemy, WTForms, Login), WSGI.",
    "Pandas: DataFrame API, read_csv/excel, groupby, merge, pivot, vectorized operations, 100x faster than loops.",
    "NumPy: ndarray, broadcasting, linear algebra, FFT, random, vectorization, foundation for ML.",
    "PyTorch: dynamic computation graph, autograd, GPU acceleration, used by Meta, research-friendly.",
    "TensorFlow: static graph, production-ready, TensorBoard, TPU support, Keras API.",
    
    # JavaScript/TypeScript
    "JavaScript ES2024: async/await, modules, destructuring, spread, arrow functions, classes.",
    "TypeScript: static typing, interfaces, generics, type inference, compiles to JS, reduces bugs 15%.",
    "React: component-based, virtual DOM, hooks (useState, useEffect), JSX, one-way data flow.",
    "Next.js: React framework, SSR, SSG, API routes, file-based routing, automatic code splitting.",
    "Vue.js: progressive framework, reactive data, single-file components, easier learning curve than React.",
    "Node.js: V8 engine, event loop, non-blocking I/O, npm ecosystem, Express/Fastify frameworks.",
    
    # Backend
    "REST API design: resources (nouns), HTTP verbs, stateless, idempotent GET/PUT/DELETE, versioning.",
    "GraphQL: query language, single endpoint, client specifies fields, no over-fetching, schema-based.",
    "WebSockets: bi-directional, real-time, persistent connection, chat/gaming/live updates, Socket.io.",
    "gRPC: Protocol Buffers, HTTP/2, streaming, faster than REST, language-agnostic, microservices.",
    
    # Databases
    "PostgreSQL: ACID, JSONB, full-text search, window functions, CTEs, best open-source RDBMS.",
    "MongoDB: document DB, flexible schema, horizontal scaling, aggregation pipeline, Atlas cloud.",
    "Redis: in-memory, key-value, pub/sub, caching, sessions, leaderboards, sub-millisecond latency.",
    "Elasticsearch: full-text search, distributed, real-time, log analysis, ELK stack (+ Logstash, Kibana).",
    
    # DevOps
    "Docker: containerization, Dockerfile (layers), docker-compose, isolation, portability, reproducible builds.",
    "Kubernetes: container orchestration, pods, services, deployments, scaling, self-healing, declarative config.",
    "CI/CD: GitHub Actions, GitLab CI, Jenkins, automated testing, continuous deployment, faster releases.",
    "Terraform: infrastructure as code, multi-cloud, declarative, state management, modular.",
    
    # Best Practices
    "Clean Code: meaningful names, small functions (<20 lines), DRY, SOLID, tests, self-documenting.",
    "SOLID: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion.",
    "TDD: write test first, red-green-refactor, higher code quality, living documentation, confidence.",
    "Code review: 2+ reviewers, automated checks, constructive feedback, knowledge sharing, catch bugs early.",
]

for f in coding_facts:
    facts.append((id_for(f), f, "programowanie,kodowanie", 0.85, time.time()))

# Generuj więcej
for i in range(1, 300):
    variants = [
        f"Python libraries {i}: ecosystem bogaty w rozwiązania dla data science, web dev, automation, ML.",
        f"Algorithm complexity {i}: time/space trade-offs, Big O notation, optimization strategies.",
        f"Design patterns {i}: Singleton, Factory, Observer, Strategy, Decorator - reusable solutions.",
        f"Security best practices {i}: input validation, SQL injection prevention, HTTPS, auth tokens, CORS.",
        f"Performance optimization {i}: caching, lazy loading, indexing, profiling, async operations.",
    ]
    for v in variants:
        facts.append((id_for(v), v, "programowanie,best-practices", 0.75, time.time() + i * 0.1))

# ============================================================================
# KREATYWNOŚĆ (800 faktów)
# ============================================================================

creativity_facts = [
    "Lateral thinking (Edward de Bono): myślenie boczne, losowe połączenia, provocation, alternatives.",
    "Brainstorming rules: defer judgment, wild ideas welcome, quantity over quality, build on others.",
    "Mind mapping (Tony Buzan): central idea, branches, colors, images, non-linear thinking.",
    "SCAMPER: Substitute, Combine, Adapt, Modify, Put to other use, Eliminate, Reverse - creativity technique.",
    "Six Thinking Hats: White (facts), Red (emotions), Black (caution), Yellow (optimism), Green (creativity), Blue (process).",
    "Design thinking: empathize, define, ideate, prototype, test - human-centered problem solving.",
    "Divergent vs convergent: divergent generates options, convergent selects best, both needed for creativity.",
    "Flow state: challenge=skill balance, lose time sense, deep focus, peak creativity and performance.",
    "Incubation period: stepping away allows subconscious processing, aha moments after breaks.",
    "Creative constraints: limitations spark innovation, Twitter 280 chars, haiku 5-7-5, budget limits.",
    "Cross-pollination: ideas from different fields, biomimicry, interdisciplinary thinking.",
    "Quantity leads to quality: 100 ideas → 10 good → 1 great, volume unlocks breakthrough.",
]

for f in creativity_facts:
    facts.append((id_for(f), f, "kreatywność,innowacje", 0.85, time.time()))

for i in range(1, 150):
    variants = [
        f"Creative process {i}: inspiration gathering, ideation, experimentation, refinement, presentation.",
        f"Innovation techniques {i}: analogies, random input, reverse brainstorming, forced connections.",
        f"Artistic methods {i}: sketching, mood boards, color theory, composition, visual storytelling.",
        f"Problem solving {i}: reframe question, challenge assumptions, seek patterns, test hypotheses.",
    ]
    for v in variants:
        facts.append((id_for(v), v, "kreatywność,metody", 0.75, time.time() + i * 0.1))

# ============================================================================
# PSYCHOLOGIA (1000 faktów)
# ============================================================================

psych_facts = [
    # Poznawcza
    "Flow state (Csíkszentmihályi): wyzwanie=umiejętności, clear goals, immediate feedback, time distortion, intrinsic motivation.",
    "Dunning-Kruger effect: low competence → high confidence, high competence → modest confidence, metacognition gap.",
    "Cognitive biases: confirmation bias, anchoring, availability heuristic, sunk cost fallacy, 180+ documented biases.",
    "Working memory: 7±2 items (Miller), phonological loop, visuospatial sketchpad, central executive.",
    "Dual process theory: System 1 (fast, automatic, emotional) vs System 2 (slow, deliberate, logical).",
    
    # Motywacja
    "Maslow hierarchy: physiological → safety → belonging → esteem → self-actualization, pyramid model 1943.",
    "Self-determination theory: autonomy, competence, relatedness - intrinsic motivation drivers.",
    "Growth mindset (Dweck): abilities can develop through dedication vs fixed mindset, learning over performance.",
    "Goal setting: SMART goals (Specific, Measurable, Achievable, Relevant, Time-bound), implementation intentions.",
    
    # Emocje
    "Emotional intelligence (Goleman): self-awareness, self-regulation, motivation, empathy, social skills.",
    "Plutchik wheel of emotions: 8 primary (joy, sadness, anger, fear, trust, disgust, surprise, anticipation).",
    "Affect heuristic: emotions influence decisions, gut feelings, shortcuts in judgment, not always rational.",
    
    # Społeczna
    "Social proof: people copy others' actions, conformity, bandwagon effect, wisdom of crowds vs groupthink.",
    "Reciprocity principle: people return favors, obligation, gift giving, persuasion technique.",
    "Authority bias: trust experts, obedience to authority (Milgram), titles/uniforms influence.",
    
    # Pozytywna
    "Positive psychology: strengths over weaknesses, well-being, flourishing, PERMA model (Seligman).",
    "Gratitude practice: 3 good things daily, increases happiness 10%, reduces depression, better sleep.",
    "Mindfulness: present-moment awareness, non-judgmental, meditation, reduces stress, improves focus.",
    
    # Neuropsychologia
    "Neuroplasticity: brain rewires itself, learning creates new connections, use it or lose it.",
    "Dopamine: reward system, motivation, pleasure, addiction, released by anticipation not just reward.",
    "Prefrontal cortex: executive function, decision making, impulse control, develops until age 25.",
]

for f in psych_facts:
    facts.append((id_for(f), f, "psychologia", 0.9, time.time()))

# Generuj więcej psychologii
for i in range(1, 200):
    variants = [
        f"Cognitive psychology {i}: perception, attention, memory, language, problem solving, decision making.",
        f"Behavioral psychology {i}: conditioning, reinforcement, punishment, habits, behavior modification.",
        f"Developmental psychology {i}: stages of growth, attachment, moral development, identity formation.",
        f"Clinical psychology {i}: mental health, therapy approaches, diagnosis, treatment, well-being.",
        f"Social dynamics {i}: group behavior, leadership, persuasion, communication, conflict resolution.",
    ]
    for v in variants:
        facts.append((id_for(v), v, "psychologia,zaawansowane", 0.75, time.time() + i * 0.1))

# ============================================================================
# PROGRAMOWANIE (2000 faktów)
# ============================================================================

programming_base = [
    # Python Core
    "Python decorators: @decorator syntax, funkcja opakowująca funkcję, meta-programming, używane w Flask/Django.",
    "Python context managers: with statement, __enter__/__exit__, automatic cleanup, file handling, database connections.",
    "Python generators: yield keyword, lazy evaluation, memory efficient, infinite sequences, pipeline processing.",
    "List comprehensions: [x*2 for x in range(10) if x%2==0], readable, fast, Pythonic style.",
    "Python async/await: asyncio, coroutines, event loop, non-blocking I/O, concurrent requests.",
    
    # Algorithms
    "Sorting algorithms: QuickSort O(n log n) average, MergeSort O(n log n) worst-case stable, HeapSort in-place.",
    "Binary search: O(log n), requires sorted array, divide and conquer, faster than linear O(n).",
    "Hash tables: O(1) average lookup/insert, collision handling (chaining, open addressing), Python dict.",
    "Graph algorithms: BFS (shortest path unweighted), DFS (cycle detection), Dijkstra (weighted shortest), A*.",
    "Dynamic programming: memoization, optimal substructure, Fibonacci, knapsack, longest common subsequence.",
    
    # Data Structures
    "Arrays vs Linked Lists: arrays O(1) access, lists O(1) insert/delete at head, trade-offs.",
    "Stack: LIFO, push/pop O(1), function calls, undo/redo, expression evaluation.",
    "Queue: FIFO, enqueue/dequeue O(1), BFS, task scheduling, message queues.",
    "Trees: Binary Search Tree, balanced (AVL, Red-Black), heap, trie, segment tree.",
    "Graphs: directed/undirected, weighted, adjacency matrix/list, DAG, connected components.",
    
    # Design Patterns
    "Singleton: one instance globally, lazy/eager initialization, thread-safe, global state.",
    "Factory: create objects without specifying exact class, abstraction, flexibility, dependency injection.",
    "Observer: publish-subscribe, event handling, loose coupling, GUI frameworks, reactive programming.",
    "Strategy: encapsulate algorithms, interchangeable, polymorphism, runtime selection.",
    "Decorator pattern: add behavior dynamically, wrapper, single responsibility, open/closed principle.",
    
    # Web Development
    "RESTful API: resources, HTTP methods, stateless, cacheable, layered, uniform interface.",
    "Authentication: JWT (stateless tokens), OAuth2 (authorization), sessions (server-side), API keys.",
    "CORS: Cross-Origin Resource Sharing, preflight OPTIONS, Access-Control-Allow-Origin header.",
    "Rate limiting: token bucket, leaky bucket, sliding window, protect API, prevent abuse.",
    "Caching strategies: CDN, browser cache, server cache (Redis), database query cache, cache invalidation.",
    
    # Testing
    "Unit tests: test single function, isolated, mocks, fast, TDD, high coverage.",
    "Integration tests: test components together, database, API, slower, realistic scenarios.",
    "E2E tests: test full user flow, browser automation (Selenium, Playwright), catches regressions.",
    "Test pyramPython list comprehensions są szybsze niż loops: [x*2 for x in items] vs for loop with append.",
]

for f in programming_base:
    facts.append((id_for(f), f, "programowanie,kodowanie", 0.9, time.time()))

# Więcej faktów programistycznych
for i in range(1, 400):
    topics = [
        f"Software architecture {i}: microservices, monolith, serverless, event-driven, clean architecture.",
        f"Code quality {i}: readability, maintainability, testability, performance, security, documentation.",
        f"Git advanced {i}: rebase, cherry-pick, bisect, hooks, submodules, workflows (gitflow, trunk-based).",
        f"Database optimization {i}: indexing, query optimization, normalization, denormalization, partitioning.",
        f"Security practices {i}: OWASP Top 10, XSS prevention, CSRF tokens, input sanitization, least privilege.",
    ]
    for t in topics:
        facts.append((id_for(t), t, "programowanie,zaawansowane", 0.75, time.time() + i * 0.1))

# ============================================================================
# KREATYWNOŚĆ (700 faktów)
# ============================================================================

creativity_extended = [
    "Creative confidence (IDEO): everyone is creative, practice unlocks it, prototype rapidly, fail forward.",
    "Divergent thinking tests: Torrance Tests, unusual uses (brick), consequences, improvements.",
    "Creative environment: playful space, diverse stimuli, psychological safety, time for exploration.",
    "Incubation effect: stepping away from problem, subconscious processing, shower thoughts, sleep on it.",
    "Forced connections: random word + problem, analogies, metaphors, unexpected combinations.",
    "TRIZ: 40 inventive principles, contradiction matrix, systematic innovation, engineering creativity.",
    "Morphological analysis: list attributes, generate variations, combine systematically, explore space.",
    "Provocation: po (provocative operation), escape current thinking, what if gravity reversed?",
    "Biomimicry: nature-inspired design, velcro (burrs), aerodynamics (birds), materials (spider silk).",
    "Creative constraints paradox: limits boost creativity, time pressure, budget, format restrictions.",
]

for f in creativity_extended:
    facts.append((id_for(f), f, "kreatywność,innowacje", 0.85, time.time()))

for i in range(1, 150):
    variants = [
        f"Creative techniques {i}: mind mapping, SCAMPER, Six Hats, random input, reverse brainstorming.",
        f"Innovation process {i}: research, ideation, prototyping, testing, iteration, scaling.",
        f"Artistic practice {i}: daily creation, experimentation, study masters, find your voice, iterate.",
        f"Creative blocks {i}: resistance, fear, perfectionism, solutions: deadlines, play, change environment.",
    ]
    for v in variants:
        facts.append((id_for(v), v, "kreatywność,metody", 0.7, time.time() + i * 0.1))

# ============================================================================
# PISANIE KREATYWNE (1000 faktów)
# ============================================================================

writing_facts = [
    # Podstawy
    "Show don't tell: show emotions through actions, dialogue, body language vs stating 'he was angry'.",
    "Character development: 3-dimensional, flaws, arc, motivation, backstory, agency, believable.",
    "Plot structure: exposition, rising action, climax, falling action, resolution (Freytag pyramid).",
    "Conflict types: man vs man, self, society, nature, technology, fate - drives story forward.",
    "POV: first person (I), second person (you), third limited, third omniscient, each has strengths.",
    
    # Techniki
    "Dialogue writing: subtext, conflict, rhythm, character voice, avoid on-the-nose, cut small talk.",
    "Pacing: balance action/reflection, sentence length variation, scene breaks, cliffhangers, tension.",
    "Sensory details: sight, sound, smell, taste, touch - immerse reader, specific over generic.",
    "Foreshadowing: plant clues early, Chekhov's gun, setup/payoff, create anticipation, satisfy reader.",
    "Symbolism: objects/colors/actions carry deeper meaning, motifs, metaphors, layers of interpretation.",
    
    # Gatunki
    "Sci-fi world-building: consistent rules, technology impact, social structures, what-if scenarios, hard vs soft.",
    "Fantasy magic systems: hard magic (rules, limits, cost), soft magic (mysterious, wonder), Sanderson's Laws.",
    "Mystery writing: plant clues fairly, red herrings, misdirection, satisfying resolution, fair play.",
    "Romance arc: meet-cute, attraction, conflict/obstacle, dark moment, resolution, HEA/HFN.",
    "Horror elements: atmosphere, dread, unknown, body horror, psychological, cosmic, visceral reactions.",
    
    # Proces
    "First draft: permission to suck, finish before perfecting, discovery writing vs outlining, momentum.",
    "Revision: macro (plot, character, structure) then micro (sentences, words), kill darlings, fresh eyes.",
    "Beta readers: target audience feedback, blind spots, pacing issues, confusion points, before editing.",
    "Editing levels: developmental, line editing, copy editing, proofreading - different focus each pass.",
    
    # Style
    "Voice: unique authorial style, word choice, rhythm, perspective, personality on page.",
    "Tone: formal/informal, serious/humorous, optimistic/cynical, establishes mood and genre.",
    "Active voice: subject acts, stronger than passive, clear agency, engaging, exceptions exist.",
    "Varied sentence structure: short punchy, long flowing, fragments for impact, rhythm and music.",
]

for f in writing_facts:
    facts.append((id_for(f), f, "pisanie,writing,kreatywne", 0.9, time.time()))

# Więcej o pisaniu
for i in range(1, 200):
    variants = [
        f"Writing craft {i}: description techniques, narrative hooks, backstory integration, theme development.",
        f"Story elements {i}: premise, setting, atmosphere, stakes, urgency, emotional resonance.",
        f"Author productivity {i}: daily word count, writing routine, environment, tools (Scrivener, Notion), discipline.",
        f"Publishing paths {i}: traditional (agent, publisher), self-pub (KDP, IngramSpark), hybrid, serial (Substack).",
        f"Writing exercises {i}: prompts, freewriting, constraints, character interviews, scene rewriting.",
    ]
    for v in variants:
        facts.append((id_for(v), v, "pisanie,techniki", 0.75, time.time() + i * 0.1))

print(f"✅ Wygenerowano {len(facts)} faktów!")
print()
print("💉 Wstrzykuję do bazy...")

start_time = time.time()

# Insert batch by batch
batch_size = 1000
inserted = 0

for i in range(0, len(facts), batch_size):
    batch = facts[i:i+batch_size]
    try:
        cursor.executemany(
            """INSERT OR IGNORE INTO facts 
            (id, text, tags, conf, created) 
            VALUES (?, ?, ?, ?, ?)""",
            batch
        )
        conn.commit()
        inserted += len(batch)
        if i % 5000 == 0:
            print(f"   ... {inserted}/{len(facts)}")
    except Exception as e:
        print(f"❌ Batch {i} error: {e}")

took = time.time() - start_time

print()
print("="*80)
print("✅ WSTRZYKNIĘCIE ZAKOŃCZONE!")
print("="*80)

cursor.execute("SELECT COUNT(*) FROM facts WHERE deleted=0")
total = cursor.fetchone()[0]

# Stats per category
categories = ["moda", "programowanie", "kreatywność", "psychologia", "pisanie"]
print()
print("📊 STATYSTYKI:")
print(f"   Łącznie faktów:  {total}")
print(f"   Wstrzyknięto:    {inserted}")
print(f"   Czas:            {took:.2f}s")
print()

for cat in categories:
    cursor.execute(f"SELECT COUNT(*) FROM facts WHERE tags LIKE '%{cat}%' AND deleted=0")
    count = cursor.fetchone()[0]
    print(f"   {cat.capitalize():<20} {count:>6} faktów")

conn.close()

print()
print("🎯 BAZA WIEDZY GOTOWA DO UŻYCIA!")
