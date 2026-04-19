from tracker import check_visibility, calculate_score
from storage import save_results, load_yesterday, load_today
from alerts import check_for_changes

brand = "Notion"
category = "project management tools"

print(f"Checking AI visibility for: {brand}")
print(f"Category: {category}")
print("=" * 50)
print()

# Check if already run today
existing = load_today()
if existing:
    print("Already ran today. Using saved results.")
    today_score = existing["score"]
else:
    results = check_visibility(brand, category)
    today_score, mentions, total = calculate_score(results)
    save_results(brand, category, today_score, results)
    print()
    print(f"Visibility Score: {today_score}%  ({mentions} out of {total})")
    print()

print("=" * 50)
print("CHANGE DETECTION")
print("=" * 50)

yesterday_data = load_yesterday()
check_for_changes(brand, today_score, yesterday_data)