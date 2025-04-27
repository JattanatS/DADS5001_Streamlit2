import streamlit as st
import streamlit as st
import duckdb as db
import pandas as pd
import plotly.express as px
import pydeck as pdk

st.write("# Starbucks in THAILAND 😃☕💯")
df = pd.read_csv("Starbucks.csv")
#st.write(df)

    
thailandProvinces = [
"Bangkok", 
"Krabi", 
"Kanchanaburi", 
"Khon Kaen", 
"Chantaburi", 
"Chachoengsao", 
"Chonburi", 
"Chainat", 
"Chaiyaphum", 
"Chiang Rai", 
"Chiang Mai", 
"Trang", 
"Trat", 
"Tak", 
"Nakhon Nayok", 
"Nakhon Pathom", 
"Nakhon Ratchasima", 
"Nakhon Si Thammarat", 
"Nakhon Sawan", 
"Narathiwat", 
"Nong Khai", 
"Nong Bua Lamphu", 
"Rayong", 
"Ratchaburi", 
"Lopburi", 
"Lampang", 
"Lamphun", 
"Loei", 
"Sisaket", 
"Sakon Nakhon", 
"Songkhla", 
"Samut Prakan", 
"Samut Songkhram", 
"Samut Sakhon", 
"Sa Kaeo", 
"Saraburi", 
"Suphan Buri", 
"Surat Thani", 
"Surin", 
"Satun", 
"Ubon Ratchathani", 
"Udon Thani", 
"Uttaradit", 
"Amnat Charoen", 
"Phayao", 
"Phatthalung", 
"Phetchaburi", 
"Phetchabun", 
"Mae Hong Son", 
"Yasothon", 
"Roi Et", 
"Nakhon Phanom", 
"Nan", 
"Bung Kan", 
"Buriram", 
"Pathum Thani", 
"Prachuap Khiri Khan", 
"Pattani", 
"Pichit", 
"Phitsanulok", 
"Phrae", 
"Phuket", 
"Maha Sarakham", 
"Mukdahan", 
"Lampang", 
"Uthai Thani", 
"Saraburi", 
"Sikkim", 
"Sakon Nakhon", 
"Samut Sakhon"
]


thailandProvinces.sort()
province_list = ", ".join(f"'{province}'" for province in thailandProvinces)
#query_thai= db.sql(f"""SELECT * FROM df WHERE Timezone like '%Bangkok%' AND city IN ({province_list})""").df()

@st.cache_data
def thai(df):
    query_thai = db.sql("""SELECT * FROM df WHERE country = 'TH' """).df()

    invalid_city_df = query_thai[~query_thai['City'].isin(thailandProvinces)]
    invalid_groupcity = db.sql("""SELECT City FROM invalid_city_df GROUP BY City""").df()
    postal_code_map = {
        "10100": "Bangkok",
        "10110": "Bangkok",
        "10120": "Bangkok",
        "10150": "Bangkok",
        "10160": "Bangkok",
        "10170": "Bangkok",
        "10200": "Bangkok",
        "10210": "Bangkok",
        "10220": "Bangkok",
        "10230": "Bangkok",
        "10240": "Bangkok",
        "10250": "Bangkok",
        "10260": "Bangkok",
        "10270": "Bangkok",
        "10280": "Bangkok",
        "10300": "Bangkok",
        "10310": "Bangkok",
        "10320": "Bangkok",
        "10330": "Bangkok",
        "10400": "Bangkok",
        "10500": "Bangkok",
        "10540": "Bangkok",
        "10600": "Bangkok",
        "10700": "Bangkok",
        "10900": "Bangkok",
        "11000": "Bangkok",
        "11120": "Nonthaburi",
        "11130": "Nonthaburi",
        "11140": "Nonthaburi",
        "12000": "Pathum Thani",
        "12121": "Samut Prakan",
        "12130": "Samut Prakan",
        "13000": "Nakhon Ratchasima",
        "13170": "Nakhon Ratchasima",
        "20000": "Chon Buri",
        "20110": "Chon Buri",
        "20150": "Chon Buri",
        "20230": "Chon Buri",
        "20260": "Chon Buri",
        "21000": "Rayong",
        "24130": "Chachoengsao",
        "30000": "Khon Kaen",
        "30130": "Khon Kaen",
        "31000": "Ubon Ratchathani",
        "34000": "Buriram",
        "40000": "Khon Kaen",
        "41000": "Udon Thani",
        "43000": "Nakhon Phanom",
        "50000": "Chiang Mai",
        "50200": "Chiang Mai",
        "50230": "Chiang Mai",
        "50300": "Chiang Mai",
        "52100": "Lampang",
        "57000": "Chiang Rai",
        "60000": "Nakhon Sawan",
        "65000": "Sukhothai",
        "74000": "Ratchaburi",
        "77110": "Prachuap Khiri Khan",
        "80000": "Surat Thani",
        "81000": "Surat Thani",
        "83000": "Phuket",
        "83100": "Phuket",
        "83150": "Phuket",
        "84000": "Krabi",
        "84320": "Trang",
        "90110": "Songkhla",
        "84140": "Surat Thani",
        "83130": "Phuket",
        "83110": "Phuket",
        "73120": "Kanchanaburi",
        "73170": "Kanchanaburi",
        "70000": "Ratchaburi",
        "45000": "Udon Thani",
        "44000": "Nakhon Ratchasima",
        "32000": "Chaiyaphum",
        "24000": "Chon Buri",
        "20131": "Chon Buri",
        "15000": "Nakhon Pathom",
        "12120": "Nonthaburi",
        "18000": "Chachoengsao",
        "10520": "Samut Prakan",
        "10800": "Bangkok",
    }
    #query_thai["City"] = query_thai["Postcode"].apply(lambda x: postal_code_map.get(x, query_thai.loc[query_thai["Postcode"] != x, "City"].values[0]))
    query_thai["City"] = query_thai["Postcode"].map(postal_code_map).fillna(query_thai["City"])
    return query_thai
query_thai = thai(df)
st.write(query_thai)


@st.cache_data
def filter_provinces(query_thai):
    available_provinces = sorted(query_thai["City"].unique())
    available_provinces = [p for p in available_provinces if p in thailandProvinces]
    return available_provinces

available_provinces = filter_provinces(query_thai)

y = st.sidebar.selectbox("Choose a Province", available_provinces)


@st.cache_data
def map3d(query_thai,y):
    st.pydeck_chart(
        pdk.Deck(
            map_style=None,
            initial_view_state=pdk.ViewState(
                latitude=query_thai.query('City == @y')["Latitude"].mean(),
                longitude=query_thai.query('City == @y')["Longitude"].mean(),
                zoom=11,
                pitch=50,
            ),
            layers=[
                pdk.Layer(
                    "HexagonLayer",
                    data=query_thai,
                    get_position="[Longitude, Latitude]",
                    radius=200,
                    elevation_scale=4,
                    elevation_range=[0, 1000],
                    pickable=False,
                    extruded=True,
                ),
                pdk.Layer(
                    "ScatterplotLayer",
                    data=query_thai,
                    get_position="[Longitude, Latitude]",
                    get_color="[200, 30, 0, 160]",
                    get_radius=200,
                ),
            ],
        )
    )
map3d(query_thai,y)


