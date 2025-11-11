# app.py
import streamlit as st
import unicodedata
import random
import time
from difflib import get_close_matches

# -----------------------------------------------------------------------------
# App configuration
#   - Sets the browser tab title and favicon.
#   - Do this as early as possible, before creating any UI elements.
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Waves Capital Guesser", page_icon="🌊")

# =========================================================
# Data: Country | Capital | Continent
# (compact list; add/remove items as you like)
# ---------------------------------------------------------
# RAW is a triple-pipe-delimited text block: "Country|Capital|Continent".
# Keeping it as a raw string makes it easy to edit in-place without CSV files.
# The parse_raw() function below will:
#   - ignore malformed lines
#   - de-duplicate exact triplets
#   - return a list of tuples (country, capital, continent)
# =========================================================
RAW = """
Afghanistan|Kabul|Asia
Albania|Tirana|Europe
Algeria|Algiers|Africa
Andorra|Andorra la Vella|Europe
Angola|Luanda|Africa
Antigua and Barbuda|Saint John's|North America
Argentina|Buenos Aires|South America
Armenia|Yerevan|Asia
Australia|Canberra|Oceania
Austria|Vienna|Europe
Azerbaijan|Baku|Asia
Bahamas|Nassau|North America
Bahrain|Manama|Asia
Bangladesh|Dhaka|Asia
Barbados|Bridgetown|North America
Belarus|Minsk|Europe
Belgium|Brussels|Europe
Belize|Belmopan|North America
Benin|Porto-Novo|Africa
Bhutan|Thimphu|Asia
Bolivia|Sucre|South America
Bosnia and Herzegovina|Sarajevo|Europe
Botswana|Gaborone|Africa
Brazil|Brasília|South America
Brunei|Bandar Seri Begawan|Asia
Bulgaria|Sofia|Europe
Burkina Faso|Ouagadougou|Africa
Burundi|Gitega|Africa
Cabo Verde|Praia|Africa
Cambodia|Phnom Penh|Asia
Cameroon|Yaoundé|Africa
Canada|Ottawa|North America
Central African Republic|Bangui|Africa
Chad|N'Djamena|Africa
Chile|Santiago|South America
China|Beijing|Asia
Colombia|Bogotá|South America
Comoros|Moroni|Africa
Congo (Republic of the)|Brazzaville|Africa
Congo (Democratic Republic)|Kinshasa|Africa
Costa Rica|San José|North America
Côte d'Ivoire|Yamoussoukro|Africa
Croatia|Zagreb|Europe
Cuba|Havana|North America
Cyprus|Nicosia|Asia
Czechia|Prague|Europe
Denmark|Copenhagen|Europe
Djibouti|Djibouti|Africa
Dominica|Roseau|North America
Dominican Republic|Santo Domingo|North America
Ecuador|Quito|South America
Egypt|Cairo|Africa
El Salvador|San Salvador|North America
Equatorial Guinea|Malabo|Africa
Eritrea|Asmara|Africa
Estonia|Tallinn|Europe
Eswatini|Mbabane|Africa
Ethiopia|Addis Ababa|Africa
Fiji|Suva|Oceania
Finland|Helsinki|Europe
France|Paris|Europe
Gabon|Libreville|Africa
Gambia|Banjul|Africa
Georgia|Tbilisi|Asia
Germany|Berlin|Europe
Ghana|Accra|Africa
Greece|Athens|Europe
Grenada|St. George's|North America
Guatemala|Guatemala City|North America
Guinea|Conakry|Africa
Guinea-Bissau|Bissau|Africa
Guyana|Georgetown|South America
Haiti|Port-au-Prince|North America
Honduras|Tegucigalpa|North America
Hungary|Budapest|Europe
Iceland|Reykjavík|Europe
India|New Delhi|Asia
Indonesia|Jakarta|Asia
Iran|Tehran|Asia
Iraq|Baghdad|Asia
Ireland|Dublin|Europe
Israel|Jerusalem|Asia
Italy|Rome|Europe
Jamaica|Kingston|North America
Japan|Tokyo|Asia
Jordan|Amman|Asia
Kazakhstan|Astana|Asia
Kenya|Nairobi|Africa
Kiribati|Tarawa|Oceania
Kuwait|Kuwait City|Asia
Kyrgyzstan|Bishkek|Asia
Laos|Vientiane|Asia
Latvia|Riga|Europe
Lebanon|Beirut|Asia
Lesotho|Maseru|Africa
Liberia|Monrovia|Africa
Libya|Tripoli|Africa
Liechtenstein|Vaduz|Europe
Lithuania|Vilnius|Europe
Luxembourg|Luxembourg|Europe
Madagascar|Antananarivo|Africa
Malawi|Lilongwe|Africa
Malaysia|Kuala Lumpur|Asia
Maldives|Malé|Asia
Mali|Bamako|Africa
Malta|Valletta|Europe
Marshall Islands|Majuro|Oceania
Mauritania|Nouakchott|Africa
Mauritius|Port Louis|Africa
Mexico|Mexico City|North America
Micronesia|Palikir|Oceania
Moldova|Chișinău|Europe
Monaco|Monaco|Europe
Mongolia|Ulaanbaatar|Asia
Montenegro|Podgorica|Europe
Morocco|Rabat|Africa
Mozambique|Maputo|Africa
Myanmar|Naypyidaw|Asia
Namibia|Windhoek|Africa
Nauru|Yaren|Oceania
Nepal|Kathmandu|Asia
Netherlands|Amsterdam|Europe
New Zealand|Wellington|Oceania
Nicaragua|Managua|North America
Niger|Niamey|Africa
Nigeria|Abuja|Africa
North Korea|Pyongyang|Asia
North Macedonia|Skopje|Europe
Norway|Oslo|Europe
Oman|Muscat|Asia
Pakistan|Islamabad|Asia
Palau|Ngerulmud|Oceania
Panama|Panama City|North America
Papua New Guinea|Port Moresby|Oceania
Paraguay|Asunción|South America
Peru|Lima|South America
Philippines|Manila|Asia
Poland|Warsaw|Europe
Portugal|Lisbon|Europe
Qatar|Doha|Asia
Romania|Bucharest|Europe
Russia|Moscow|Europe
Rwanda|Kigali|Africa
Saint Kitts|Basseterre|North America
Saint Lucia|Castries|North America
Saint Vincent|Kingstown|North America
Samoa|Apia|Oceania
San Marino|San Marino|Europe
Sao Tome and Príncipe|Sao Tome|Africa
Saudi Arabia|Riyadh|Asia
Senegal|Dakar|Africa
Serbia|Belgrade|Europe
Seychelles|Victoria|Africa
Sierra Leone|Freetown|Africa
Singapore|Singapore|Asia
Slovakia|Bratislava|Europe
Slovenia|Ljubljana|Europe
Solomon Islands|Honiara|Oceania
Somalia|Mogadishu|Africa
South Africa|Pretoria|Africa
South Korea|Seoul|Asia
South Sudan|Juba|Africa
Spain|Madrid|Europe
Sri Lanka|Kotte|Asia
Sudan|Khartoum|Africa
Suriname|Paramaribo|South America
Sweden|Stockholm|Europe
Switzerland|Bern|Europe
Syria|Damascus|Asia
Tajikistan|Dushanbe|Asia
Tanzania|Dodoma|Africa
Thailand|Bangkok|Asia
Timor-Leste|Dili|Asia
Togo|Lomé|Africa
Tonga|Nuku'alofa|Oceania
Trinidad and Tobago|Port of Spain|North America
Tunisia|Tunis|Africa
Türkiye|Ankara|Asia
Turkmenistan|Ashgabat|Asia
Tuvalu|Funafuti|Oceania
Uganda|Kampala|Africa
Ukraine|Kyiv|Europe
United Arab Emirates|Abu Dhabi|Asia
United Kingdom|London|Europe
United States|Washington D.C|North America
Uruguay|Montevideo|South America
Uzbekistan|Tashkent|Asia
Vanuatu|Port Vila|Oceania
Venezuela|Caracas|South America
Vietnam|Hanoi|Asia
Yemen|Sana'a|Asia
Zambia|Lusaka|Africa
Zimbabwe|Harare|Africa
The Vatican|Vatican City|Europe
Palestine|Ramallah|Asia
"""

