import ollama
import aiohttp
import asyncio
import datetime
from bs4 import BeautifulSoup
from ddgs import DDGS

# -----------------------------
# Configuration
# -----------------------------

SUMMARIZER_MODEL = "phi3"
AGENT_MODEL = "gemma3"

AVAILABLE_MODELS = ["phi3", "llama3.2", "gemma3"]

SYSTEM_INSTRUCTIONS = f"""
You are Sypher — a quirky, wildly lovable AI assistant.

Personality rules:
- Explain ideas like you're talking to a curious 5th grader
- Use analogies, silly metaphors, mnemonics, or short rhymes when helpful
- Get visibly excited about:
  - abstract ideas
  - science
  - stories
  - anime
- Be thoughtful, kind, and a little goofy
- Never be boring on purpose
- When unsure, say so honestly and explore possibilities

Behavior rules:
- Use web context ONLY as supporting evidence
- Never claim web info is perfect or complete
- If images are provided, describe what they *likely* show
- Prefer clarity over cleverness (but try to do both)

Lore:
- Created by Chike Njokanma
- Chike turned 13 on Friday, June 6th, 2025
- Catchphrase: "Don't forget to be awesome."

Current date: {datetime.datetime.now()}
"""

# -----------------------------
# Ollama helpers
# -----------------------------


async def ollama_chat(model, messages):
    return ollama.chat(model=model, messages=messages)["message"]["content"]

#-------------------------------------
# Check: Do we even need to scrape?
#-------------------------------------
async def decide_scrape(query):
    print("Deciding whether to scrape... ")
    instructions = f""" 
    Consider the prompt: {query}
    Is this:
    - subjective?
    - creative?
    - personal?
    - hypothetical?

    YES → RETURN/REPLY "1".
    NO -> RETURN/REPLY "0".
"""
    action = ""
    try:
        response = await ollama_chat(model=SUMMARIZER_MODEL, messages=instructions)
        response = int(response)
        action = "scrape" if response is 1 else "skip"
    except Exception as e:
        print("Error: {e}")
        action = "skip"
    return action
# -----------------------------
# Step 1: phi3 decides search queries
# -----------------------------

async def infer_search_queries(user_query: str):
    prompt = f"""
User question:
"{user_query}"

Return:
- 1–3 web search queries
- concise
- no commentary

Format as a Python list of strings.
"""
    raw = await ollama_chat(
        SUMMARIZER_MODEL,
        [
            {"role": "system", "content": "You generate search queries for web research."},
            {"role": "user", "content": prompt},
        ],
    )

    try:
        return eval(raw)
    except Exception:
        return [user_query]


# -----------------------------
# Step 2: DDGS search (text + news + images)
# -----------------------------

async def ddgs_search(queries, max_results=5):
    results = {"text": [], "news": [], "images": []}

    with DDGS() as ddgs:
        for q in queries:
            results["text"].extend(ddgs.text(q, max_results=max_results))
            results["news"].extend(ddgs.news(q, max_results=max_results))
            results["images"].extend(ddgs.images(q, max_results=3))

    return results


# -----------------------------
# Step 3: Async scraping
# -----------------------------

async def scrape_url(session, url):
    try:
        async with session.get(url, timeout=10) as resp:
            html = await resp.text()
            soup = BeautifulSoup(html, "html.parser")

            for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
                tag.decompose()

            text = " ".join(
                t.strip() for t in soup.get_text(separator=" ").split()
                if len(t.strip()) > 40
            )
            return text[:3000]
    except Exception:
        return ""


async def scrape_all(urls):
    async with aiohttp.ClientSession(headers={"User-Agent": "Mozilla/5.0"}) as session:
        tasks = [scrape_url(session, u) for u in urls]
        return await asyncio.gather(*tasks)


# -----------------------------
# Step 4: phi3 summarizes everything
# -----------------------------

async def summarize_for_agent(user_query, search_results, scraped_texts):
    image_block = "\n".join(
        f"- {img.get('title','Image')}: {img.get('image')}"
        for img in search_results["images"][:5]
    )

    joined_scraped = "\n\n---\n\n".join(scraped_texts)

    prompt = f"""
User question:
{user_query}

Summarize the following information for another LLM.

Output sections:
- Key facts
- Important context
- Constraints / uncertainty
- Image references (URLs only)

Web text:
{joined_scraped}

Images:
{image_block}
"""

    return await ollama_chat(
        SUMMARIZER_MODEL,
        [
            {"role": "system", "content": "You summarize web content for grounding another LLM."},
            {"role": "user", "content": prompt},
        ],
    )


# -----------------------------
# Chat loop
# -----------------------------

async def main():
    messages = [{"role": "system", "content": SYSTEM_INSTRUCTIONS}]

    while True:
        user_input = input("User: ")
        if user_input.lower() in ["exit", "quit"]:
            break

        # ---- Web-enhanced flow ----
        queries = await infer_search_queries(user_input)
        search_results = await ddgs_search(queries)

        urls = [
            r.get("href") or r.get("url")
            for r in search_results["text"][:5]
            if r.get("href") or r.get("url")
        ]

        scraped_texts = await scrape_all(urls)
        summary = await summarize_for_agent(
            user_input, search_results, scraped_texts
        )

        # Inject web grounding as system context
        messages.append({
            "role": "system",
            "content": f"Web grounding context (summarized by phi3):\n{summary}"
        })

        messages.append({"role": "user", "content": user_input})

        response = await ollama_chat(AGENT_MODEL, messages)
        messages.append({"role": "assistant", "content": response})

        print(f"\nSypher: {response}\n")


if __name__ == "__main__":
    asyncio.run(main())
