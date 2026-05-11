import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta
import os

# -------------------- SOZLAMALAR --------------------
fake = Faker('uz_UZ')
random.seed(42)
np.random.seed(42)

# -------------------- 1. DIM_DATE --------------------
start_date = datetime(2020, 1, 1)
end_date = datetime(2024, 12, 31)
date_list = pd.date_range(start=start_date, end=end_date, freq='D')

dim_date = pd.DataFrame({
    'Date_Key': range(1, len(date_list) + 1),
    'Full_Date': date_list,
    'Year': date_list.year,
    'Quarter': 'Q' + date_list.quarter.astype(str),
    'Month_Name': date_list.strftime('%B'),
    'Is_Weekend': date_list.dayofweek >= 5
})

# -------------------- 2. DIM_REGION (Shape Map uchun) --------------------
# `uz.json` faylidagi name maydonlariga to‘liq mos
regions_eng = [
    'Tashkent',          # Toshkent shahri (shape map da ikkala Toshkent birlashadi)
    'Tashkent',          # Toshkent viloyati
    'Samarkand',
    'Bukhoro',
    'Andijon',
    'Ferghana',
    'Namangan',
    'Kashkadarya',
    'Surkhandarya',
    'Khorezm',
    'Navoi',
    'Jizzakh',
    'Sirdaryo',
    'Karakalpakstan'
]

regions_uz = [
    'Toshkent shahri',
    'Toshkent viloyati',
    'Samarqand viloyati',
    'Buxoro viloyati',
    'Andijon viloyati',
    "Farg'ona viloyati",
    'Namangan viloyati',
    'Qashqadaryo viloyati',
    'Surxondaryo viloyati',
    'Xorazm viloyati',
    'Navoiy viloyati',
    'Jizzax viloyati',
    'Sirdaryo viloyati',
    "Qoraqalpog'iston Respublikasi"
]

dim_region = pd.DataFrame({
    'Region_ID': range(1, 15),
    'Region_Name_Uz': regions_uz,
    'Region_Name_Eng': regions_eng
})

# -------------------- 3. DIM_BRANCHES (Region_ID bilan) --------------------
cities_uz = [
    'Toshkent', 'Nurafshon', 'Samarqand', 'Buxoro', 'Andijon',
    'Farg‘ona', 'Namangan', 'Qarshi', 'Termiz', 'Urganch',
    'Navoiy', 'Jizzax', 'Guliston', 'Nukus'
]

branch_names = [f"Aloqa Bank {city} filiali" for city in cities_uz]

lats = [41.2995, 41.0442, 39.6542, 39.7747, 40.7841, 40.3842,
        40.9983, 38.8606, 37.2242, 41.5519, 40.0844, 40.1158, 40.4906, 42.4647]
lons = [69.2401, 69.3090, 66.9597, 64.4282, 72.3425, 71.7849,
        71.6721, 65.7891, 67.2753, 60.6324, 65.3783, 67.8567, 68.7858, 59.6166]

targets = [
    2_500_000_000, 1_800_000_000, 1_200_000_000, 1_000_000_000,
    900_000_000, 950_000_000, 800_000_000, 1_100_000_000,
    700_000_000, 750_000_000, 850_000_000, 700_000_000,
    600_000_000, 650_000_000
]

# Region_ID: 1-Toshkent sh, 2-Toshkent vil, 3-Samarqand, ...
region_ids = list(range(1, 15))

dim_branches = pd.DataFrame({
    'Branch_ID': range(1, 15),
    'Branch_Name': branch_names,
    'City_Uz': cities_uz,
    'Latitude': lats,
    'Longitude': lons,
    'Target_Quarter': targets,
    'Region_ID': region_ids
})

# -------------------- 4. DIM_CUSTOMERS (Region_ID bilan) --------------------
n_customers = 50_000
occupations = ['O‘qituvchi', 'Shifokor', 'Muhandis', 'Dasturchi', 'Tadbirkor',
               'Ishlab chiqaruvchi', 'Talaba', 'Nafaqaxo‘r', 'Huquqshunos',
               'Hisobchi', 'Savdogar', 'Boshqa']

customers_data = []
for i in range(1, n_customers + 1):
    age = random.randint(18, 80)
    # Mijozning yashash hududi (region)
    region_id = random.choice(region_ids)
    customers_data.append({
        'Customer_ID': i,
        'Full_Name': fake.name(),
        'Age': age,
        'Gender': random.choice(['Erkak', 'Ayol']),
        'Occupation': random.choice(occupations),
        'Is_Active': random.choices([True, False], weights=[0.9, 0.1])[0],
        'Region_ID': region_id
    })
dim_customers = pd.DataFrame(customers_data)

