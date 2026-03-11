# 🚀 QUICK START - Mordzix AI System

## ⚡ NAJSZYBSZY START

```bash
bash start.sh
```

**DONE!** Otwórz http://localhost:8080/ 

---

## 📋 CO SIĘ DZIEJE

1. ✅ Wczytuje `.env` (wszystkie klucze)
2. ✅ Instaluje dependencies
3. ✅ Zabija stare procesy
4. ✅ Sprawdza bazę danych
5. ✅ Startuje serwer
6. ✅ Health check

---

## 🔧 PLIKI

### `start.sh` - Main starter
- Wszystko w jednym
- Auto-cleanup
- Health verification

### `.env` - Configuration  
- **50+ zmiennych**
- Klucze API już wypełnione
- Gotowe do użycia

### `monolit.py` - Core system
- 81+ faktów w bazie
- Wszystkie moduły
- Ready to go

---

## 🌐 DOSTĘPNE URLs

```
Chat Assistant:  http://localhost:8080/
Paint Editor:    http://localhost:8080/paint  
API Docs:        http://localhost:8080/docs
```

---

## 🧪 QUICK TESTS

### Test 1: Health
```bash
curl http://localhost:8080/api/health
```

### Test 2: LTM Search
```bash
curl -H "Authorization: Bearer 0d460626341b9fb28b7923c8018013dda72af180ffdebbfae4c3fb0e7603b9a5" \
  "http://localhost:8080/api/ltm/search?q=python&limit=2"
```

### Test 3: Chat
W przeglądarce zapytaj:
- "Co wiesz o Coco Chanel?"
- "Wyjaśnij FastAPI"
- "Show don't tell - przykład"

---

## 📚 WIEDZA W SYSTEMIE

**81+ faktów ze źródłami:**

- 🎨 **Moda** (10): Chanel, McQueen, Yamamoto, Vogue...
- 💻 **Programowanie** (22): Python, FastAPI, Git, Docker, SOLID...
- 🎨 **Kreatywność** (10): Lateral thinking, Flow, Design Thinking...
- 🧠 **Psychologia** (15): Neuroplastyczność, CBT, Growth Mindset...
- ✍️ **Pisanie** (12): Show don't tell, Hero's Journey, Hemingway...
- 🌍 **Geografia** (12): Everest, Tokio, Santorini...

**Źródła:** Realne książki, research papers, dokumentacje

---

## 🛑 STOP SERVER

```bash
# Zobacz PID
ps aux | grep uvicorn

# Kill
kill [PID]

# Lub brutal
pkill -9 python3
```

---

## ⚙️ ZMIENNE .ENV

Najważniejsze (reszta w `.env`):

```bash
AUTH_TOKEN=0d460626341b9fb28b7923c8018013dda72af180ffdebbfae4c3fb0e7603b9a5
LLM_API_KEY=w52XW0XN6zoV9hdY8OONhLu6tvnFaXbZ
LLM_MODEL=zai-org/GLM-4.6
PORT=8080
```

---

**KONIEC! Wszystko ready! 🔥**
