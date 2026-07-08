from flask import Flask, request, jsonify
import boto3
import json

app = Flask(__name__) # creates the Flask web server 

def classify(sender, subject, body):

    # creating a connection to bedrock / an object that knows how to communicate with bedrock
    bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")
    
    # This is your prompt — notice the f before the triple quotes
    # That makes it an f-string so {sender}, {subject}, {body} get filled in automatically
    prompt = f"""You are an executive email assistant. Your job is to classify every email into exactly one of these categories.

                    Definitions:

                    Important:
                        - Requires action, approval, review, signature, or a reply — even if not time-sensitive.
                        - Time-sensitive or has a deadline.
                        - Legal, financial, investment, board, contract, client, or executive communication.
                        - High-priority project updates or decisions.
                        - A direct question or specific request from a colleague, client, or partner that 
                        warrants a response in the near future.

                    Normal:
                        - Legitimate work-related email that does not require a response.
                        - One-way communication: general updates, reports, confirmations, newsletters, 
                        or FYI messages from coworkers, clients, or business partners.
                        - Useful context or information that requires no action or reply.

                    Noise:
                        - Marketing or promotional emails.
                        - Newsletters.
                        - Advertisements.
                        - Social media notifications.
                        - Automated reminders unrelated to the recipient's work or 
                        registered commitments.
                        - Generic announcements.
                        - Sales emails.
                        - Messages that can safely be ignored without affecting work.
                        - NOTE: Reminders for events, appointments, or services the 
                        recipient has registered for are NOT noise — classify as Normal.

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


# tells FLask to listen for POST requests at the address /classify
@app.route("/classify", methods=["POST"])

# function that runs when a request arrives 
def classify_email():
    # request object represents the incoming HTTP request 
    data = request.get_json() # data now is a Python dictonary since it got the JSON that was sent in the request

    # extracting values from key-value records in data
    sender = data["sender"]
    subject = data["subject"]
    body = data["body"]

    # calling our classify function
    result = classify(sender, subject, body)

    return jsonify({"result": result}) # converting Python dictionary into a JSON file

# this tells Falsk to start the web server when we run this file
if __name__ == "__main__":
    app.run(debug=True)
