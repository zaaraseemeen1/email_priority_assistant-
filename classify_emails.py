import csv
import boto3
import json

def classify(sender, subject, body):

    # creating a connection to bedrock / an object that knows how to communicate with bedrock
    bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
    
    # This is your prompt — notice the f before the triple quotes
    # That makes it an f-string so {sender}, {subject}, {body} get filled in automatically
    prompt = f"""You are an executive email assistant. Your job is to classify every email into exactly one of these categories.

                    Definitions:

                    Important:
                    - Requires action, approval, review, signature, or a reply.
                    - Time-sensitive or has a deadline.
                    - Legal, financial, investment, board, contract, client, or executive communication.
                    - High-priority project updates or decisions.

                    Normal:
                    - Legitimate work-related email that does not require immediate action.
                    - General updates from coworkers, clients, or business partners.
                    - Reports, research, confirmations, or conversations that are useful but not urgent.

                    Noise:
                    - Marketing or promotional emails.
                    - Newsletters.
                    - Advertisements.
                    - Social media notifications.
                    - Automated reminders.
                    - Generic announcements.
                    - Sales emails.
                    - Messages that can safely be ignored without affecting work.

                    Email:

                    Sender:
                    {sender}

                    Subject:
                    {subject}

                    Body:
                    {body}

                    Rules:
                    - Choose exactly ONE category.
                    - Reply with only one word.
                    - Valid responses are:
                    Important
                    Normal
                    Noise
                    """

    # actual API call/sends request to Claude
    response = bedrock.invoke_model(
        modelId="us.anthropic.claude-haiku-4-5-20251001-v1:0",
        body=json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 10,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }),
        contentType="application/json", # I'm sending a JSON
        accept="application/json", # provide your answer in a JSON
    )

    result = json.loads(response["body"].read()) # .read() gets the raw JSON text, .loads( ) converts that into a Python dictionary
    return result["content"][0]["text"].strip() 


def main():
    important_count = 0
    noise_count = 0
    normal_count = 0

    # with keyword takes care of closing file for me
    with open("inbox.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            result = classify(row["sender_email"],row["subject"], row["body_preview"])
            print(result + " " + row["sender_name"] + " " + row["subject"])
            if (result == "Important"):
                important_count = important_count + 1
            elif (result == "Noise"):
                noise_count = noise_count +1
            else:
                normal_count = normal_count +1 
        
        print(f"Number of emails classified as important: {important_count}")
        print(f"Number of emails classified as normal: {normal_count}")
        print(f"Number of emails classified as noise: {noise_count}")

main()