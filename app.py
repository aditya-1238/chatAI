from dotenv import load_dotenv
load_dotenv()
import psycopg2 as psy
import streamlit as st
import os

import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLEAPI"))

def get_gemini_response(question,prompt ):
    model = genai.GenerativeModel('gemini-pro')
    response =model.generate_content([prompt[0],question])
    return response.text 

def read_sql_query(sql):
    conn = psy.connect(
    dbname=os.getenv("DBNAME"),
    user=os.getenv("DBUSER"),
    password=os.getenv("DBPASS"),
    host="localhost",
    port="5432")
    cur=conn.cursor()
    cur.execute(sql)
    rows=cur.fetchall()
    conn.commit()
    conn.close()
    return rows


prompt=[
    """
    You are an expert in converting English questions to SQL query!
    The SQL table has the name SALES and has the following columns SrNo, Order ID, Product, 
    Quantity Ordered, Price Each, Date, Purchase Address, Month, 
    Sales, City, Hour. Date is of the format yyyy/mm/dd. Month column has integer values representing the month number like december as 12.
    
    \n\nFor example,\nExample 1 - How many entries of records are present?, 
    the SQL command will be something like this SELECT COUNT(*) FROM SALES ;
    \nExample 2 - Tell me all the products bought on 2019/12/25?, 
    the SQL command will be something like this SELECT DISTINCT PRODUCT FROM SALES 
    where DATE='2019/12/25';
    \nExample 3 -  Give me total count of all products bought on 2019/12/25, 
    the SQL command will be something like this- SELECT SUM("Quantity Ordered") FROM SALES 
    where DATE='2019/12/25'; 

    when you mention a column name which has 2 or more terms seperated by a space character put the column name in double quotes like in example 3 "Quanitity Ordered" is in quotes.
    use " and not ` or ' for double quotes while generating queries
    also the sql code should not have ``` in beginning or end and sql word in output

    """


]

## Streamlit App

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

# if submit is clicked
if submit:
    response=get_gemini_response(question,prompt)
    print(response)
    response=read_sql_query(response)
    st.subheader("The Response is")
    for row in response:
        for i in row:
            print(i)
            st.header(i)

