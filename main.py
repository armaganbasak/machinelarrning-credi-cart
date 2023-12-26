import streamlit as st
st.set_page_config(layout="wide")
import pandas as pd
import plotly.express as px
import joblib
@st.cache_data
def get_data():
    df = pd.read_csv("datasets/clean_dataset.csv")
    df['PriorDefault'].replace({1: 0, 0: 1}, inplace=True)
    return df


def get_model():
    model = joblib.load("gapminder_model.joblib")
    return model



st.header("🏦 :blue[Kredi Kartı Onay Tahmin Sistemi] 🏦")
tab_home,tab_model = st.tabs(["Ana Sayfa","Model"])

#st.subheader()
#st.markdown()
#st.image() resim eklemek

column_1,column_2 = tab_home.columns(2)

column_1.markdown('''Kredi kartı başvuruları, finansal dünyada önemli bir adımdır ve başvuru sonuçlarını beklemek pek çok kişi için heyecan verici, ancak bir o kadar da stresli bir deneyim olabilir. Biz, bu stresi ortadan kaldırmak ve kullanıcılarımıza anında bilgi sağlamak için bir makine öğrenmesi modeli geliştirdik.

Artık kredi kartı başvurularınızın olumlu ya da olumsuz olma olasılığını hemen öğrenebilir, finansal geleceğinizi anlık olarak değerlendirebilirsiniz. Bu yenilikçi çözüm sayesinde, kredi kartı başvurularınızın sonuçlarına dair belirsizlikleri geride bırakın. Finansal geleceğinizi şekillendirmek için adım atın, hedeflerinize bir adım daha yaklaşın!
''')

column_1.image("banka.jpg")
df = get_data()
column_2.dataframe(df,width=1000)





#TAB MODEL

model = get_model()



bankcust = tab_model.radio("Banka müşterisi misiniz?", ["Evet", "Hayır"])
employed = tab_model.radio("Çalışıyor musunuz?", ["Evet", "Hayır"])
married = tab_model.radio("Evli misiniz?", ["Evet", "Hayır"])
income = tab_model.number_input("Yıllık Gelir Giriniz",min_value = 0,max_value = 100000000,step = 500,value=0)
cscore = tab_model.number_input("Kredi Skorunuzu giriniz",min_value = 0,max_value = 1800,step = 10,value=0)
debt  = tab_model.number_input("Borç giriniz",min_value = 0.0,max_value = 1000000000.0,step = 500.0,value=0.0)
yearsemp = tab_model.number_input("Kac yıldır calısıyorsunuz?",min_value = 0,max_value = 100,step = 1,value=0)
age =  tab_model.number_input("Kac yasındasınız?",min_value = 0,max_value = 150,step = 1,value=0)
priordef = tab_model.radio("Temerrüte Düşme Durumu?", ["Evet", "Hayır"])


bankcust = 1 if bankcust == "Evet" else 0
employed = 1 if employed ==  "Evet" else 0
married = 1 if married == "Evet" else 0
priordef = 1 if priordef == "Evet" else 0



user_input = pd.DataFrame({'BankCustomer':bankcust,'Employed':employed,'Married':married,'Income':income,'CreditScore':cscore, 'Debt':debt,'YearsEmployed':yearsemp,'Age':age,'PriorDefault':priordef},index=[0])



if tab_model.button("Tahmin yap!"):
    prediction = model.predict(user_input)
    print(f"Model prediction: {prediction}")
    if prediction[0] == 1:
        tab_model.success("Kredi Kartı Onaylandı!")
        st.balloons()
    else:
        tab_model.error("Kredi Kartı Onaylanamadı!")
