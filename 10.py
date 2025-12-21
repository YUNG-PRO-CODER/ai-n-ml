import requests

HEADERS = {
    "User-Agent": "MusicTriviaApp/1.0 (school-project)"
}

def fetch_artist(artist):
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{artist.replace(' ', '_')}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        return None
    return response.json()

def ask(question, answer):
    user = input(question + " ").lower()
    if answer.lower() in user:
        print("✅ Correct!\n")
        return 1
    else:
        print(f"❌ Wrong! Correct answer: {answer}\n")
        return 0

def main():
    print("\n🎧 Travis Scott & Playboi Carti Trivia Quiz 🎧\n")
    travis = fetch_artist("Travis Scott")
    carti = fetch_artist("Playboi Carti")
    if travis is None or carti is None:
        print("❌ Could not fetch data from API. Try again later.")
        return
    score = 0

    print("🔥 Travis Scott Section 🔥\n")

    score += ask(
        "1) What is Travis Scott's stage name?",
        travis["title"]
    )
    score += ask(
        "2) Travis Scott is mainly known as a?",
        travis["description"].split(",")[0]
    )
    score += ask(
        "3) Travis Scott is associated with which music genre?",
        "hip hop"
    )
    score += ask(
        "4) Which famous Travis Scott album is mentioned online?",
        "Astroworld"
    )
    score += ask(
        "5) Travis Scott is an American?",
        "rapper"
    )

    print("🧛 Playboi Carti Section 🧛\n")

    score += ask(
        "6) What is Playboi Carti's stage name?",
        carti["title"]
    )
    score += ask(
        "7) Playboi Carti is mainly known as a?",
        carti["description"].split(",")[0]
    )
    score += ask(
        "8) Playboi Carti is associated with which music genre?",
        "hip hop"
    )
    score += ask(
        "9) Name one famous Playboi Carti album:",
        "Die Lit"
    )
    score += ask(
        "10) Playboi Carti is an American?",
        "rapper"
    )

    print(f"🏆 Final Score: {score}/10")

main()