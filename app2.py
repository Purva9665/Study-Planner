import datetime
import pandas as pd
import requests
from streamlit_calendar import calendar
import streamlit as st
def get_default_subjects(exam_name: str, exam_category: str):
    name = exam_name.lower()
    cat = exam_category.lower()

    # -------- Engineering / Technical entrance --------
    # GATE CS / IT
    if "gate" in name and ("cs" in name or "cse" in name or "computer" in name):
        return [
            "Programming & Data Structures",
            "Algorithms",
            "Operating Systems",
            "Database Management Systems",
            "Computer Networks",
            "Computer Organization & Architecture",
            "Theory of Computation",
            "Digital Logic",
            "Engineering Mathematics",
            "Aptitude",
        ]

    # JEE (engineering entrance)
    if "jee" in name:
        return [
            "Physics",
            "Chemistry",
            "Mathematics",
        ]

    # BITSAT / VITEEE / other engg entrances
    if any(x in name for x in ["bitsat", "viteee"]):
        return [
            "Physics",
            "Chemistry",
            "Mathematics",
            "English / Logical Reasoning",
        ]

    # -------- Medical entrance --------
    if "neet" in name:
        return [
            "Physics",
            "Chemistry",
            "Biology (Botany)",
            "Biology (Zoology)",
        ]

    # -------- Management / MBA --------
    if any(x in name for x in ["cat", "xat", "mat", "snap"]):
        return [
            "Quantitative Aptitude",
            "Logical Reasoning",
            "Data Interpretation",
            "Verbal Ability & RC",
        ]

    if "gmat" in name:
        return [
            "Quantitative Reasoning",
            "Verbal Reasoning",
            "Data Insights",
            "Analytical Writing",
        ]

    # -------- Study abroad / language --------
    if "ielts" in name:
        return [
            "Listening",
            "Reading",
            "Writing",
            "Speaking",
        ]

    if "toefl" in name or "pte" in name:
        return [
            "Reading",
            "Listening",
            "Speaking",
            "Writing",
        ]

    if "gre" in name:
        return [
            "Quantitative Reasoning",
            "Verbal Reasoning",
            "Analytical Writing",
        ]

    if "sat" in name:
        return [
            "Maths",
            "Reading & Writing",
        ]

    # -------- Government / civil services --------
    if "upsc" in name or "civil services" in name:
        return [
            "Polity",
            "History",
            "Geography",
            "Economy",
            "Environment",
            "Science & Tech",
            "Current Affairs",
            "Optional Subject",
        ]

    if "ssc" in name:
        return [
            "Quantitative Aptitude",
            "Reasoning",
            "English",
            "General Awareness",
        ]

    # -------- Professional exams --------
    if "cfa" in name:
        return [
            "Ethics",
            "Quantitative Methods",
            "Economics",
            "Financial Reporting & Analysis",
            "Corporate Finance",
            "Equity Investments",
            "Fixed Income",
            "Derivatives",
            "Alternative Investments",
            "Portfolio Management",
        ]

    if "ca" in name:
        return [
            "Accounting",
            "Costing",
            "Taxation",
            "Law",
            "Auditing",
            "Financial Management",
        ]

    if "clat" in name or "law" in name:
        return [
            "Legal Reasoning",
            "Logical Reasoning",
            "English",
            "General Knowledge & Current Affairs",
            "Quantitative Techniques",
        ]

    # -------- Semester / college exams --------
    if "semester" in cat or "college" in cat:
        return [
            "C Programming",
            "C++",
            "Python",
            "Maths",
            "DBMS",
            "DSA",
            "OS",
            "Computer Networks",
        ]

    # -------- Generic fallback --------
    return [
        "C Programming",
        "C++",
        "Python",
        "Maths",
        "DBMS",
        "DSA",
        "OS",
        "Other",
    ]

