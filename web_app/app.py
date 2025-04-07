from utils.openai import send_image_to_server
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(layout="wide") # Use wider layout

# Set consistent plot style
sns.set_theme(style="whitegrid")

# --- Helper Function to Create Plots ---
# This helps avoid matplotlib state issues in Streamlit
def create_plot(plot_func, *args, **kwargs):
    """Creates a matplotlib plot in a new figure."""
    fig, ax = plt.subplots()
    plot_func(*args, **kwargs, ax=ax)
    return fig

# --- Streamlit App ---
st.title("📊 Dataset Analysis")
# button for refreshing data
if st.button('Refresh Data'):
    st.cache_data.clear()


tab1, tab2 = st.tabs(["Mandatory Tasks Results", "Additional Visualization Tasks"])

@st.cache_data
def load_data():
    with st.spinner():
        df = None
        dataset_path = os.environ.get("DATASET_PATH_TIPSPORT")
        if os.path.exists(dataset_path):
            df = pd.read_csv(dataset_path)
        if df is None:
            raise FileNotFoundError('Could not find csv file with data.')
        return df


with tab1:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.header('Task 1 - Common words')
        res1 = pd.read_csv('./results/Task1_results.csv')
        st.dataframe(res1, use_container_width=True)
    with col2:
        st.header('Task 2 - Similar words')
        res2 = pd.read_csv('./results/Task2_results.csv')
        st.dataframe(res2, use_container_width=True)
    with col3:
        st.header('Task 3 - Dollar amount')
        res3 = pd.read_csv('./results/Task3_results.csv')
        st.dataframe(res3, use_container_width=True)

with tab2:
    data = load_data()
    expander1 = st.expander("1. Number of articles by sex")
    expander2 = st.expander("2. Top 10 topics")
    expander3 = st.expander("3. Heatmap of top 10 topics vs. zodiac signs")
    with expander1:
        st.header("1. Number of articles by sex")
        colexp11, colexp12 = st.columns(2)
        with colexp11:
            if 'gender' in data.columns:
                gender_counts = data['gender'].value_counts()
                if not gender_counts.empty:
                    fig1, ax1 = plt.subplots()
                    p, tx, autotexts = ax1.pie(gender_counts.values,
                            labels=gender_counts.index.tolist(),
                            autopct='',
                            shadow=False,
                            startangle=90)
                    percentage = [gender_counts.values[i] / sum(gender_counts.values) for i in range(len(gender_counts.values))]

                    for i, a in enumerate(autotexts):
                        a.set_text(f"{percentage[i]:.1%}\n {gender_counts.values[i]}")
                    ax1.axis('equal')
                    # add actual numbers to the pie chart
                    fig1.set_size_inches(5, 4)
                    # set smaller font
                    plt.setp(tx, size=10, weight="bold")
                    st.pyplot(fig1, use_container_width=False)
                    # save the figure for openai processing
                    os.makedirs('data', exist_ok=True)
                    fig1.savefig('data/pie_chart.png')
                else:
                    st.warning("There are no articles in the dataset.")
            else:
                st.warning("Can not find gender column in the dataset.")

            with colexp12:
                genai_ask1 = st.button('Interpret the graph by AI', key='ask1')
                if genai_ask1:
                    with st.spinner('Getting response'):
                        text_response_1 = send_image_to_server(task_number=1, image_path='data/pie_chart.png')
                        gender_interpretation = st.write(text_response_1)

    with expander2:
        st.header("2. Top 10 topics")
        colexp21, colexp22 = st.columns(2)
        with colexp21:
            if 'topic' in data.columns:
                # Handle potential NaN values in 'topic' before counting
                topic_counts = data['topic'].dropna().value_counts()
                top_10_topics = topic_counts.head(10)

                if not top_10_topics.empty:
                    fig_topics = create_plot(sns.barplot, y=top_10_topics.index, x=top_10_topics.values, orient='h',
                                             palette="magma")
                    plt.xlabel("Number of articles")
                    plt.ylabel("Topic")
                    plt.title("Top 10 topics")
                    plt.tight_layout()  # Adjust layout to prevent labels overlapping
                    # set size of the figure
                    fig_topics.set_size_inches(5, 4)
                    # center the plot to the container center
                    st.pyplot(fig_topics, use_container_width=False)
                    # save the figure for openai processing
                    os.makedirs('data', exist_ok=True)
                    fig_topics.savefig('data/topics_chart.png')

                else:
                    st.warning("There are no topics in the dataset.")
            else:
                st.warning("Column Topic not found")
        with colexp22:
            genai_ask2 = st.button('Interpret the graph by AI', key='ask2')
            if genai_ask2:
                with st.spinner('Getting response'):
                    text_response_2 = send_image_to_server(task_number=2, image_path='data/topics_chart.png')
                    topics_interpretation = st.write(text_response_2)

    with expander3:
        st.header("3. Heatmap of top 10 topics vs. zodiac signs")
        colexp31, colexp32 = st.columns(2)
        with colexp31:
            if 'topic' in data.columns and 'sign' in data.columns:
                tmp_data = data.copy()
                # take just top 10 topics
                top_10_topics = data['topic'].value_counts().head(10).index.tolist()
                # Filter the data to include only the top 10 topics
                tmp_data = tmp_data[tmp_data['topic'].isin(top_10_topics)]
                # Handle potential NaN values in 'sign'
                tmp_data.dropna(subset=['sign'], inplace=True)

                if not tmp_data.empty:
                    # Create a cross-tabulation (contingency table)
                    crosstab = pd.crosstab(tmp_data['topic'], tmp_data['sign'])

                    zodiac_order = [
                        "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                        "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"
                    ]
                    # Filter crosstab columns to include only signs present AND in the defined order
                    ordered_columns = [sign for sign in zodiac_order if sign in crosstab.columns]
                    # Reindex if there are columns to order
                    if ordered_columns:
                        crosstab = crosstab.reindex(columns=ordered_columns)

                    if not crosstab.empty:
                        st.write("")
                        fig_heatmap, ax_heatmap = plt.subplots(figsize=(12, 8))  # Adjust figure size
                        sns.heatmap(crosstab, annot=True, fmt="d", cmap="coolwarm", linewidths=.5, ax=ax_heatmap, cbar=True)
                        plt.xlabel("Zodiac Sign")
                        plt.ylabel("Theme")
                        plt.title("Heatmap of Topics vs Zodiac Signs")
                        plt.xticks(rotation=45, ha='right')  # Rotate labels for better readability
                        fig_heatmap.set_size_inches(10, 5)
                        plt.tight_layout()  # Adjust layout
                        st.pyplot(fig_heatmap, use_container_width=False)
                        # save the figure for openai processing
                        os.makedirs('data', exist_ok=True)
                        fig_heatmap.savefig('data/topics_heatmap.png')
                    else:
                        st.warning("Not enough data to create the heatmap. Please check the dataset.")
                else:
                    st.warning("After filtering, there are no articles in the dataset.")
        with colexp32:
            genai_ask3 = st.button('Interpret the graph by AI', key='ask3')
            if genai_ask3:
                with st.spinner('Getting response'):
                    text_response_3 = send_image_to_server(task_number=3, image_path='data/topics_heatmap.png')
                    heatmap_interpretation = st.write(text_response_3)

