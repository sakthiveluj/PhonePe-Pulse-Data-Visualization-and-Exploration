import os
import json
import streamlit as st
import pandas as pd
import requests
import mysql.connector
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

#CREATE DATAFRAMES FROM SQL
#sql connection
mydb = mysql.connector.connect(host = "localhost",
                        user = "sakthi",
                        password = "Sakthi12345",
                        database = "phonepe_data"
                        )
cursor = mydb.cursor(buffered=True)

#Aggregated_transsaction
cursor.execute("select * from aggregated_transaction;")
mydb.commit()
table1 = cursor.fetchall()
Aggre_transaction = pd.DataFrame(table1,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count", "Transaction_amount"))

#Aggregated_user
cursor.execute("select * from aggregated_user")
mydb.commit()
table2 = cursor.fetchall()
Aggre_user = pd.DataFrame(table2,columns = ("States", "Years", "Quarter", "Brands", "Transaction_count", "Percentage"))

#Map_transaction
cursor.execute("select * from map_transaction")
mydb.commit()
table3 = cursor.fetchall()
Map_transaction = pd.DataFrame(table3,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count", "Transaction_amount"))

#Map_user
cursor.execute("select * from map_user")
mydb.commit()
table4 = cursor.fetchall()
Map_user = pd.DataFrame(table4,columns = ("States", "Years", "Quarter", "Districts", "RegisteredUser", "AppOpens"))

#Top_transaction
cursor.execute("select * from top_transaction")
mydb.commit()
table5 = cursor.fetchall()
Top_transaction = pd.DataFrame(table5,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))

#Top_user
cursor.execute("select * from top_user")
mydb.commit()
table6 = cursor.fetchall()
Top_user = pd.DataFrame(table6, columns = ("States", "Years", "Quarter", "Pincodes", "RegisteredUser"))

def Transaction_amount_count_Y(df, year):
    # aggre_transaction_amount_count_year(tacy)
    tacy = df[df["Years"]== year]
    tacy.reset_index(drop = True, inplace = True)

    tacyg = tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2= st.columns(2)

    with col1:

        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name= []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1= px.choropleth(tacyg, geojson=data1, locations= "States", featureidkey= "properties.ST_NM", 
                                color= "Transaction_amount", color_continuous_scale= "Rainbow",
                                range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()), 
                                hover_name= "States", title= f"{year} TRANSACTION AMOUNT", fitbounds= "locations", 
                                height= 600,width= 600)
        
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)
        
        
    with col2:

        fig_count=px.bar(tacyg, x="States" , y="Transaction_count", title=f"{year} TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 650,width= 600)
        st.plotly_chart(fig_count)

    col1,col2= st.columns(2)


    return tacy


def Transaction_amount_count_Y_Q(df, quarter):
    # aggre-transaction_amount_year-quarter(tacy)
    tacy = df[df["Quarter"]== quarter]
    tacy.reset_index(drop = True, inplace = True)

    tacyg = tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name= []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1= px.choropleth(tacyg, geojson=data1, locations= "States", featureidkey= "properties.ST_NM", 
                                color= "Transaction_amount", color_continuous_scale= "Rainbow",
                                range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()), 
                                hover_name= "States", title= f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds= "locations", 
                                height= 600,width= 600)
        
        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)

    with col2:

        fig_count=px.bar(tacyg, x="States" , y="Transaction_count", title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 650,width= 600)
        st.plotly_chart(fig_count)
        
        
    col1,col2= st.columns(2)

    



def Aggre_user_plot_1(df, year):
    aguy= df[df["Years"]== year]
    aguy.reset_index(drop= True, inplace= True)

    aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_bar_1= px.bar(aguyg, x="Brands", y="Transaction_count", title= "BRANDS AND TRANSACTION COUNT",
                    width= 1000, color_discrete_sequence= px.colors.sequential.haline, hover_name="Brands")

    st.plotly_chart(fig_bar_1)

    return aguy