def fetch_random_quote() -> str:
    try:
        resp = requests.get("https://api.quotable.io/random", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            content = data.get("content", "").strip()
            author = data.get("author", "").strip()
            if content:
                return f"“{content}” — {author}" if author else f"“{content}”"
        return "Stay consistent. Your daily effort matters more than perfection."
    except Exception:
        return "Stay consistent. Your daily effort matters more than perfection."


# --------- Simple step state (for app-like flow) ---------
if "step" not in st.session_state:
    st.session_state["step"] = 1
if "user_name" not in st.session_state:
    st.session_state["user_name"] = ""
if "goal" not in st.session_state:
    st.session_state["goal"] = "Study goals"

# --------- Step 1: Welcome / basic info ---------
if st.session_state["step"] == 1:
    st.title("📚 Study Planner")
    st.subheader("Welcome!")

    st.write("Let's first know a bit about you and your exam prep.")

    name_input = st.text_input("Your name")
    goal_input = st.text_input("Your main goal (e.g., 'Semester 1 exams', 'GATE prep')")

    # ---- Exam category selection ----
    exam_category = st.selectbox(
        "Select exam category",
        [
            "Semester / College exams",
            "Engineering / Technical entrance",
            "Medical entrance",
            "Management / MBA / Business",
            "Study abroad / language",
            "Government / civil services / govt jobs",
            "Professional (CA / CFA / Law / others)",
            "Other",
        ],
        index=0,
    )

    # ---- Popular exams per category ----
    popular_exams_map = {
        "Semester / College exams": [
            "University semester exams",
            "Internal college exams",
        ],
        "Engineering / Technical entrance": [
            "JEE Main",
            "JEE Advanced",
            "GATE",
            "BITSAT",
            "VITEEE",
        ],
        "Medical entrance": [
            "NEET UG",
            "NEET PG",
        ],
        "Management / MBA / Business": [
            "CAT",
            "XAT",
            "MAT",
            "GMAT",
        ],
        "Study abroad / language": [
            "IELTS",
            "TOEFL",
            "PTE",
            "SAT",
            "GRE",
        ],
        "Government / civil services / govt jobs": [
            "UPSC CSE",
            "State PSC",
            "SSC CGL",
            "Bank PO",
        ],
        "Professional (CA / CFA / Law / others)": [
            "CA",
            "CFA",
            "CS",
            "CLAT",
            "LSAT",
        ],
        "Other": [],
    }

    popular_exams = popular_exams_map.get(exam_category, [])

    selected_exam = None
    if popular_exams:
        selected_exam = st.selectbox(
            "Select specific exam (or choose 'Other exam in this category')",
            popular_exams + ["Other exam in this category"],
        )

    custom_exam_name = st.text_input("Or enter the exact exam name")

    if st.button("Continue"):
        if not name_input.strip():
            st.error("Please enter your name to continue.")
        else:
            # Save name and goal
            st.session_state["user_name"] = name_input.strip()
            st.session_state["goal"] = goal_input.strip() if goal_input.strip() else "Study goals"

            # Save exam category
            st.session_state["exam_category"] = exam_category

            # Decide final exam name
            if custom_exam_name.strip():
                exam_name_final = custom_exam_name.strip()
            elif selected_exam and selected_exam != "Other exam in this category":
                exam_name_final = selected_exam
            else:
                exam_name_final = exam_category

            st.session_state["exam_name"] = exam_name_final
            st.session_state["default_subjects"] = get_default_subjects(
                exam_name_final, exam_category
            )
            # ---- Subject pool in session_state ----
            if "subject_pool" not in st.session_state:
                # start from exam-based defaults when Step 2 is opened first time
                default_subjects = st.session_state.get("default_subjects", [])
                st.session_state["subject_pool"] = sorted(set(default_subjects + ["Other"]))

            # Go to Step 2
            st.session_state["step"] = 2
            st.rerun()

    st.stop()


# --------- Step 2: Planner UI ---------

st.sidebar.header("Settings")
st.title("📚 Study Planner")
st.write("Plan your daily study schedule based on your subjects and available time.")

name = st.session_state.get("user_name", "Student")
goal = st.session_state.get("goal", "Study goals")
exam_category = st.session_state.get("exam_category", "Exam")
exam_name = st.session_state.get("exam_name", exam_category)

# Motivation from quote API + exam context
st.write("### 🎯 Motivation for your goal")

if st.button("Get motivational quote"):
    quote_text = fetch_random_quote()
    st.session_state["last_quote"] = quote_text

quote_to_show = st.session_state.get("last_quote", None)

if quote_to_show:
    st.write(f"For your **{exam_name}** preparation:")
    st.write(quote_to_show)
    st.caption("Quote source: public quotes API (e.g., Quotable/ZenQuotes).")
else:
    st.info("Click the button above to fetch a motivational quote for your exam.")

st.caption(f"Planning for: {exam_name} · {exam_category} · {goal}")

hours_per_day = st.sidebar.number_input(
    "Hours you can study per day",
    min_value=1.0, max_value=12.0, value=2.0, step=0.5
)

all_default = st.session_state.get("default_subjects", [])
base_pool = sorted(set(all_default + ["Other"]))

# always read from session_state
subject_pool = st.session_state.get("subject_pool", [])
default_subjects = st.session_state.get("default_subjects", [])

subjects = st.sidebar.multiselect(
    "Select your subjects",
    subject_pool,
    default=default_subjects if default_subjects else subject_pool,
)

new_subj = st.sidebar.text_input("Add another subject")
if st.sidebar.button("➕ Add subject") and new_subj.strip():
    new = new_subj.strip()
    if new not in subject_pool:
        # update pool in session_state
        subject_pool.append(new)
        st.session_state["subject_pool"] = subject_pool


st.sidebar.markdown("### Subject difficulty (1 = easy, 5 = hard)")
subject_difficulties = {}
for subj in subjects:
    subject_difficulties[subj] = st.sidebar.slider(
        f"{subj} difficulty",
        min_value=1, max_value=5, value=3
    )

target_date = st.sidebar.date_input(
    "Target exam date / goal date",
    datetime.date.today() + datetime.timedelta(days=30)
)

overall_difficulty = st.sidebar.slider(
    "Overall syllabus difficulty",
    min_value=1, max_value=5, value=3
)

generate_plan = st.sidebar.button("Generate Study Plan")

st.write("---")

today = datetime.date.today()

# ------------------ Tabs Layout ------------------

tab_planner, tab_progress = st.tabs(["📅 Planner", "📋 Plan distribution"])

with tab_planner:
    today = datetime.date.today()

    if "view_mode" not in st.session_state:
        st.session_state["view_mode"] = "table"

    if generate_plan:
        days_left = (target_date - today).days

        if days_left <= 0:
            st.error("Target date must be in the future.")
        elif len(subjects) == 0:
            st.error("Please select at least one subject.")
        else:
            total_hours = days_left * hours_per_day

            # Weight subjects by difficulty
            weights = []
            for subj in subjects:
                diff = subject_difficulties.get(subj, 3)
                weights.append(diff)

            weight_sum = sum(weights) if sum(weights) > 0 else 1
            subject_hours = {}
            for subj, w in zip(subjects, weights):
                subject_hours[subj] = total_hours * (w / weight_sum)

            st.session_state["subject_hours"] = subject_hours

            # Build day-wise plan
            daily_hours = hours_per_day
            plan_rows = []
            calendar_events = []

            day_date = today
            subject_index = 0
            subject_list = list(subjects)

            for day in range(days_left):
                day_subjects = []

                slots = 2
                hours_per_slot = daily_hours / slots

                for _ in range(slots):
                    subj = subject_list[subject_index % len(subject_list)]
                    day_subjects.append(f"{subj} ({hours_per_slot:.1f} h)")
                    subject_index += 1

                focus_text = " + ".join(day_subjects)

                plan_rows.append(
                    {
                        "Date": day_date.strftime("%d %b"),
                        "Focus": focus_text,
                    }
                )

                calendar_events.append(
                    {
                        "title": focus_text,
                        "start": day_date.isoformat(),
                        "end": day_date.isoformat(),
                    }
                )

                day_date += datetime.timedelta(days=1)

            # Save plan in session_state
            st.session_state["plan_rows"] = plan_rows
            st.session_state["calendar_events"] = calendar_events
            st.session_state["has_plan"] = True

    # Show stored plan if available
    if st.session_state.get("has_plan", False):
        plan_rows = st.session_state.get("plan_rows", [])
        calendar_events = st.session_state.get("calendar_events", [])
        subject_hours = st.session_state.get("subject_hours", {})

        days_left = len(plan_rows)
        total_hours = days_left * hours_per_day if days_left > 0 else 0

        st.subheader(f"📌 Overview for {name}")
        st.caption(f"Planning for: {exam_name} · {exam_category}")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Days left", days_left)
        with col2:
            st.metric("Total hours planned", f"{total_hours:.1f}")
        with col3:
            st.metric("Subjects", len(subject_hours))

        st.write("### Hours per subject (weighted by difficulty)")
        for subj, hrs in subject_hours.items():
            st.write(f"- {subj}: **{hrs:.1f}** hours")

        # ---- View selector (icons on the right) ----
        top_left, top_spacer, top_right = st.columns([3, 5, 2])

        with top_left:
            st.write("### Day-wise study plan")

        with top_right:
            col_list, col_cal = st.columns(2)
            with col_list:
                if st.button("📋", help="List / table view"):
                    st.session_state["view_mode"] = "table"
            with col_cal:
                if st.button("📅", help="Calendar view"):
                    st.session_state["view_mode"] = "calendar"

        view_mode = st.session_state["view_mode"]

        # DataFrame for interactive list view
        df_plan = pd.DataFrame(plan_rows)

        if view_mode == "table":
            st.dataframe(df_plan, use_container_width=True)
        else:
            calendar_options = {
                "initialView": "dayGridMonth",
                "selectable": False,
                "editable": False,

                # make calendar taller and rows expandable
                "contentHeight": 650,  # try 600–800 and adjust as you like
                "expandRows": True,  # allow month rows to grow vertically
                "dayMaxEventRows": False,  # do not collapse into “+ more”

                "headerToolbar": {
                    "left": "prev,next today",
                    "center": "title",
                    "right": "dayGridMonth,dayGridWeek,dayGridDay",
                },
            }

            calendar(
                events=calendar_events,
                options=calendar_options,
                custom_css="""
                .fc-daygrid-event .fc-event-main-frame {
                    white-space: normal;      /* allow text to wrap */
                    line-height: 1.1;         /* tighter lines so more fits */
                    font-size: 0.75rem;       /* slightly smaller text */
                }
                .fc-daygrid-event {
                    padding: 1px 2px;         /* reduce padding to gain space */
                }
                """,
                key="study_calendar",
            )

        # Simple advice
        if subject_hours:
            st.write("### Smart advice for you")
            hardest_subject = max(subject_hours, key=subject_hours.get)
            easiest_subject = min(subject_hours, key=subject_hours.get)

            advice = (
                f"Focus more on **{hardest_subject}**, since it needs the most hours. "
                f"Use your fresh energy at the start of the day for this.\n\n"
                f"Keep **{easiest_subject}** for lighter sessions when you are tired.\n\n"
                f"Try to protect your **{hours_per_day:.1f} hours/day** as non-negotiable study time. "
                f"On busy days, at least finish one slot from the plan above."
            )
            st.write(advice)
    else:
        if not generate_plan:
            st.info(
                "Set your details in the sidebar and click **Generate Study Plan** "
                "to see your schedule."
            )


with tab_progress:
    st.subheader("📊 Plan distribution (hours per subject)")

    if "subject_hours" not in st.session_state:
        st.info("Generate a study plan in the Planner tab first to see your subject-wise data.")
    else:
        subject_hours = st.session_state["subject_hours"]

        df_hours = pd.DataFrame(
            {
                "Subject": list(subject_hours.keys()),
                "Hours": list(subject_hours.values()),
            }
        )

        st.dataframe(df_hours, use_container_width=True)
        st.write(
            "This shows how your **planned** study hours are distributed across subjects. "
            "Live completion tracking can be added later."
        )

# ------------------ Connect with me ------------------

st.write("---")
st.subheader("🌐 Connect with the creator")

st.write("If you like this Study Planner, you can see the code or connect with me here:")

col_github, col_linkedin = st.columns(2)

GITHUB_URL = "https://github.com/Purva9665"
LINKEDIN_URL = "https://www.linkedin.com/in/purva-kadam-791350383/"

with col_github:
    st.link_button("🔗 View on GitHub", GITHUB_URL, type="primary")

with col_linkedin:
    st.link_button("💼 Connect on LinkedIn", LINKEDIN_URL)