# -------------------- 5. DIM_PRODUCTS --------------------
products = [
    {'Product_Name': 'Humo kartasi', 'Category': 'Karta', 'Service_Fee': 15000},
    {'Product_Name': 'UzCard', 'Category': 'Karta', 'Service_Fee': 12000},
    {'Product_Name': 'Visa Gold', 'Category': 'Karta', 'Service_Fee': 25000},
    {'Product_Name': 'Mastercard Standard', 'Category': 'Karta', 'Service_Fee': 20000},
    {'Product_Name': 'Avtokredit', 'Category': 'Kredit', 'Service_Fee': 50000},
    {'Product_Name': 'Ipoteka', 'Category': 'Kredit', 'Service_Fee': 100000},
    {'Product_Name': 'Iste’mol krediti', 'Category': 'Kredit', 'Service_Fee': 30000},
    {'Product_Name': 'Kredit karta', 'Category': 'Kredit', 'Service_Fee': 40000},
    {'Product_Name': 'Omonat (Depozit)', 'Category': 'Omonat', 'Service_Fee': 0},
    {'Product_Name': 'Kumulyativ omonat', 'Category': 'Omonat', 'Service_Fee': 0},
    {'Product_Name': 'Kommunal to‘lov', 'Category': 'To‘lovlar', 'Service_Fee': 2000},
    {'Product_Name': 'Internet to‘lov', 'Category': 'To‘lovlar', 'Service_Fee': 1500},
    {'Product_Name': 'Mobil aloqa to‘lovi', 'Category': 'To‘lovlar', 'Service_Fee': 1000},
    {'Product_Name': 'Pul o‘tkazmasi', 'Category': 'To‘lovlar', 'Service_Fee': 5000},
    {'Product_Name': 'Valyuta ayirboshlash', 'Category': 'To‘lovlar', 'Service_Fee': 10000}
]
dim_products = pd.DataFrame(products)
dim_products.insert(0, 'Product_ID', range(1, len(products) + 1))

# -------------------- 6. DIM_CHANNEL (yangi) --------------------
channels = [
    {'Channel_ID': 1, 'Channel_Name': 'Mobile App', 'Channel_Type': 'Raqamli'},
    {'Channel_ID': 2, 'Channel_Name': 'Web Banking', 'Channel_Type': 'Raqamli'},
    {'Channel_ID': 3, 'Channel_Name': 'ATM', 'Channel_Type': 'O‘ziga xizmat'},
    {'Channel_ID': 4, 'Channel_Name': 'Filial', 'Channel_Type': 'Ofis'},
    {'Channel_ID': 5, 'Channel_Name': 'Call Center', 'Channel_Type': 'Raqamli'}
]
dim_channel = pd.DataFrame(channels)

