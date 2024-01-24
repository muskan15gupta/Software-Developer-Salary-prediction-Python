import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt 


def shorten_categories(categories,cutoff):
    categorical_map={}
    for i in range(len(categories)):
        if categories.values[i]>=cutoff:
            categorical_map[categories.index[i]]=categories.index[i]
        else:
             categorical_map[categories.index[i]]='other'
    return categorical_map   


def clean_experience(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    try:
        return float(x)
    except ValueError:
        return None
    

def clean_education(x):
    if  'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if  'Master’s degree' in x:
        return 'Master’s degree'
    if  'Professional degree 'in x or 'Other doctoral degree' in x:
        return 'post grad'
    return 'less that a Bachelors'

@st.cache_data
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedComp"]]
    df=df[df["ConvertedComp"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed full-time"]
    df = df.drop("Employment", axis=1)

    country_map = shorten_categories(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    df = df[df["ConvertedComp"] <= 250000]
    df = df[df["ConvertedComp"] >= 10000]
    df = df[df["Country"] != "Other"]

    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_education)
    df = df.rename({"ConvertedComp": "Salary"}, axis=1)
    return df
   
df=load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write(
        "Stack Overflow Developer Survey 2020")
    
    data=df["Country"].value_counts()
    fig1, ax1=plt.subplots(figsize=(10,10))
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=False, startangle=90, pctdistance=0.75)
    ax1.axis("equal") 
    st.write("""#### Number of Data from different countries""")
    plt.tight_layout(pad=0.2)
    st.pyplot(fig1)

    st.write(
        """
    #### Mean Salary Based On Country
    """
    )

    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write(
        """
    #### Mean Salary Based On Experience
    """
    )

    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)




