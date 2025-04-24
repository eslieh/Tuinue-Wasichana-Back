from datetime import datetime

class Donor:
    def __init__(self, id, name, email, phone=None, address=None, is_anonymous=False, donation_frequency='one-time', created_at=None, updated_at=None):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address
        self.is_anonymous = is_anonymous
        self.donation_frequency = donation_frequency
        self.created_at = created_at if created_at else datetime.now()
        self.updated_at = updated_at if updated_at else datetime.now()

    def __str__(self):
        return f"Donor(id={self.id}, name={self.name}, email={self.email}, anonymous={self.is_anonymous}, frequency={self.donation_frequency})"

    def update_contact_info(self, phone=None, address=None):
        if phone:
            self.phone = phone
        if address:
            self.address = address

    def set_anonymous(self, is_anonymous):
        self.is_anonymous = is_anonymous
        self.updated_at = datetime.now()

    def set_donation_frequency(self, frequency):
        self.donation_frequency = frequency
        self.updated_at = datetime.now()
