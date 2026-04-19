def check_for_changes(brand, today_score, yesterday_data):

    if yesterday_data is None:
        print("No previous data found — this is your first run!")
        print(f"Today's score saved: {today_score}%")
        return

    yesterday_score = yesterday_data["score"]
    difference = today_score - yesterday_score

    print(f"Today's score:     {today_score}%")
    print(f"Yesterday's score: {yesterday_score}%")
    print()

    if difference == 0:
        print(f"No change — '{brand}' visibility is stable at {today_score}%")

    elif difference > 0:
        print(f"GOOD — '{brand}' visibility INCREASED by {difference}%!")

    elif difference <= -20:
        print(f"ALERT — '{brand}' visibility DROPPED by {abs(difference)}%!")
        print("Action needed: check what changed in AI answers")

    else:
        print(f"WARNING — '{brand}' visibility dropped slightly by {abs(difference)}%")