def Aggre_user_plot_2(df, quarter):
    aguyq= df[df["Quarter"]== quarter]
    aguyq.reset_index(drop= True, inplace= True)

    aguyqg= pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace= True)

    fig_bar_1= px.bar(aguyqg, x= "Brands", y= "Transaction_count", title= f"{quarter} QUARTER, BRANDS AND TRANSACTION COUNT",
                    width= 1000, color_discrete_sequence= px.colors.sequential.haline, hover_name="Brands")

    st.plotly_chart(fig_bar_1)

    return aguyq

def Aggre_user_plot_3(df, state):

    auyqs= df[df["States"] == state]
    auyqs.reset_index(drop= True, inplace= True)

    fig_line_1=px.line(auyqs, x= "Brands", y= "Transaction_count",
                    title= "BRANDS, TRANSACTION COUNT , PERCENTAGE" ,width=1000, markers= True)
    st.plotly_chart(fig_line_1)


def map_user_plot_1(df, year):
    muy= df[df["Years"]== year]
    muy.reset_index(drop= True, inplace= True)

    muyg= muy.groupby("States")[["RegisteredUser","AppOpens"]].sum()
    muyg.reset_index(inplace= True)

    fig_line_1= px.line(muyg, x="States", y= ["RegisteredUser", "AppOpens"],
                        title= "REGISTEREDUSER APPOPENS", width= 1000, height= 800, markers= True)
    st.plotly_chart(fig_line_1)

    return muy

def map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"]== quarter]
    muyq.reset_index(drop= True, inplace= True)

    muyqg= muyq.groupby("States")[["RegisteredUser", "AppOpens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_line_1= px.line(muyqg, x= "States", y= ["RegisteredUser", "AppOpens"],
                        title= "QUARTER REGISTERED USER APPOPENS", width= 1000, height=800, markers=True,
                         color_discrete_sequence= px.colors.sequential.Aggrnyl)
    
    st.plotly_chart(fig_line_1)

    return muyq




def top_user_plot_1(df, year):
    tuy= df[df["Years"]== year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["States", "Quarter"])["RegisteredUser"].sum())
    tuyg.reset_index(inplace= True)

    fig_bar_1= px.bar(tuyg, x="States", y="RegisteredUser", title= "REGISTEREDUSER", color= "Quarter",
                    width= 1000, color_discrete_sequence= px.colors.sequential.haline, hover_name="States")

    st.plotly_chart(fig_bar_1)
  
    return tuy


def top_user_plot_2(df,state):
    tuys= df[df["States"] == state]
    tuys.reset_index(drop= True, inplace= True)


    fig_top_plot_2= px.bar(tuys, x= "Quarter", y= "RegisteredUser",title= "REGISTEREDUSER, PINCODES, QUARTER",
                           width=1000, height= 800,color= "RegisteredUser", 
                            color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_2)

def ques1():
    brand= Aggre_user[["Brands","Transaction_count"]]
    brand1= brand.groupby("Brands")["Transaction_count"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index()

    fig_brands= px.pie(brand2, values= "Transaction_count", names= "Brands", color_discrete_sequence=px.colors.sequential.dense_r,
                       title= "Top Mobile Brands of Transaction_count")
    return st.plotly_chart(fig_brands)

def ques2():
    lt= Aggre_transaction[["States", "Transaction_amount"]]
    lt1= lt.groupby("States")["Transaction_amount"].sum().sort_values(ascending= True)
    lt2= pd.DataFrame(lt1).reset_index().head(10)

    fig_lts= px.bar(lt2, x= "States", y= "Transaction_amount",title= "LOWEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques3():
    htd= Map_transaction[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=False)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Emrld_r)
    return st.plotly_chart(fig_htd)

def ques4():
    htd= Map_transaction[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
    return st.plotly_chart(fig_htd)


def ques5():
    sa= Map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=False)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="Top 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.deep_r)
    return st.plotly_chart(fig_sa)

def ques6():
    sa= Map_user[["States", "AppOpens"]]
    sa1= sa.groupby("States")["AppOpens"].sum().sort_values(ascending=True)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "AppOpens", title="lowest 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.dense_r)
    return st.plotly_chart(fig_sa)

def ques7():
    stc= Aggre_transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=True)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH LOWEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Jet_r)
    return st.plotly_chart(fig_stc)

def ques8():
    stc= Aggre_transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=False)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH HIGHEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_stc)