# -----------------------------------------------------------------------------
# List of all selectable continents for filtering.
# Used to drive the sidebar multiselect when playing "By continent".
# -----------------------------------------------------------------------------
CONTINENTS = ["Africa", "Asia", "Europe", "North America", "South America", "Oceania"]

# -----------------------------------------------------------------------------
# parse_raw(raw: str) -> list[(country, capital, continent)]
#   - Splits the RAW block into lines, then each line into 3 parts.
#   - Skips malformed lines.
#   - Deduplicates exact triplets via the 'seen' set to avoid double entries.
#   - Returns a list of tuples for fast, index-based access later.
# -----------------------------------------------------------------------------
def parse_raw(raw: str):
    rows, seen = [], set()
    for line in raw.strip().splitlines():
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 3:
            continue
        key = tuple(parts)
        if key in seen:
            continue
        seen.add(key)
        rows.append(tuple(parts))  # (country, capital, continent)
    return rows

# -----------------------------------------------------------------------------
# DATA_ALL holds the canonical dataset for the session.
# All filtering uses this immutable list as source-of-truth.
# -----------------------------------------------------------------------------
DATA_ALL = parse_raw(RAW)

# -----------------------------
# Helpers
# -----------------------------
# normalize(s): makes comparing user input to answers accent/space/case tolerant.
#   - NFKD decomposes diacritics (e.g., "São" -> "São"), then combining marks
#     are stripped so "São" ~ "Sao".
#   - Lowercases and keeps only alphanumeric + spaces to avoid punctuation issues.
# is_close_guess(guess, answer, cutoff):
#   - Returns True if normalized guess matches normalized answer exactly,
#     or if difflib.get_close_matches says it is similar enough (>= cutoff).
#   - We use a strict cutoff (0.92) for "correct" and a looser one (0.75)
#     to drive the "So close!" hint.
def normalize(s: str) -> str:
    if not isinstance(s, str):
        return ""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return "".join(ch for ch in s.lower().strip() if ch.isalnum() or ch.isspace())

