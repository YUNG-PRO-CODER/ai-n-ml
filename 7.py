import requests

def getRandomJokes():
    url = "https://official-joke-api.appspot.com/random_joke"
    response = requests.get(url)
    if response.status_code == 200:
        print(f"Full JSON response {response.json()}")
        joke_data = response.json()
        return f"{joke_data['setup']} - {joke_data['punchline']}"
    else:
        return "failed to retrive the joke"
        
def main():
    print("Welcome to Random Joke Generator")

    while True:
        userInput = input(f"Press Enter to get the new joke, or type 'q'/'exit' to quit").strip().lower()
        if userInput in ("q", "exit"):
            print("Goodbye")
            exit()
        joke = getRandomJokes()
        print(joke)

if __name__ == "__main__":
    main()