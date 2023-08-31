import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text, inspect
from sqlalchemy.orm import Session, sessionmaker, registry

# open vivino.db from data directory
vivino_engine = create_engine('sqlite:///../data/vivino.db', echo=True)
vivino_engine.connect()

# establish and instantiate session as vivino_session
vivino_session = sessionmaker(bind=vivino_engine)
vivino_session = vivino_session()

# create a registry for the vivino_session
mapper_registry = registry()
Base = mapper_registry.generate_base()



# query wines table from vivino.db
query_wines_of_the_world = vivino_engine.execute(
    """
    SELECT 
        wines.id AS wine_id,
        wines.name AS wine_name,
        wines.is_natural AS is_natural,
        wines.ratings_average,
        wines.ratings_count,
        regions.name AS region_name,
        countries.name AS country_name
    FROM 
        wines
    LEFT JOIN 
        regions ON wines.region_id = regions.id
    LEFT JOIN 
        countries ON regions.country_code = countries.code
    ORDER BY
        ratings_count DESC;
    """
)

# fetch query_wines_of_the_world
fetch_query_wines_of_the_world = query_wines_of_the_world.fetchall()

# initialize fetch_query_wines_of_the_world into pandas dataframe named df_wines_expanded
df_wines_expanded = pd.DataFrame(
    fetch_query_wines_of_the_world,
    columns=query_wines_of_the_world.keys()
)

# # unlimited display df_wines_expanded
# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     display(df_wines_expanded)

# create an map sidebar using streamlit
st.title("WINES OF THE WORLD")
st.dataframe(df_wines_expanded)