def is_close_guess(guess: str, answer: str, cutoff: float = 0.8) -> bool:
    g, a = normalize(guess), normalize(answer)
    if g == a:
        return True
    return bool(get_close_matches(g, [a], n=1, cutoff=cutoff))

# -----------------------------
# Session State
# -----------------------------
# We alias st.session_state to 'ss' for brevity.
# Using setdefault creates keys if absent while preserving existing values after reruns.
# Keys:
#   - started:        whether a game is in progress
#   - mode:           direction of question ("Country → Capital" or reverse)
#   - locked_mode:    snapshot of mode at game start so player can't change mid-game
#   - index:          current question index into 'order'
#   - score:          number of correctly answered questions
#   - history:        list of (prompt, guess, correct?, answer) for review
#   - order:          list of integer indices pointing into the *filtered* rows
#   - active_filter:  current region selection in the UI before game starts
#   - locked_filter:  snapshot of region(s) at game start; used for consistent run
#   - shuffle:        whether to shuffle questions when starting a new game
ss = st.session_state
ss.setdefault("started", False)
ss.setdefault("mode", "Country → Capital")
ss.setdefault("locked_mode", None)
ss.setdefault("index", 0)
ss.setdefault("score", 0)
ss.setdefault("history", [])
ss.setdefault("order", [])             # list of indices into filtered rows
ss.setdefault("active_filter", ["Whole world"])
ss.setdefault("locked_filter", None)   # locked regions after start
ss.setdefault("shuffle", True)

