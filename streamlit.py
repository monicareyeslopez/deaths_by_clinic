# Create a Streamlit app that includes:
# A short title and description of the case.
# One or more visualizations (line chart, bar chart, etc.) that show trends in the data (e.g., births vs. deaths, hand-washing introduction impact).
# Short explanation (2–3 sentences) within the app describing your findings
# Optional: Add filters or sliders for exploring different years or hospitals.



# ----
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(page_title="Semmelweis & Handwashing", layout="wide")

# ── Title & description ───────────────────────────────────────────────────────
st.title("🧼 The Semmelweis Handwashing Discovery")
st.markdown(
    """
    In the 1840s, Dr. Ignaz Semmelweis worked at the Vienna General Hospital, where he noticed
    that mortality rates from childbed fever were dramatically higher in **Clinic 1** (staffed by
    doctors and medical students) than in **Clinic 2** (staffed by midwives). In **1847**, he
    mandated that doctors wash their hands with chlorinated lime solution before delivering
    babies — and deaths plummeted almost immediately.  
    This app explores that data and the life-saving impact of his intervention.

    Authors: Monica Reyes-Lopez, and Xavier Alonso
    """
)
st.divider()

# ── Load data ─────────────────────────────────────────────────────────────────
df = pd.read_csv("yearly_deaths_by_clinic-1.csv")
df.columns = df.columns.str.strip()
df["Death Rate (%)"] = (df["Deaths"] / df["Birth"] * 100).round(2)
df["Clinic"] = df["Clinic"].str.title()

# ── Sidebar filters ───────────────────────────────────────────────────────────
st.sidebar.header("🔍 Filters")
year_range = st.sidebar.slider(
    "Select year range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (int(df["Year"].min()), int(df["Year"].max())),
)
clinics = st.sidebar.multiselect(
    "Select clinics", options=df["Clinic"].unique().tolist(), default=df["Clinic"].unique().tolist()
)

filtered = df[(df["Year"].between(*year_range)) & (df["Clinic"].isin(clinics))]

# ── KPI row ───────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

pre = df[df["Year"] < 1847]
post = df[df["Year"] >= 1847]
clinic1_pre = pre[pre["Clinic"] == "Clinic 1"]["Death Rate (%)"].mean()
clinic1_post = post[post["Clinic"] == "Clinic 1"]["Death Rate (%)"].mean()

col1.metric("Clinic 1 Death Rate (pre-1847)", f"{clinic1_pre:.1f}%")
col2.metric("Clinic 1 Death Rate (post-1847)", f"{clinic1_post:.1f}%", delta=f"{clinic1_post - clinic1_pre:.1f}%", delta_color="inverse")
col3.metric("Lives saved (Clinic 1, 1847–1849)",
            int(post[post["Clinic"] == "Clinic 1"].apply(
                lambda r: r["Birth"] * (clinic1_pre / 100) - r["Deaths"], axis=1).sum()))

st.divider()

# ── Chart 1: Death rate over time ─────────────────────────────────────────────
st.subheader("📉 Death Rate Over Time by Clinic")

fig1 = px.line(
    filtered, x="Year", y="Death Rate (%)", color="Clinic",
    markers=True,
    color_discrete_map={"Clinic 1": "#e05252", "Clinic 2": "#4c8bf5"},
    labels={"Death Rate (%)": "Death Rate (% of births)"},
)
fig1.add_vline(
    x=1847, line_dash="dash", line_color="green",
    annotation_text="Handwashing introduced (1847)",
    annotation_position="top left",
    annotation_font_color="green",
)
fig1.update_layout(
    plot_bgcolor="white",
    yaxis=dict(gridcolor="#eeeeee"),
    legend=dict(title="Clinic"),
)
st.plotly_chart(fig1, use_container_width=True)

# ── Chart 2: Births vs Deaths grouped bar ────────────────────────────────────
st.subheader("📊 Births vs. Deaths by Year and Clinic")

fig2 = go.Figure()
colors = {"Clinic 1": ("#f5a0a0", "#e05252"), "Clinic 2": ("#a0c4f5", "#4c8bf5")}

for clinic in clinics:
    sub = filtered[filtered["Clinic"] == clinic]
    light, dark = colors.get(clinic, ("#ccc", "#888"))
    fig2.add_trace(go.Bar(
        name=f"{clinic} – Births", x=sub["Year"], y=sub["Birth"],
        marker_color=light, legendgroup=clinic,
    ))
    fig2.add_trace(go.Bar(
        name=f"{clinic} – Deaths", x=sub["Year"], y=sub["Deaths"],
        marker_color=dark, legendgroup=clinic,
    ))

fig2.update_layout(
    barmode="group",
    xaxis_title="Year",
    yaxis_title="Count",
    plot_bgcolor="white",
    yaxis=dict(gridcolor="#eeeeee"),
)
fig2.add_vline(x=1847, line_dash="dash", line_color="green",
               annotation_text="← Handwashing", annotation_font_color="green")
st.plotly_chart(fig2, use_container_width=True)

# ── Findings ──────────────────────────────────────────────────────────────────
st.divider()
st.subheader("🔬 Key Findings")
st.info(
    """
    **Before 1847**, Clinic 1's death rate averaged around **9–10%** of births — roughly
    3–5× higher than Clinic 2, which was staffed by midwives who did not perform autopsies.
    **After Semmelweis mandated handwashing in 1847**, Clinic 1's death rate fell sharply
    to under **2%**, converging with Clinic 2's historically lower rate.
    This natural experiment provides one of history's earliest and most compelling pieces of
    evidence for germ theory and the importance of hygiene in medical practice.
    """
)

# ── Raw data expander ─────────────────────────────────────────────────────────
with st.expander("📋 View raw data"):
    st.dataframe(filtered.reset_index(drop=True), use_container_width=True)
