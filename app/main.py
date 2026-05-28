import plotly.graph_objects as go
import streamlit as st
import pandas as pd

# 1. Page Configuration
st.set_page_config(page_title="Hostel Match AI", page_icon="🏫", layout="wide")

st.title("🏫 Intelligent Hostel Roommate Recommendation System")
st.markdown(
    "Adjust the sliders on the left to input your lifestyle preferences and find your perfect roommate match."
)


# 2. Load the Clustered Data
# We use st.cache_data so the app doesn't reload the file every time a slider moves
@st.cache_data
def load_data():
    return pd.read_csv("data/male_students_clustered.csv")


df = load_data()

# 3. Build the Sidebar (User Input)
st.sidebar.header("Your Lifestyle Profile")
sleep_val = st.sidebar.slider("Sleep Schedule (1=Early, 5=Night Owl)", 1, 5, 3)
study_val = st.sidebar.slider("Study Habit (1=Silent, 5=Loud Music)", 1, 5, 3)
clean_val = st.sidebar.slider("Cleanliness (1=Messy, 5=Spotless)", 1, 5, 3)
social_val = st.sidebar.slider("Social Personality (1=Introvert, 5=Extrovert)", 1, 5, 3)
visitor_val = st.sidebar.slider("Visitor Frequency (1=Never, 5=Always)", 1, 5, 3)

user_profile = {
    "Sleep_Schedule": sleep_val,
    "Study_Habit": study_val,
    "Cleanliness": clean_val,
    "Social_Personality": social_val,
    "Visitor_Frequency": visitor_val,
}


# 4. The Compatibility Engine (Adapted for the Web App)
def get_match_score(user, row):
    sleep_diff = abs(user["Sleep_Schedule"] - row["Sleep_Schedule"])
    clean_diff = abs(user["Cleanliness"] - row["Cleanliness"])
    study_diff = abs(user["Study_Habit"] - row["Study_Habit"])
    social_diff = abs(user["Social_Personality"] - row["Social_Personality"])
    visitor_diff = abs(user["Visitor_Frequency"] - row["Visitor_Frequency"])

    weighted_penalty = (
        (sleep_diff * 1.5)
        + (clean_diff * 1.5)
        + (study_diff * 1.0)
        + (social_diff * 0.5)
        + (visitor_diff * 0.5)
    )
    score = max(0, 100 - ((weighted_penalty / 20) * 100))
    return round(score, 1)


# 5. Calculate scores for every student in the database
# We apply the engine to every row and save it in a new column
df["Compatibility_Score"] = df.apply(
    lambda row: get_match_score(user_profile, row), axis=1
)

# 6. Sort by highest score to find the Top 3 Matches
top_matches = df.sort_values(by="Compatibility_Score", ascending=False).head(3)

# 7. Display the Results nicely
st.subheader("🏆 Your Top 3 Roommate Matches")

# Create 3 columns for a clean UI layout
col1, col2, col3 = st.columns(3)

# Display Match 1
with col1:
    st.success(f"🥇 Match #1: Student {top_matches.iloc[0]['StudentID']}")
    st.metric(
        label="Compatibility Score",
        value=f"{top_matches.iloc[0]['Compatibility_Score']}%",
    )
    st.write(f"**Assigned Hostel Persona (Cluster):** {top_matches.iloc[0]['Cluster']}")

# Display Match 2
with col2:
    st.info(f"🥈 Match #2: Student {top_matches.iloc[1]['StudentID']}")
    st.metric(
        label="Compatibility Score",
        value=f"{top_matches.iloc[1]['Compatibility_Score']}%",
    )
    st.write(f"**Assigned Hostel Persona (Cluster):** {top_matches.iloc[1]['Cluster']}")

# Display Match 3
with col3:
    st.warning(f"🥉 Match #3: Student {top_matches.iloc[2]['StudentID']}")
    st.metric(
        label="Compatibility Score",
        value=f"{top_matches.iloc[2]['Compatibility_Score']}%",
    )
    st.write(f"**Assigned Hostel Persona (Cluster):** {top_matches.iloc[2]['Cluster']}")

# --- BAR CHART VISUALIZATION (Better UX) ---
st.write("---")
st.subheader("📊 Lifestyle Comparison: You vs. Top Match")

best_match = top_matches.iloc[0]
categories = [
    "Sleep Schedule",
    "Study Habit",
    "Cleanliness",
    "Social Personality",
    "Visitor Frequency",
]

user_scores = [
    user_profile["Sleep_Schedule"],
    user_profile["Study_Habit"],
    user_profile["Cleanliness"],
    user_profile["Social_Personality"],
    user_profile["Visitor_Frequency"],
]
match_scores = [
    best_match["Sleep_Schedule"],
    best_match["Study_Habit"],
    best_match["Cleanliness"],
    best_match["Social_Personality"],
    best_match["Visitor_Frequency"],
]

# Create a Grouped Bar Chart
fig = go.Figure(
    data=[
        go.Bar(
            name="Your Profile", x=categories, y=user_scores, marker_color="royalblue"
        ),
        go.Bar(
            name=f"Student {best_match['StudentID']}'s Profile",
            x=categories,
            y=match_scores,
            marker_color="darkorange",
        ),
    ]
)

# Format the layout
fig.update_layout(
    barmode="group",
    yaxis=dict(title="Score (1 to 5)", range=[0, 5.5]),
    margin=dict(l=40, r=40, t=40, b=40),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
)

st.plotly_chart(fig, use_container_width=True)

st.divider()
st.write("🎓 *System built by Uzodinma Gerard | Powered by K-Means Clustering*")