# -----------------------------
# Sidebar (Setup + Score)
# -----------------------------
# Top-of-page title & caption.
# The sidebar provides:
#   - Region scope selection (Whole world vs By continent)
#   - Mode selection (locked once the game starts)
#   - Shuffle toggle (applies to the next "new game")
#   - Live score and counters
#   - "Reset game" button (clears progress and reruns)
st.title("🌊 Waves Capitals Quiz")
st.caption("How well do you know the capital cities of the world?")

with st.sidebar:
    st.header("Setup")

    # Region selection:
    #   - Before a game starts, allow the player to pick "Whole world" or choose continents.
    #   - After a game starts, show a read-only summary ("locked regions").
    if not ss.started:
        region = st.radio(
            "Play scope",
            ["Whole world", "By continent"],
            index=0 if ss.active_filter == ["Whole world"] else 1,
        )
        if region == "By continent":
            sel = st.multiselect(
                "Continents",
                CONTINENTS,
                default=(ss.active_filter if ss.active_filter != ["Whole world"] else ["Europe"]),
            )
            # If nothing selected, default to Europe so the game always has data.
            ss.active_filter = sel or ["Europe"]
        else:
            ss.active_filter = ["Whole world"]
    else:
        # During a game, prevent changes that would desync the planned question order.
        locked = ss.locked_filter or ss.active_filter
        st.caption("Regions locked for this game:")
        st.write(", ".join(locked if isinstance(locked, list) else [locked]))

    # Mode selection (locked after start to keep question/answer consistency).
    if not ss.started:
        ss.mode = st.radio(
            "Mode",
            ["Country → Capital", "Capital → Country"],
            index=0 if ss.mode == "Country → Capital" else 1,
        )
    else:
        st.radio(
            "Mode",
            ["Country → Capital", "Capital → Country"],
            index=0 if (ss.locked_mode or ss.mode) == "Country → Capital" else 1,
            disabled=True,
        )
        st.caption(f"Mode locked: **{ss.locked_mode or ss.mode}**")

    # Shuffle toggle (only affects a future new game).
    if not ss.started:
        ss.shuffle = st.toggle("Shuffle order on new game", value=ss.shuffle)
    else:
        st.toggle("Shuffle order on new game", value=ss.shuffle, disabled=True)

    st.markdown("---")

    # ---- Score / Counters (works during game) ----
    # Shows either:
    #   - live counters (if a game is in progress and order is built)
    #   - or the "planned total questions" for the current selection
    st.subheader("Score")
    # Determine total questions planned (if order exists, use it; else compute prospective)
    if ss.started and ss.order:
        total = len(ss.order)
        asked_completed = min(ss.index, total)           # completed questions
        current_q = min(ss.index + 1, total)             # current question number (1-based)
        st.write(f"Questions: **{asked_completed}** / {total}")
        st.write(f"Score: **{ss.score}** / {total}")
    else:
        # Before starting, estimate how many questions the chosen filter will yield.
        planned_total = len(DATA_ALL) if ss.active_filter == ["Whole world"] else len(
            [r for r in DATA_ALL if r[2] in set(ss.active_filter)]
        )
        st.write(f"Questions: **{planned_total}**")

    st.markdown("---")
    # Reset clears the game-specific keys and reruns the script from the top.
    if st.button("🔁 Reset game", type="secondary"):
        for k in ["started","locked_mode","index","score","history","order","locked_filter"]:
            ss.pop(k, None)
        st.rerun()

# Visual separator between header and game content.
st.write("---")

# -----------------------------
# Filtering + Order
# -----------------------------
# filtered_rows(active_filter):
#   - Returns a subset of DATA_ALL based on selected continent(s), or the whole list.
def filtered_rows(active_filter):
    if active_filter == ["Whole world"]:
        return DATA_ALL
    allowed = set(active_filter)
    return [r for r in DATA_ALL if r[2] in allowed]

# ensure_order_built():
#   - Called right before starting a game.
#   - Locks the filter selection (so later UI changes can't affect this run).
#   - Builds the 'order' as a list of integer indices into the filtered rows.
#   - Optionally shuffles those indices for a randomized quiz.
#   - Resets progress counters (index, score, history).
def ensure_order_built():
    if ss.order:
        return
    ss.locked_filter = ss.active_filter
    rows = filtered_rows(ss.locked_filter)
    idx = list(range(len(rows)))
    if ss.shuffle:
        random.shuffle(idx)
    ss.order = idx
    ss.index = 0
    ss.score = 0
    ss.history = []

