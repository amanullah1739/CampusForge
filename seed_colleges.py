from app import app
from database import db
from database.models.college import College


colleges = [
    "IIT Roorkee",
    "NIT Uttarakhand",
    "GBPUAT, Pantnagar",
    "BTKIT Dwarahat",
    "THDC-IHET, Tehri",
    "VMSB Uttarakhand Technical University, Dehradun",
    "UPES, Dehradun",
    "Graphic Era Deemed to be University, Dehradun",
    "DIT University, Dehradun",
    "Uttaranchal University, Dehradun",
    "College of Engineering Roorkee (COER)",
    "Quantum University, Roorkee",
    "Tula's Institute, Dehradun",
    "Dev Bhoomi Uttarakhand University (DBUU)",
    "Roorkee Institute of Technology (RIT)",
    "Shivalik College of Engineering, Dehradun",
    "Beehive College of Engineering & Technology",
    "CampusForge Demo College"
]


with app.app_context():

    for college_name in colleges:

        existing = College.query.filter_by(
            name=college_name
        ).first()

        if not existing:

            college = College(
                name=college_name,
                email=f"{college_name.lower().replace(' ', '')}@campusforge.local"
            )

            db.session.add(college)

    db.session.commit()

    print("Colleges seeded successfully.")