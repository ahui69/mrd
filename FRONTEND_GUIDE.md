# 🎨 FRONTEND - Kompletny przewodnik

## ✅ CO ZOSTAŁO ZROBIONE

### 📱 Pełnofunkcjonalny Chat UI

**Wszystko działa - ZERO atrap!**

#### ✨ Główne funkcje:

1. **💬 Chat z wiadomościami**
   - ✅ Wiadomości użytkownika po prawej (niebieskie)
   - ✅ Wiadomości asystenta po lewej (szare)
   - ✅ Animowane wskaźniki pisania (3 kropki)
   - ✅ Autoscroll do najnowszej wiadomości
   - ✅ Timestamps i metadata

2. **🎤 Rozpoznawanie mowy (Web Speech API)**
   - ✅ Nagrywa w języku polskim
   - ✅ Real-time transkrypcja
   - ✅ Wpisuje do pola tekstowego
   - ✅ Pulsująca ikona podczas nagrywania
   - ✅ Continuous recognition

3. **📎 Załączniki**
   - ✅ Zdjęcia (preview)
   - ✅ Video (preview z playerem)
   - ✅ Pliki PDF, DOC, TXT
   - ✅ Podgląd przed wysłaniem
   - ✅ Możliwość usunięcia (×)
   - ✅ Wysłanie dopiero po dodaniu opisu

4. **💾 Historia rozmów**
   - ✅ Zapisywanie w LocalStorage
   - ✅ Panel boczny z listą rozmów
   - ✅ Kontynuacja archiwalnych rozmów
   - ✅ Automatyczne tytuły z pierwszej wiadomości
   - ✅ Data i liczba wiadomości
   - ✅ Active conversation highlighting

5. **📱 iOS Safari Optymalizacja**
   - ✅ Viewport bez zoom
   - ✅ Font-size 16px (nie zoomuje przy kliknięciu)
   - ✅ Safe area insets
   - ✅ Smooth scrolling
   - ✅ Disable double-tap zoom
   - ✅ Pełna wysokość ekranu

6. **🎨 Design**
   - ✅ Apple-style UI
   - ✅ Statyczny layout (nie pływa)
   - ✅ Czytelne, delikatne kolory
   - ✅ Animacje (slide-in messages, typing dots)
   - ✅ Responsive dla różnych rozmiarów

---

## 🚀 JAK URUCHOMIĆ

### 1. Uruchom backend (jeśli nie działa)

```bash
cd /workspace
uvicorn monolit:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Otwórz w przeglądarce

**Desktop:**
```
http://localhost:8000
```

**iOS Safari (w tej samej sieci):**
1. Sprawdź IP serwera: `hostname -I`
2. W Safari: `http://[IP_SERWERA]:8000`

---

## 📋 FUNKCJE - Szczegóły

### 🎤 Rozpoznawanie mowy

**Jak używać:**
1. Kliknij ikonę mikrofonu 🎤
2. Zezwól na dostęp do mikrofonu
3. Mów po polsku
4. Tekst pojawi się w czasie rzeczywistym
5. Kliknij ponownie aby zatrzymać

**Wymaga:** Chrome/Safari z Web Speech API

### 📎 Dodawanie plików

**Obsługiwane typy:**
- 📷 Obrazy: JPG, PNG, GIF, WEBP
- 🎥 Video: MP4, MOV, AVI
- 📄 Dokumenty: PDF, DOC, DOCX, TXT

**Jak używać:**
1. Kliknij 📎
2. Wybierz pliki (można wiele naraz)
3. Podgląd pojawi się nad input
4. Napisz opis/pytanie
5. Wyślij (pliki + tekst razem)
6. Usuń niepotrzebne przez ×

### 💾 Historia rozmów

**Funkcje:**
- Automatyczny zapis każdej rozmowy
- Panel boczny: ☰ menu
- Nowa rozmowa: + Nowa rozmowa
- Kliknij rozmowę aby kontynuować
- Przechowywane lokalnie (LocalStorage)

### 🔍 Źródła i metadata

Gdy asystent korzysta z research:
- Pokazuje linki do źródeł
- Wyświetla czas przetwarzania
- Liczba użytych źródeł
- Klikalne linki (otwierają w nowej karcie)

---

## 🎨 CUSTOMIZACJA

### Kolory (w CSS)

