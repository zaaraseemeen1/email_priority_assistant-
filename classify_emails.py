import csv

important = ["urgent", "sign", "contract", "review", "board meeting", "NDA", "introduction", "allocation", "deadline", "approval", "action required"]

noise = ["newsletter", "webinar", "invoice", "prize", "click here", "daily summary", "morning note", "reminder", "deals", "unsubscribe", "notification", "viewed your profile", "weekly", "browse"]

sender_domains = ["ir@blackrock.com", "s.mitchell@granthamlaw.com", "d.chen@alphaventures.vc", "boardsec@nexuscorp.com", "legal@oriongroup.com"]

def classify(sender, subject, body):
    # combined subject and body
    comb = (subject + " " + body).lower()

    # is the sender in the important sender's list?
    for email in sender_domains:
        if (sender.lower() == email.lower()):
            return "Important"
    
    # does contain important keyword?
    for word in important:
        if (word in comb):
            return "Important"
        
    # does contain a noise keyword?
    for word in noise:
        if (word in comb):
            return "Noise"
        
    return "Normal"

def main():
    important_count = 0
    noise_count = 0
    normal_count = 0

    # with keyowrd takes care of closing file for me
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