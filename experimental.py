from dotenv import load_dotenv
import os
import anthropic


load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("CLAUDE_API_KEY"))


def estimate_tokens(text):
    return int(len(text) / 4)

def summarize_transcript(text):
    prompt = f"""You are a helpful assistant.

Given the following meeting transcript, identify the 3 most important topics or decisions discussed.

For each topic:
• Provide a clear and concise headline summarizing the main idea.
• Include 2–4 supporting bullet points that summarize relevant details, decisions, or action items.

Format your response like this:

Headline 1:

- Bullet point

- Bullet point

Headline 2:

- Bullet point

- Bullet point

Headline 3:

- Bullet point

- Bullet point

Here's the transcript:

{text}"""

    response = client.messages.create(
        model="claude-opus-4-20250514",  
        max_tokens=1024,
        temperature=0.3,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.content[0].text


with open("combined_transcripts/2025_05_12_to_2025_05_16_combined.txt", "r", encoding="utf-8") as f:
    transcript = f.read()

print(estimate_tokens(transcript))

summary = summarize_transcript(transcript)

with open("report_opus.txt", "w", encoding="utf-8") as f:
    f.write(summary)

print(summary)

