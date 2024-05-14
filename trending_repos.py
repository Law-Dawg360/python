import requests
from datetime import datetime

def fetch_trending_repos():
    url = "https://api.github.com/search/repositories"
    params = {
        "q": "created:>2022-01-01",
        "sort": "stars",
        "order": "desc",
        "per_page": 5  # You can adjust the number of repositories to fetch
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()["items"]
    else:
        return None

def main():
    trending_repos = fetch_trending_repos()
    if trending_repos:
        with open("trending_repos.md", "w") as f:
            f.write("# Trending Repositories\n")
            f.write("This list was generated on {}.\n\n".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            for repo in trending_repos:
                f.write("- [{}]({}) - {}\n".format(repo["name"], repo["html_url"], repo["description"]))
    else:
        print("Failed to fetch trending repositories.")

if __name__ == "__main__":
    main()
