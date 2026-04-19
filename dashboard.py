import streamlit as st
import json
import os
from datetime import date, timedelta
from tracker import check_visibility, calculate_score
from storage import save_results, load_today, load_yesterday
from alerts import check_for_changes

st.set_page_config(
    page_title="GEO Visibility Tracker",
    page_icon="🔍",
    layout="centered"
)

st.title("🔍 GEO Visibility Tracker")
st.caption("Track how often AI mentions your brand — built to understand Writesonic's core problem")

st.divider()

# --- Inputs ---
col1, col2 = st.columns(2)
with col1:
    brand = st.text_input("Brand name", value="Notion")
with col2:
    category = st.text_input("Category", value="project management tools")

competitor = st.text_input("Competitor to compare (optional)", placeholder="e.g. Asana")

run = st.button("Check AI Visibility", type="primary")

st.divider()

# --- Run tracker ---
if run:
    if not brand or not category:
        st.warning("Please enter a brand name and category.")
    else:
        with st.spinner(f"Asking AI 5 questions about '{brand}'..."):
            results = check_visibility(brand, category)
            score, mentions, total = calculate_score(results)
            save_results(brand, category, score, results)

        # Score display
        st.subheader("Today's Visibility Score")
        col1, col2, col3 = st.columns(3)
        col1.metric("Score", f"{score}%")
        col2.metric("Mentioned", f"{mentions}/{total} queries")

        yesterday = load_yesterday()
        if yesterday and yesterday["brand"] == brand:
            delta = score - yesterday["score"]
            col3.metric("vs Yesterday", f"{delta:+}%",
                delta_color="normal")
        else:
            col3.metric("vs Yesterday", "First run")

        st.divider()

        # --- Trend chart ---
        st.subheader("Score Trend (Last 7 Days)")

        scores_by_date = {}
        for i in range(7):
            day = str(date.today() - timedelta(days=i))
            filepath = os.path.join("results", f"{day}.json")
            if os.path.exists(filepath):
                with open(filepath) as f:
                    data = json.load(f)
                    if data.get("brand") == brand:
                        scores_by_date[day] = data["score"]

        if len(scores_by_date) > 1:
            sorted_dates = sorted(scores_by_date.keys())
            chart_data = {
                "Date": sorted_dates,
                "Score": [scores_by_date[d] for d in sorted_dates]
            }
            import pandas as pd
            df = pd.DataFrame(chart_data).set_index("Date")
            st.line_chart(df)
        else:
            st.info("Run the tracker daily to see your trend chart build up over time.")

        st.divider()

        # --- Query breakdown ---
        st.subheader("Query Breakdown")
        for i, r in enumerate(results, 1):
            icon = "✅" if r["mentioned"] else "❌"
            st.write(f"{icon} **Query {i}:** {r['query']}")
            with st.expander("See full AI answer"):
                st.write(r["answer"])

        st.divider()

        # --- Competitor comparison ---
        if competitor:
            st.subheader(f"Competitor Comparison: {brand} vs {competitor}")
            with st.spinner(f"Checking '{competitor}'..."):
                comp_results = check_visibility(competitor, category)
                comp_score, comp_mentions, _ = calculate_score(comp_results)

            col1, col2 = st.columns(2)
            col1.metric(brand, f"{score}%")
            col2.metric(competitor, f"{comp_score}%",
                delta=f"{score - comp_score:+}% vs competitor")

            if score > comp_score:
                st.success(f"'{brand}' is MORE visible than '{competitor}' in AI answers!")
            elif score < comp_score:
                st.warning(f"'{competitor}' is MORE visible than '{brand}' — action needed!")
            else:
                st.info("Both brands have equal AI visibility.")

        st.divider()

        # --- Alert ---
        st.subheader("Change Alert")
        if yesterday and yesterday["brand"] == brand:
            check_for_changes(brand, score, yesterday)
        else:
            st.info("No previous data to compare. Run daily to activate alerts.")