def ques9():
    ht= Aggre_transaction[["States", "Transaction_amount"]]
    ht1= ht.groupby("States")["Transaction_amount"].sum().sort_values(ascending= False)
    ht2= pd.DataFrame(ht1).reset_index().head(10)

    fig_lts= px.bar(ht2, x= "States", y= "Transaction_amount",title= "HIGHEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques10():
    dt= Map_transaction[["Districts", "Transaction_amount"]]
    dt1= dt.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    dt2= pd.DataFrame(dt1).reset_index().head(50)

    fig_dt= px.bar(dt2, x= "Districts", y= "Transaction_amount", title= "DISTRICTS WITH LOWEST TRANSACTION AMOUNT",
                color_discrete_sequence= px.colors.sequential.Mint_r)
    return st.plotly_chart(fig_dt)


# streamlit part 

st.set_page_config(layout= "wide")

st.title(":violet[PHONEPE DATA VISUALIZATION AND EXPLORATION]")
st.write(':green[ Transaction and User Data based on analysis in the span of year **2018** to **2023** in **INDIA** ]')

with st.sidebar:

    select = option_menu("Main Menu", ["HOME PAGE", "DATA ANALYSIS" , "BRAINSTORMING"])

if select == "HOME PAGE":

    image=Image.open("C:/Users/Jayavelu/OneDrive/Desktop/Desktop Downloads/phonepeimage4.webp")
    st.image(image,width= 1000)

    col1,col2= st.columns(2)

    with col1:
        st.header(":violet[PHONEPE]")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("   **-> Credit & Debit card linking**")
        st.write("   **-> Bank Balance check**")
        st.write("   **->Instantly & Free**")
        st.write("   **->PIN Authorization**")
        st.write("   **->No Wallet Top-Up Required**")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        image=Image.open("C:/Users/Jayavelu/OneDrive/Desktop/Desktop Downloads/phonepeimage3.jpg")
        st.image(image)

    col3,col4= st.columns(2)

    with col3:
        image=Image.open("C:/Users/Jayavelu/OneDrive/Desktop/Desktop Downloads/phonepeimage1.jpg")
        st.image(image)

    with col4:
        st.write("**-> Easy Transactions**")
        st.write("**-> One App For All Your Payments**")
        st.write("**-> Your Bank Account Is All You Need**")
        st.write("**-> Multiple Payment Modes**")
        st.write("**-> PhonePe Merchants**")
        st.write("**-> 1.Direct Transfer & More**")
        st.write("**-> 2.QR Code**")
        st.write("**-> Earn Great Rewards**")


elif select =="DATA ANALYSIS":
    
    tab1, tab2 , tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:

        method = st.radio("Select The Method",["Aggregated Transaction", "Aggregated User"])

        if method == "Aggregated Transaction":
             
            col1,col2= st.columns(2)
            with col1:
                 
                 years= st.number_input("Select The Year", Aggre_transaction["Years"].min(), Aggre_transaction["Years"].max(),  Aggre_transaction["Years"].min() )
            tac_Y= Transaction_amount_count_Y(Aggre_transaction, years)

            col1,col2= st.columns(2)

            with col1:
                 
                 quarters= st.number_input("Select The Quarter", tac_Y["Quarter"].min(), tac_Y["Quarter"].max(),  tac_Y["Quarter"].min() )
            Transaction_amount_count_Y_Q(tac_Y, quarters)

                 
            

        elif method == "Aggregated User":
            col1,col2= st.columns(2)
            with col1:
                 
                 years= st.number_input("Select The Year", Aggre_user["Years"].min(), Aggre_user["Years"].max(),  Aggre_user["Years"].min() )
            Aggre_user_Y= Aggre_user_plot_1(Aggre_user, years)

            col1, col2= st.columns(2)
            with col1:
                
                quarters= st.number_input("Select The Quarter",Aggre_user_Y["Quarter"].min(), Aggre_user_Y["Quarter"].max(), Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q= Aggre_user_plot_2(Aggre_user_Y, quarters)

            col1, col2= st.columns(2)
            with col1:
                states= st.selectbox("Select The State",  Aggre_user_Y_Q["States"].unique())
            Aggre_user_plot_3(Aggre_user_Y_Q, states)


    with tab2:
        
        method_2= st.radio("Select The Method",["Map Transaction", "Map User"])

        if method_2 == "Map Transaction":
            col1,col2= st.columns(2)
            with col1:
                years= st.number_input("Select the Year", Map_transaction["Years"].min(), Map_transaction["Years"].max(),Map_transaction["Years"].min())

            Map_transaction_tac_Y= Transaction_amount_count_Y(Map_transaction, years)

        
            col1,col2= st.columns(2)
            with col1:
                quarters= st.number_input("Select the Quarter", Map_transaction_tac_Y["Quarter"].min(), Map_transaction_tac_Y["Quarter"].max(),Map_transaction_tac_Y["Quarter"].min())

            Transaction_amount_count_Y_Q(Map_transaction_tac_Y, quarters)

            

        elif method_2 == "Map User":
            col1,col2= st.columns(2)
            with col1:
                years= st.number_input("Select The year", Map_user["Years"].min(), Map_user["Years"].max(),  Map_user["Years"].min() )
            Map_user_Y= map_user_plot_1(Map_user, years)

            col1, col2= st.columns(2)
            with col1:
                
                quarters= st.number_input("Select the Quarter",Map_user_Y["Quarter"].min(), Map_user_Y["Quarter"].max(), Map_user_Y["Quarter"].min())
            Map_user_Y_Q= map_user_plot_2(Map_user_Y, quarters)


            


            


    with tab3:
        method_3= st.radio("Select The Method",["Top Transaction", "Top User"])

        if method_3 == "Top Transaction":
            col1,col2= st.columns(2)
            with col1:
                years= st.number_input("select the year", Top_transaction["Years"].min(), Top_transaction["Years"].max(), Top_transaction["Years"].min())
            Top_transaction_tac_Y= Transaction_amount_count_Y(Top_transaction, years)

            col1,col2= st.columns(2)
            with col1:
                quarters=st.number_input("select the quarter", Top_transaction_tac_Y["Quarter"].min(), Top_transaction_tac_Y["Quarter"].max(), Top_transaction_tac_Y["Quarter"].min())
            Transaction_amount_count_Y_Q(Top_transaction_tac_Y, quarters)
            
        elif method_3 == "Top User":
            col1,col2= st.columns(2)
            with col1:
                years= st.number_input("Select the Year", Top_user["Years"].min(), Top_user["Years"].max(),  Top_user["Years"].min())
            Top_user_Y= top_user_plot_1(Top_user, years)

            col1, col2= st.columns(2)
            with col1:
                
                quarters= st.number_input("Select THE Quarter",Top_user_Y["Quarter"].min(), Top_user_Y["Quarter"].max(), Top_user_Y["Quarter"].min())
            Top_user_Y_Q= top_user_plot_2(Top_user_Y, quarters)


elif select == "BRAINSTORMING":
    
    ques= st.selectbox("select the question",('Top Brands Of Mobiles Used','States With Lowest Trasaction Amount',
                                'Districts With Highest Transaction Amount','Top 10 Districts With Lowest Transaction Amount',
                                'Top 10 States With AppOpens','Least 10 States With AppOpens','States With Lowest Trasaction Count',
                                'States With Highest Trasaction Count','States With Highest Trasaction Amount',
                                'Top 50 Districts With Lowest Transaction Amount'))
    if ques=="Top Brands Of Mobiles Used":
        ques1()

    elif ques=="States With Lowest Trasaction Amount":
        ques2()

    elif ques=="Districts With Highest Transaction Amount":
        ques3()

    elif ques=="Top 10 Districts With Lowest Transaction Amount":
        ques4()

    elif ques=="Top 10 States With AppOpens":
        ques5()

    elif ques=="Least 10 States With AppOpens":
        ques6()

    elif ques=="States With Lowest Trasaction Count":
        ques7()

    elif ques=="States With Highest Trasaction Count":
        ques8()

    elif ques=="States With Highest Trasaction Amount":
        ques9()

    elif ques=="Top 50 Districts With Lowest Transaction Amount":
        ques10()
