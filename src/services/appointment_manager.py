class AppointmentManager:
    def __init__(self):
        # Aqui viria a conexão com o sistema Java existente
        self.appointments = {
            "12345": [
                {"date": "2024-01-15", "time": "14:30", "doctor": "Dr. Silva", "specialty": "Cardiologia"},
                {"date": "2024-01-20", "time": "10:00", "doctor": "Dra. Costa", "specialty": "Dermatologia"}
            ]
        }
    
    def handle_appointment_request(self, user_id, message):
        message_lower = message.lower()
        
        if 'agendar' in message_lower or 'marcar' in message_lower:
            return "Para agendar uma consulta, entre em contato com nossa central pelo telefone (11) 1234-5678"
        elif 'cancelar' in message_lower:
            return "Para cancelar uma consulta, ligue para (11) 1234-5678 ou acesse o portal do paciente"
        else:
            next_appt = self.get_next_appointment(user_id)
            if next_appt:
                return f"Sua próxima consulta: {next_appt['date']} às {next_appt['time']} com {next_appt['doctor']}"
            else:
                return "Não encontrei agendamentos para você."
    
    def get_next_appointment(self, patient_id):
        # Simulação - na prática, integraria com o sistema Java
        if patient_id in self.appointments and self.appointments[patient_id]:
            return self.appointments[patient_id][0]
        return None
    
    def confirm_appointment(self, patient_id, appointment_date):
        # confirmar consulta
        return True
    
    def cancel_appointment(self, patient_id, appointment_date):
        # cancelar consulta
        return True