# seed.py

from app import app
from models import db, Admin, Donor, Charity, CharityApplication, Donation, Story, Inventory

def seed_data():
    with app.app_context():
        print("Dropping all tables...")
        db.drop_all()
        print("Creating all tables...")
        db.create_all()

        print("Seeding data...")

        # Create an Admin user
        admin1 = Admin(
            name="Admin",
            email="admin@gmail.com",
            user_type="admin",
            is_verified=True
        )
        admin.set_password("Admin123")

        # Create Donors
        donor1 = Donor(
            name="Jane",
            email="jane@gmail.com",
            user_type="donor",
            is_verified=True,
            reminder_enabled=True,
            anonymous_donor=False,
            donation_frequency="monthly"
        )
        donor1.set_password("JaneDonor123")

        donor2 = Donor(
            name="John",
            email="john@gmail.com",
            user_type="donor",
            is_verified=True,
            reminder_enabled=True,
            anonymous_donor=False,
            donation_frequency="monthly"
        )
        donor2.set_password("JohnDonor123")

        

        # Create Charity users
        charity1 = Charity(
            name="AFRIpads Foundation",
            email="afripads@charity.org",
            user_type="charity",
            is_verified=True,
            organisation_name="AFRIpads Foundation",
            organisation_description="Manufactures reusable sanitary pads in Africa and empowers women and girls through access and education on menstrual health.",
            logo_url="https://www.afripadsfoundation.org/wp-content/uploads/2021/10/logo-afripads-foundation.png",
            approved=True
        )
        charity1.set_password("AFRIpads123")

        charity2 = Charity(
            name="ZanaAfrica Foundation",
            email="zana@charity.org",
            user_type="charity",
            is_verified=True,
            organisation_name="ZanaAfrica Foundation",
            organisation_description="Providing Kenyan adolescent girls with sanitary pads and reproductive health education to empower them.",
            logo_url="https://images.squarespace-cdn.com/content/v1/5533c2bfe4b09a66347a97ae/1447286966437-2HCS7T55860O4QIL8I5H/image-asset.jpeg",
            approved=True
        )
        charity2.set_password("ZanaFoundation123")

        charity3 = Charity(
            name="The Pad Project",
            email="padproject@charity.org",
            user_type="charity",
            is_verified=True,
            organisation_name="The Pad Project",
            organisation_description="Working globally to increase access to menstrual products, fight stigma, and advance menstrual equity.",
            logo_url="https://thepadproject.org/wp-content/uploads/2024/06/TPP_Logo.png",
            approved=True
        )
        charity3.set_password("Padproject123")

        charity4 = Charity(
            name="Days for Girls Kenya",
            email="daysforgirlskenya@charity.org",
            user_type="charity",
            is_verified=True,
            organisation_name="Days for Girls Kenya",
            organisation_description="Provides sustainable menstrual health solutions and education to women and girls worldwide.",
            logo_url="https://www.daysforgirls.org/wp-content/uploads/2021/12/Kenya-light-background-1.png",
            approved=True
        )
        charity4.set_password("Daysforgirls254")

        charity5 = Charity(
            name="Huru International",
            email="huruinternational@charity.org",
            user_type="charity",
            is_verified=True,
            organisation_name="Huru International",
            organisation_description="Fighting period poverty in Africa by distributing reusable pads and providing menstrual health education to keep girls in school.",
            logo_url="https://togetherwomenrise.org/wp-content/uploads/2014/01/Huru-Logo.png",
            approved=True
        )
        charity5.set_password("Huruinternational123")

        charity6 = Charity(
            name="I Support The Girls",
            email="isupportthegirls@charity.org",
            user_type="charity",
            is_verified=True,
            organisation_name="I Support The Girls",
            organisation_description="Collects and distributes essential items, including menstrual products, to girls and women facing hardship globally.",
            logo_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSejkFMkcZL-rKYkoKdQh0PlyhljfJDlouGDg&s",
            approved=True
        )
        charity6.set_password("Isupport254")

        # Create Donations
        donation1 = Donation(
            amount=500,
            is_recurring=True,
            is_anonymous=False,
            status="completed",
            donor=donor1,
            charity=charity1
        )

        donation2 = Donation(
            amount=200,
            is_recurring=False,
            is_anonymous=True,
            status="pending",
            donor=donor2,
            charity=charity2
        )

        # Create Story
        story1 = Story(
            charity=charity1,
            title="Amina's Dreams Bloom",
            content="For 14-year-old Amina in rural Kenya, school attendance was a monthly struggle until AFRIpads provided her with sanitary pads and vital health education. Now, with dignity and confidence, Amina no longer misses class and is focused on her dream of becoming a teacher, her potential finally blooming.",
            image_url="https://assets.isu.pub/document-structure/221214093420-51f7d1372d69518146dbf2bee5a3f799/v1/62c7d3a524111c640c2a47b0bd4a4628.jpeg"
        )
        story2 = Story(
            charity=charity2,
            title="Breaking the Silence in Meru",
            content="In a small town in Meru, Sarah, a high school student, felt isolated due to lack of access to period products. Thanks to a local initiative supported by ZanaAfrica Foundation, her school now has a menstrual product dispenser in the restrooms. Sarah no longer feels ashamed and can fully participate in her education, breaking the silence around menstruation.",
            image_url="https://images.squarespace-cdn.com/content/v1/62d03eea82f8f40a3af66f78/293eadb0-9dea-435e-afb6-789116514d8c/IMG_2638.jpg"
        )
        story3 = Story(
            charity=charity3,
            title="A Kit of Malindi",
            content="Maya in Malindi received a The Pad Project reusable pad kit and health training. This simple kit not only provided her with a sustainable solution for managing her period but also empowered her with knowledge about her body. Now, Maya feels healthy, attends school consistently, and shares her knowledge with other girls in her village, spreading hope.",
            image_url="https://www.daysforgirls.org/wp-content/uploads/2020/11/1150cf_902eba4a7316478d9ff1ad54637e096bmv2.jpg"
        )
        story4 = Story(
            charity=charity4,
            title="No More Missed Days for Abimbola",
            content="Abimbola, a bright student in rural Kenya, used to miss several school days each month due to her period. Days for Girls Kenya's provision of reusable sanitary pads and comprehensive education changed everything. Now, Abimbola attends school regularly, her grades have improved, and she is determined to become a doctor.",
            image_url="https://www.daysforgirls.org/wp-content/uploads/2021/12/2019-Kenya_DfG-Farmers-Helping-Farmers-by-Krystal-Woodside-1-752x564.jpg"
        )
        story5 = Story(
            charity=charity5,
            title="Dignity Restored in a Shelter",
            content="Living in a shelter, 16-year-old Layla in Kiambu often felt her dignity stripped away. When Huru International provided her with a care package containing bras and menstrual hygiene products, it was more than just supplies; it was a message of care and respect, helping Layla feel more confident and supported during a difficult time.",
            image_url="https://images.squarespace-cdn.com/content/v1/62e296d22352496d44278e34/1667584884454-4MOUVJR15CCDF951W7D0/CJ-222-%281%29.jpg"
        )
        story6 = Story(
            charity=charity6,
            title="Empowerment Through Enterprise in Nairobi",
            content="Through I Support The Girls' initiatives, not only did Nkatha in Nairobi receive reusable sanitary pads, but her mother also became part of a local enterprise producing them. This provided the family with income and empowered both mother and daughter, ensuring sustainable access to menstrual hygiene and improved livelihoods.",
            image_url="https://asec-sldi.org/contentAsset/image/af0aea4b-5902-4ef9-82d2-b1c0ee6257b3/binaryImage/filter/Resize,Jpeg/jpeg_q/65/resize_w/825/v/510f39b3-79ca-4139-a150-fa006d85215f/"
        )

        # Create Inventory
        inventory1 = Inventory(
            charity=charity1,
            product="Sanitary Pads",
            product_quantity=100,
            beneficiary_name="Light Childrens' Home"
        )
        inventory2 = Inventory(
            charity=charity2,
            product="Sanitary Pads",
            product_quantity=250,
            beneficiary_name="Meru Girls' Highschool"
        )
        inventory3 = Inventory(
            charity=charity3,
            product="Sanitary Pads",
            product_quantity=150,
            beneficiary_name="Tawheed Girls' Secondary School"
        )
        inventory4 = Inventory(
            charity=charity4,
            product="Sanitary Pads",
            product_quantity=300,
            beneficiary_name="Iwobi Childrens' Home"
        )
        inventory5 = Inventory(
            charity=charity5,
            product="Sanitary Pads",
            product_quantity=50,
            beneficiary_name="Kambui Girls' Secondary School"
        )
        inventory6 = Inventory(
            charity=charity6,
            product="Sanitary Pads",
            product_quantity=75,
            beneficiary_name="Good Samaritan Childrens' Home"
        )

        # Add everything to the session
        db.session.add_all([admin, donor, charity, donation1, donation2, story, inventory])
        db.session.commit()

        print("Database seeded successfully.")

if __name__ == "__main__":
    seed_data()
