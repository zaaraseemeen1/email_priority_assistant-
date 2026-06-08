import csv

important = ["urgent", "sign", "contract", "review", "board meeting", "NDA", "introduction", "allocation", "deadline", "approval", "action required"]

noise = ["newsletter", "webinar", "invoice", "prize", "click here", "daily summary", "morning note", "unsubscribe", "reminder", "deals", "unsubscribe", "click here", "notification", "viewed your profile", "weekly", "browse"]

sender_domains = ["ir@blackrock.com", "s.mitchell@granthamlaw.com", "chen@alphaventures.vc", "boardsec@nexuscorp.com", "legal@oriongroup.com"]

def classify(sender, subject, body):
    # combined subject and body
    comb = (subject + " " + body).lower()

    # is the sender in the important sender's list? ASK ABOUT THIS
    for email in sender_domains:
        if (sender == email):
            return "Important"
        
    # does contain a noise keyword?
    for word in noise:
        if (word in comb):
            return "Noise"
    
    # does contain important keyword?
    for word in important:
        if (word in comb):
            return "Important"
        
    return "Normal"

def main():
    important = 0
    noise = 0
    normal = 0

    # with keyowrd takes care of closing file for me
    with open("inbox.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            result = classify(row["sender_email"],row["subject"], row["body_preview"])
            print(result + " " + row["sender_name"] + " " + row["subject"])
            if (result == "Important"):
                important = important + 1
            elif (result == "Noise"):
                noise = noise +1
            else:
                normal = normal +1 
        
        print(f"Number of emails classified as important: {important}")
        print(f"Number of emails classified as normal: {normal}")
        print(f"Number of emails classified as noise: {noise}")


main()