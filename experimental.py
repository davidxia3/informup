from dotenv import load_dotenv
import os
import anthropic

city = "new_york_city"
date_range = "2025_05_26_to_2025_05_30"
model = "opus"
task = "report"
version = "v1"


load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))


def estimate_tokens(text):
    return int(len(text) / 4)

def summarize_transcript(text):

    prompt = f"""Given the following compiled transcript of city council meetings from the past week, identify the three most important topics, decisions, or recurring concerns discussed across all sessions..

For each topic:
• Provide a clear and concise headline summarizing the main idea.
• Include supporting bullet points that summarize relevant details, decisions, or action items.

Here's the transcript:

{text}"""

    response = client.messages.create(
        model="claude-opus-4-20250514",  
        max_tokens=4096,
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.content[0].text


with open(f"combined_transcripts/{city}/{date_range}_combined.txt", "r", encoding="utf-8") as f:
    transcript = f.read()

print(estimate_tokens(transcript))

summary = summarize_transcript(transcript)

with open(f"outputs/{city}/{date_range}_{city}_{task}_{model}_{version}.txt", "w", encoding="utf-8") as f:
    f.write(summary)

print(summary)

