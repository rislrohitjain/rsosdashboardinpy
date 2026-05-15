import pandas as pd
import numpy as np
import os  # <--- ADD THIS LINE
import random
import string
from datetime import datetime, timedelta

def generate_synthetic_data(num_records=500):
   
    # Ensure folder exists
    if not os.path.exists('static'):
        os.makedirs('static')
        
    # Setup categorical options (Placeholder values similar to your domain)
    districts = ['Jaipur', 'Jodhpur', 'Udaipur', 'Bikaner', 'Kota', 'Ajmer', 'Alwar']
    genders = ['Male(पुरुष)', 'Female(महिला)', 'Other(अन्य)']
    religions = ['Hindu(हिंदू)', 'Muslim(मुसलमान)', 'Sikh(सिख)', 'Christian(ईसाई)', 'Buddhist(बौद्ध)']
    subjects = ['Mathematics (211)', 'Hindi (201)', 'English (202)', 'Science (212)', 'Social Science (213)']
    categories = ['GEN(जनरल )', 'OBC(अन्य पिछड़ा वर्ग )', 'SC(अनुसूचित जाति)', 'ST(अनुसूचित जनजाति)']
    courses = ['10th', '12th']
    streams = ['Stream-July', 'Stream-March', 'Stream-October']

    data = []

    for i in range(num_records):
        # Generate random names
        first_name = "".join(random.choices(string.ascii_uppercase, k=6))
        last_name = "".join(random.choices(string.ascii_uppercase, k=6))
        
        # Generate random dates (Age 15 to 30)
        start_date = datetime(1994, 1, 1)
        end_date = datetime(2009, 1, 1)
        dob = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        
        record = {
            'student_internal_id': 2000000 + i,
            'application_internal_id': 3000000 + i,
            'enrollment': 10000000000 + i,
            'ssoid': f"testuser_{i}",
            'student_code': 7000 + i,
            'ack_number': 161010000000 + i,
            'ai_code': 50000 + (i % 50),
            'student_name': f"{first_name} {last_name}",
            'first_name': first_name,
            'last_name': last_name,
            'father_name': "FATHER_" + "".join(random.choices(string.ascii_uppercase, k=5)),
            'mother_name': "MOTHER_" + "".join(random.choices(string.ascii_uppercase, k=5)),
            'date_of_birth': dob.strftime('%Y-%m-%d'),
            'gender_label': random.choice(genders),
            'religion_label': random.choice(religions),
            'mobile': int("9" + "".join(random.choices(string.digits, k=9))),
            'email': f"student_{i}@example.com",
            'aadhar_number': int("2" + "".join(random.choices(string.digits, k=11))),
            'district_name': random.choice(districts),
            'course_name': random.choice(courses),
            'stream_name': random.choice(streams),
            'subject_name': random.choice(subjects),
            'category_label': random.choice(categories),
            'rural_urban_label': random.choice(['Rural(ग्रामीण)', 'Urban(शहरी)']),
            'employment_status_label': random.choice(['Employed(कार्यरत)', 'Un-Employed(बेरोजगार)']),
            'fee_paid_amount': random.choice([2000, 2500, 3140, 4500]),
            'verifier_status_label': 'Pending',
            'college_name': f"Govt. Senior Sec. School, {random.choice(districts)}",
            'is_eligible': 1
        }
        data.append(record)

    # Create DataFrame
    df = pd.DataFrame(data)

    # Export to Excel
    # Export to the static folder
    file_name = "static/sample_for_dashboard.xlsx"
    df.to_excel(file_name, index=False)
     
    file_path = os.path.join('static', 'sample_for_dashboard.xlsx')
    df.to_excel(file_path, index=False)
    return file_path 