# -----------------------------
# Game flow
# -----------------------------
# The script renders one question per run.
# Streamlit re-executes top-to-bottom on every interaction, so we:
#   - keep persistent variables in st.session_state
#   - gate logic on ss.started and ss.index
#   - use st.form so typing doesn't submit on every keystroke
#   - use st.rerun() after advancing to the next question to refresh the UI
if not ss.started:
    # Pre-game screen: the user sets options and starts the quiz.
    st.info("Choose mode and region(s), then click **Start new game**.")
    if st.button("🚀 Start new game", type="primary"):
        ensure_order_built()
        ss.started = True
        ss.locked_mode = ss.mode
        st.rerun()
else:
    # In-game: render either the completion screen or the current question.
    rows = filtered_rows(ss.locked_filter or ss.active_filter)
    if not rows:
        # Defensive guard: in practice this shouldn't happen because we lock filters.
        st.warning("No countries found for that selection.")
    elif ss.index >= len(ss.order):
        # Finished all planned questions.
        st.success(f"All done! Final score: **{ss.score} / {len(ss.order)}**")
        # Show an expandable review of the entire attempt using the history log.
        with st.expander("Review answers"):
            for q, g, ok, ans in ss.history:
                icon = "✅" if ok else "❌"
                st.write(f"{icon} **{q}** → {g} → **{ans}**")
    else:
        # Retrieve the current (country, capital, continent) from the filtered dataset
        # using the integer index stored in ss.order[ss.index].
        country, capital, continent = rows[ss.order[ss.index]]

        # Decide which side is the prompt vs the expected answer based on locked mode.
        mode = ss.locked_mode or ss.mode
        if mode == "Country → Capital":
            prompt = f"({continent}) What's the capital of **{country}**?"
            correct = capital
        else:
            prompt = f"({continent}) **{capital}** is the capital of which country?"
            correct = country

        # The question header shows a 1-based question number.
        st.subheader(f"Question {ss.index + 1}")
        st.write(prompt)

        # Use a form so "Enter" or clicking the button triggers a single submission,
        # not a submit on every keypress. The key includes ss.index to ensure each
        # question has a distinct form identity across reruns.
        with st.form(key=f"q{ss.index}"):
            guess = st.text_input("Your answer:", "")
            submitted = st.form_submit_button("Submit")

        # Handle a submitted guess:
        #   - If the guess is "close enough" at a strict cutoff (0.92), count it correct.
        #   - Otherwise, if it's just "near" (>=0.75), show a softer warning.
        #   - Append the attempt (prompt, guess, ok, answer) to history for review pane.
        #   - On correct or give-up, advance index, show a toast, pause briefly, rerun.
        if submitted:
            if is_close_guess(guess, correct, cutoff=0.92):
                ss.score += 1
                ss.history.append((prompt, guess, True, correct))
                st.balloons()  # fun confetti animation
                st.success(f"🎉 Correct! **{correct}**")
                st.toast("✅ Moving to next question...", icon="✅")
                time.sleep(3.0)  # small UX pause so the user can read feedback
                ss.index += 1
                st.rerun()
            else:
                near = is_close_guess(guess, correct, cutoff=0.75)
                st.warning("So close!" if near else "Not quite, try again.")
                ss.history.append((prompt, guess, False, correct))

        # "Give Up" lets the user skip the current question without scoring.
        # We still store the correct answer in history for later review.
        if st.button("Give Up 🛑", type="secondary"):
            ss.history.append((prompt, "(gave up)", False, correct))
            st.error(f"❌ Gave up! The answer was **{correct}**")
            st.toast("❌ Moving on...", icon="❌")
            time.sleep(3.0)  # brief pause for readability
            ss.index += 1
            st.rerun()
