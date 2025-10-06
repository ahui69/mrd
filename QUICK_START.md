# 🚀 QUICK START - Monolit działa na 100%!

## ✅ Status: **FULLY OPERATIONAL**

Klucz API podpięty, wszystko śmiga! 🔥

---

## 🔑 Autentykacja

**Token**: `0d460626341b9fb28b7923c8018013dda72af180ffdebbfae4c3fb0e7603b9a5`

Wszystkie żądania wymagają nagłówka:
```bash
Authorization: Bearer 0d460626341b9fb28b7923c8018013dda72af180ffdebbfae4c3fb0e7603b9a5
```

---

## 🚀 Uruchomienie

```bash
# Uruchom serwer
uvicorn monolit:app --host 0.0.0.0 --port 8000

# Lub z auto-reload (development)
uvicorn monolit:app --host 0.0.0.0 --port 8000 --reload
```

Serwer dostępny: **http://localhost:8000**

---

## 🤖 GŁÓWNY ENDPOINT - Chat Assistant (ALL-IN-ONE)

### POST /api/chat/assistant

**To jest główny endpoint do podpięcia pod okno czatu!**

Automatycznie obsługuje:
- 🧠 STM (pamięć krótkotermowa)
- 💾 LTM (pamięć długotermowa)  
- 🔍 Research/Autonauka (web search)
- 🎯 Semantyka (analiza kontekstu)
- 💬 Zapis rozmów

### Przykład użycia:

```bash
curl -X POST http://localhost:8000/api/chat/assistant \
  -H "Authorization: Bearer 0d460626341b9fb28b7923c8018013dda72af180ffdebbfae4c3fb0e7603b9a5" \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "Cześć! Jak się masz?"}
    ],
    "use_memory": true,
    "use_research": false,
    "save_to_memory": true
  }'
```

### Odpowiedź:
```json
{
  "ok": true,
  "answer": "Cześć! Jestem dobrze, dziękuję...",
  "sources": [],
  "context_used": {
    "stm": true,
    "ltm": false,
    "research": false,
    "semantic": false
  },
  "metadata": {
    "processing_time_s": 1.32,
    "stm_messages_used": 2,
    "ltm_facts_used": 0,
    "research_sources": 0
  }
}
```

### Parametry:

```javascript
{
  "messages": [                    // Lista wiadomości (wymagane)
    {"role": "user", "content": "..."},
    {"role": "assistant", "content": "..."}
  ],
  "user_id": "default",           // ID użytkownika (opcjonalne)
  "use_memory": true,             // Używaj STM+LTM
  "use_research": true,           // Włącz web research
  "use_semantic": true,           // Analiza semantyczna
  "save_to_memory": true,         // Zapisz do pamięci
  "research_depth": "standard",   // quick|standard|deep
  "max_context_messages": 10,     // Ile wiadomości z historii
  "temperature": 0.7,             // Temperatura LLM (opcjonalne)
  "max_tokens": 500               // Max tokenów (opcjonalne)
}
```

---

## 📚 Inne endpointy

### 💬 LLM Chat (prosty)
```bash
POST /api/llm/chat
{
  "messages": [{"role": "user", "content": "Hello"}]
}
```

### 🧠 Pamięć (STM)
```bash
# Dodaj
POST /api/memory/add
{"role": "user", "content": "Treść wiadomości"}

# Pobierz historię
GET /api/memory/context?limit=20

# Historia dla assistant
GET /api/chat/history?limit=20
```

### 💾 Pamięć długoterminowa (LTM)
```bash
# Dodaj fakt
POST /api/ltm/add
{"text": "Python to język programowania", "tags": "python,coding"}

# Szukaj
GET /api/ltm/search?q=python&limit=5
```

### 🔍 Research/Autonauka
```bash
GET /api/research/sources?q=AI+w+2025&topk=8&deep=false
```

### 📝 Writer Pro (generowanie tekstów)
```bash
POST /api/write/creative
{
  "topic": "AI w medycynie",
  "language": "pl",
  "tone": "profesjonalny",
  "format": "article",
  "min_words": 200,
  "max_words": 400
}
```

### 🏥 Health Check
```bash
GET /api/health
# Nie wymaga autentykacji
```

---

## 🎨 Frontend - Przykład integracji

### HTML + JavaScript

```html
<!DOCTYPE html>
<html>
<head>
    <title>Chat z Asystentem</title>
</head>
<body>
    <div id="chat"></div>
    <input id="input" type="text" placeholder="Napisz wiadomość...">
    <button onclick="sendMessage()">Wyślij</button>

    <script>
    const TOKEN = "0d460626341b9fb28b7923c8018013dda72af180ffdebbfae4c3fb0e7603b9a5";
    const API = "http://localhost:8000/api/chat/assistant";
    let messages = [];

    async function sendMessage() {
        const input = document.getElementById('input');
        const userMsg = input.value;
        if (!userMsg) return;

        messages.push({role: "user", content: userMsg});
        
        const response = await fetch(API, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${TOKEN}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                messages: messages,
                use_memory: true,
                use_research: false,
                save_to_memory: true
            })
        });

        const data = await response.json();
        if (data.ok) {
            messages.push({role: "assistant", content: data.answer});
            displayMessages();
        }
        
        input.value = '';
    }

    function displayMessages() {
        const chat = document.getElementById('chat');
        chat.innerHTML = messages.map(m => 
            `<div><b>${m.role}:</b> ${m.content}</div>`
        ).join('');
    }
    </script>
</body>
</html>
```

---

## 📊 Dokumentacja API (Swagger)

Pełna interaktywna dokumentacja:
**http://localhost:8000/docs**

---

## 🔥 TLDR - Najważniejsze

1. **Serwer**: `uvicorn monolit:app --host 0.0.0.0 --port 8000`
2. **Główny endpoint**: `POST /api/chat/assistant`
3. **Token**: `0d460626341b9fb28b7923c8018013dda72af180ffdebbfae4c3fb0e7603b9a5`
4. **Docs**: http://localhost:8000/docs

**GOTOWE - WSZYSTKO DZIAŁA!** 🚀