# -------------------- 7. DIM_LOANS (kreditlar) --------------------
# Faol mijozlarning 30% kredit olgan, ba'zilari bir necha
active_customers = dim_customers[dim_customers['Is_Active'] == True]['Customer_ID'].tolist()
loan_customers = random.choices(active_customers, k=int(len(active_customers) * 0.3))
n_loans = len(loan_customers) + random.randint(0, len(loan_customers)//2)

loans_data = []
date_keys = dim_date['Date_Key'].tolist()
for loan_id in range(1, n_loans + 1):
    cust_id = random.choice(loan_customers)
    loan_amount = random.randint(1_000_000, 500_000_000)
    interest_rate = round(random.uniform(10, 30), 1)
    start_date_key = random.choice(date_keys[:-180])
    start_date = dim_date[dim_date['Date_Key'] == start_date_key]['Full_Date'].iloc[0]
    end_date = start_date + timedelta(days=random.randint(365, 5*365))
    npl_status = random.choices(['Ha', 'Yo‘q'], weights=[0.15, 0.85])[0]
    if npl_status == 'Ha':
        remaining_debt = loan_amount * random.uniform(0.5, 0.95)
    else:
        remaining_debt = loan_amount * random.uniform(0, 0.5)
    remaining_debt = round(remaining_debt, 2)
    loans_data.append({
        'Loan_ID': loan_id,
        'Customer_ID': cust_id,
        'Loan_Amount': loan_amount,
        'Interest_Rate': interest_rate,
        'Start_Date': start_date,
        'End_Date': end_date,
        'NPL_Status': npl_status,
        'Remaining_Debt': remaining_debt
    })
dim_loans = pd.DataFrame(loans_data)

# -------------------- 8. FACT_TRANSACTIONS (Channel_ID qo'shilgan) --------------------
n_transactions = 1_000_000
date_keys_list = dim_date['Date_Key'].tolist()
customer_ids = dim_customers['Customer_ID'].tolist()
branch_ids = dim_branches['Branch_ID'].tolist()
product_ids = dim_products['Product_ID'].tolist()
channel_ids = dim_channel['Channel_ID'].tolist()

transaction_types = ['Kirim', 'Chiqim']
statuses = ['Muvaffaqiyatli', 'Xatolik', 'Kutilmoqda']
status_weights = [0.9, 0.05, 0.05]

def get_amount(trans_type):
    if trans_type == 'Kirim':
        return random.randint(50_000, 10_000_000)
    else:
        return random.randint(10_000, 5_000_000)

# Filial og'irliklari (Toshkent sh. eng ko'p)
branch_weights = [0.25, 0.15, 0.08, 0.06, 0.05, 0.05, 0.04, 0.06, 0.04, 0.04, 0.04, 0.04, 0.03, 0.03]
channel_weights = [0.45, 0.25, 0.15, 0.10, 0.05]  # Mobile eng ko'p

transactions_data = []
for txn_id in range(1, n_transactions + 1):
    trans_type = random.choice(transaction_types)
    branch_id = random.choices(branch_ids, weights=branch_weights)[0]
    channel_id = random.choices(channel_ids, weights=channel_weights)[0]
    transactions_data.append({
        'Transaction_ID': txn_id,
        'Date_Key': random.choice(date_keys_list),
        'Customer_ID': random.choice(customer_ids),
        'Branch_ID': branch_id,
        'Product_ID': random.choice(product_ids),
        'Channel_ID': channel_id,
        'Amount': get_amount(trans_type),
        'Transaction_Type': trans_type,
        'Status': random.choices(statuses, weights=status_weights)[0]
    })
    if txn_id % 100_000 == 0:
        print(f"{txn_id} tranzaksiya yaratildi...")
fact_transactions = pd.DataFrame(transactions_data)

# -------------------- 9. FACT_LOAN_PAYMENTS (yangi) --------------------
# Har bir kredit uchun oylik to'lovlar (3-60 oy)
loan_ids = dim_loans['Loan_ID'].tolist()
payments_data = []
payment_id = 1
for loan_id in loan_ids:
    loan = dim_loans[dim_loans['Loan_ID'] == loan_id].iloc[0]
    loan_amount = loan['Loan_Amount']
    start_date = loan['Start_Date']
    end_date = loan['End_Date']
    npl = loan['NPL_Status']
    # To'lovlar soni (oylik)
    months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
    if months < 1:
        months = 1
    # Oddiy annuitet to'lovi (soddalashtirilgan)
    monthly_payment = loan_amount / months * random.uniform(0.8, 1.2)
    for m in range(1, months + 1):
        payment_date = start_date + timedelta(days=30*m)
        # NPL bo'lsa, ba'zi to'lovlar o'tkazib yuborilgan
        if npl == 'Ha' and random.random() < 0.4:
            continue  # to'lov qilinmagan
        principal = monthly_payment * random.uniform(0.7, 0.9)
        interest = monthly_payment - principal
        payments_data.append({
            'Payment_ID': payment_id,
            'Loan_ID': loan_id,
            'Payment_Date': payment_date,
            'Payment_Amount': round(monthly_payment, 2),
            'Principal': round(principal, 2),
            'Interest': round(interest, 2)
        })
        payment_id += 1
        if payment_id % 50000 == 0:
            print(f"{payment_id} to'lov yozuvi yaratildi...")
fact_loan_payments = pd.DataFrame(payments_data)

# -------------------- CSV GA SAQLASH --------------------
output_dir = "aloqa_bank_9_tables"
os.makedirs(output_dir, exist_ok=True)

dim_date.to_csv(f"{output_dir}/Dim_Date.csv", index=False)
dim_region.to_csv(f"{output_dir}/Dim_Region.csv", index=False)
dim_branches.to_csv(f"{output_dir}/Dim_Branches.csv", index=False)
dim_customers.to_csv(f"{output_dir}/Dim_Customers.csv", index=False)
dim_products.to_csv(f"{output_dir}/Dim_Products.csv", index=False)
dim_channel.to_csv(f"{output_dir}/Dim_Channel.csv", index=False)
dim_loans.to_csv(f"{output_dir}/Dim_Loans.csv", index=False)
fact_transactions.to_csv(f"{output_dir}/Fact_Transactions.csv", index=False)
fact_loan_payments.to_csv(f"{output_dir}/Fact_LoanPayments.csv", index=False)

print("\n✅ Barcha 9 ta jadval yaratildi!")
print("Fayllar:", os.listdir(output_dir))

# Fayl hajmlari
for f in os.listdir(output_dir):
    size_mb = os.path.getsize(f"{output_dir}/{f}") / (1024*1024)
    print(f"{f}: {size_mb:.2f} MB")