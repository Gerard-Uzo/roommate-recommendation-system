# generate_data.py
import pandas as pd
import numpy as np

# 1. Set a random seed so our results are consistent every time we run it
np.random.seed(42)

# 2. Let's generate 500 students to give our model plenty of data
num_students = 500

# 3. Build the dataset with Hard Constraints AND Personality Features
data = {
    "StudentID": range(1, num_students + 1),
    # Hard Constraints (Used for filtering)
    "Gender": np.random.choice(["Male", "Female"], num_students),
    "Smoker": np.random.choice(
        ["Yes", "No"], num_students, p=[0.05, 0.95]
    ),  # 5% smokers
    # Personality Features (Scale of 1 to 5, used for K-Means)
    "Sleep_Schedule": np.random.choice(
        [1, 2, 3, 4, 5], num_students
    ),  # 1: Early, 5: Night Owl
    "Study_Habit": np.random.choice(
        [1, 2, 3, 4, 5], num_students
    ),  # 1: Silent, 5: Loud
    "Cleanliness": np.random.choice(
        [1, 2, 3, 4, 5], num_students
    ),  # 1: Messy, 5: Spotless
    "Social_Personality": np.random.choice(
        [1, 2, 3, 4, 5], num_students
    ),  # 1: Introvert, 5: Extrovert
    "Visitor_Frequency": np.random.choice(
        [1, 2, 3, 4, 5], num_students
    ),  # 1: Never, 5: Always
}

# 4. Convert to a DataFrame and save
df = pd.DataFrame(data)
df.to_csv("data/enhanced_hostel_data.csv", index=False)

print(
    f"Successfully generated {num_students} student profiles with realistic constraints!"
)