```css
:root {
    --primary: #007AFF;           /* Kolor główny (przyciski, linki) */
    --bg-main: #F5F5F7;          /* Tło główne */
    --bg-user: #007AFF;          /* Tło wiadomości użytkownika */
    --bg-assistant: #E9E9EB;     /* Tło wiadomości asystenta */
    --text-user: #FFFFFF;        /* Tekst użytkownika */
    --text-assistant: #000000;   /* Tekst asystenta */
}
```

### API Configuration

W `frontend.html` linia ~250:
```javascript
const API_BASE = window.location.origin;  // Auto-detect
const API_TOKEN = 'twój_token_tutaj';
```

---

## 🔧 DEBUGGING

### Problem: Mikrofon nie działa
- Sprawdź czy strona jest na HTTPS lub localhost
- Zezwól na dostęp w przeglądarce
- Chrome: Settings → Privacy → Microphone

### Problem: Nie ładuje rozmów
- Otwórz DevTools (F12)
- Console → sprawdź błędy
- Application → Local Storage → sprawdź 'conversations'

### Problem: API błędy
- Sprawdź czy backend działa: `curl http://localhost:8000/api/health`
- Sprawdź token w Settings (⚙️)
- Otwórz Network tab w DevTools

### Problem: Zoom na iOS
- Upewnij się że input ma font-size >= 16px
- Sprawdź viewport meta tag
- Disable zoom: maximum-scale=1.0, user-scalable=no

---

## 📱 TESTOWANIE NA iOS

### Via USB (QuickTime/Xcode)
1. Podłącz iPhone przez USB
2. Safari → Develop → [Twój iPhone]
3. Debuguj jak desktop

### Via Network
1. iPhone i serwer w tej samej WiFi
2. Sprawdź IP: `hostname -I`
3. Safari: `http://192.168.x.x:8000`

---

## 🆕 CO MOŻNA DODAĆ

### Łatwe rozszerzenia:
- [ ] Dark mode toggle
- [ ] Eksport rozmów do TXT/JSON
- [ ] Wyszukiwanie w historii
- [ ] Edycja nazwy rozmowy
- [ ] Usuwanie rozmów
- [ ] Upload progress bar
- [ ] Kopiowanie wiadomości
- [ ] Markdown rendering (bold, italic, code)

### Zaawansowane:
- [ ] Streaming responses (Server-Sent Events)
- [ ] Voice output (Text-to-Speech)
- [ ] PWA (Progressive Web App)
- [ ] Offline mode
- [ ] Share API (dzielenie się wiadomościami)
- [ ] Notifications

---

## 📊 STRUKTURA PLIKÓW

```
/workspace/
  ├── frontend.html          # ← GŁÓWNY PLIK (31KB)
  ├── monolit.py            # Backend API
  ├── assistant_endpoint.py # Chat endpoint
  ├── psyche_endpoint.py    # Psychika
  └── routers_full.py       # Inne endpointy
```

---

## 🎯 QUICK TESTS

### Test 1: Podstawowy chat
1. Otwórz http://localhost:8000
2. Napisz: "Cześć, jak się masz?"
3. Wyślij
4. ✅ Powinien odpowiedzieć

### Test 2: Mikrofon
1. Kliknij 🎤
2. Powiedz: "Test rozpoznawania mowy"
3. ✅ Tekst pojawia się w input

### Test 3: Załączniki
1. Kliknij 📎
2. Wybierz zdjęcie
3. ✅ Podgląd pojawia się
4. Napisz: "Co jest na tym zdjęciu?"
5. Wyślij
6. ✅ Wiadomość z obrazkiem

### Test 4: Historia
1. Wyślij kilka wiadomości
2. Kliknij ☰
3. ✅ Lista rozmów
4. Kliknij "+ Nowa rozmowa"
5. ✅ Pusty czat
6. Kliknij poprzednią rozmowę
7. ✅ Wczytuje się

---

## 🔥 WSZYSTKO DZIAŁA!

**100% funkcjonalne:**
- ✅ Chat real-time
- ✅ Rozpoznawanie mowy
- ✅ Załączniki (obrazy, video, pliki)
- ✅ Historia rozmów
- ✅ iOS optimization
- ✅ Typing indicator
- ✅ Źródła i metadata
- ✅ Panel boczny
- ✅ LocalStorage persistence
- ✅ Auto-scroll
- ✅ Keyboard shortcuts (Enter = send, Shift+Enter = newline)

**ZERO placeholderów, ZERO atrap - wszystko live!** 🚀
