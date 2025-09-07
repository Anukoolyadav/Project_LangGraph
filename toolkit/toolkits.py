import pandas as pd
from typing import Literal
from langchain_core.tools import tool
from data_models.models import *

@tool
def check_availability_by_doctor(desired_date: DateModel, doctor_name: Literal['kevin anderson', 'robert martinez', 'susan davis', 'daniel miller', 'sarah wilson', 'michael green', 'lisa brown', 'jane smith', 'emily johnson', 'john doe']):
    """Checks the database for a specific doctor's availability on a given date."""
    df = pd.read_csv("data/doctor_availability.csv")
    df['date_slot_time'] = df['date_slot'].apply(lambda x: x.split(' ')[1])
    rows = df[(df['date_slot'].str.startswith(desired_date.date)) & (df['doctor_name'] == doctor_name) & (df['is_available'] == True)]['date_slot_time'].tolist()
    if not rows:
        return f"Doctor {doctor_name} has no availability on {desired_date.date}."
    return f"Doctor {doctor_name} is available on {desired_date.date} at the following times: {', '.join(rows)}"

@tool
def set_appointment(desired_date: DateTimeModel, id_number: IdentificationNumberModel, doctor_name: Literal['kevin anderson', 'robert martinez', 'susan davis', 'daniel miller', 'sarah wilson', 'michael green', 'lisa brown', 'jane smith', 'emily johnson', 'john doe']):
    """Sets an appointment for a patient with a specific doctor at a given date and time."""
    df = pd.read_csv("data/doctor_availability.csv")
    mask = (df['date_slot'] == desired_date.date) & (df['doctor_name'] == doctor_name) & (df['is_available'] == True)
    if not df[mask].empty:
        df.loc[mask, ['is_available', 'patient_to_attend']] = [False, id_number.id]
        df.to_csv("data/doctor_availability.csv", index=False)
        return f"Appointment successfully booked for patient ID {id_number.id} with Dr. {doctor_name} on {desired_date.date}."
    return "This slot is not available for booking."

@tool
def cancel_appointment(date: DateTimeModel, id_number: IdentificationNumberModel, doctor_name: Literal['kevin anderson', 'robert martinez', 'susan davis', 'daniel miller', 'sarah wilson', 'michael green', 'lisa brown', 'jane smith', 'emily johnson', 'john doe']):
    """Cancels an existing appointment for a patient."""
    df = pd.read_csv("data/doctor_availability.csv")
    mask = (df['date_slot'] == date.date) & (df['patient_to_attend'] == id_number.id) & (df['doctor_name'] == doctor_name)
    if not df[mask].empty:
        df.loc[mask, ['is_available', 'patient_to_attend']] = [True, ""]
        df.to_csv("data/doctor_availability.csv", index=False)
        return "Appointment successfully cancelled."
    return "No matching appointment found to cancel."
