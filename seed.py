# Seed for ShareBnb
from sharebnb import create_app
from sharebnb.models import db, User, Property, Image

app = create_app("development")

with app.app_context():
    db.drop_all()
    db.create_all()

    # Users ##############################
    u1 = User(
        username="user-1",
        first_name="f_name-1",
        last_name="l_name-1",
        email="user1@test.com",
    )

    u2 = User(
        username="user-2",
        first_name="f_name-2",
        last_name="l_name-2",
        email="user2@test.com",
    )

    db.session.add_all([u1, u2])
    db.session.commit()

    # Properties ##############################
    p1 = Property(
        name="Sunny Oasis with Private Pool",
        description=(
            "Escape the summer heat and dive into your own private"
            + " paradise in our spacious backyard. Perfect"
            + " for relaxing with friends and family."
            ),
        price=60,
        address="123 Main Street, Sunnydale Suburb, CA, 98765",
        backyard=False,
        pool=True,
        user_id=1,
    )

    p2 = Property(
        name="Cozy Backyard Retreat",
        description=(
            "Discover serenity in our charming backyard retreat!"
            + " our cozy outdoor space offers a peaceful"
            + " escape from the hustle and bustle of city life."
        ),
        price=100,
        address="456 Elm Avenue, Oakwood Heights Suburb, NY, 54321",
        backyard=True,
        pool=False,
        user_id=1,
    )

    p3 = Property(
        name="Ultimate Outdoor Haven: Backyard & Pool Combo",
        description=(
            "Experience the best of both worlds in our ultimate outdoor haven!"
            + " We boast ample seating areas for lounging and entertaining."
        ),
        price=350,
        address="789 Oak Street, Maplewood Suburb, NJ, 67890",
        backyard=True,
        pool=True,
        user_id=2,
    )

    p4 = Property(
        name="Tranquil Garden Hideaway",
        description=(
            "Step into a serene garden hideaway and leave the stresses"
            + " of city life behind!"
        ),
        price=70,
        address="345 Willow Lane, Willow Creek Suburb, OR, 45678",
        backyard=False,
        pool=True,
        user_id=2,
    )

    p5 = Property(
        name="Sun-Kissed Pool Retreat",
        description=(
            "Indulge in the ultimate relaxation at our sun-kissed pool retreat!"
            + " Immerse yourself in crystal-clear waters and enjoy our spacious"
            + " deck."
        ),
        price=120,
        address="234 Palm Boulevard, Palm Grove Suburb, FL, 34567",
        backyard=False,
        pool=True,
        user_id=2,
    )

    db.session.add_all([p1, p2, p3, p4, p5])
    db.session.commit()

    # Images ##############################
    i1 = Image(
        property_id=1,
        storage_key="123",
        url=(
            "https://images.unsplash.com/"
            + "photo-1536745511564-a5fa6e596e7b?q=80&w=992&auto=format&fit"
            + "=crop&ixlib=rb-4.0.3&ixid="
            + "M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        ),
    )

    i2 = Image(
        property_id=2,
        storage_key="456",
        url=(
            "https://images.unsplash.com/photo-1560749003-f4b1e17e2dff"
            + "?q=80&w=1674&auto=format&fit=crop&ixlib=rb-4.0.3"
            + "&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        ),
    )

    i3 = Image(
        property_id=3,
        storage_key="333",
        url=(
            "https://images.unsplash.com/photo-1576013551627"
            + "-0cc20b96c2a7?q=80&w=2670&auto=format&fit=crop&ixlib=rb-4.0.3&ixid"
            + "=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        ),
    )

    i4 = Image(
        property_id=4,
        storage_key="444",
        url=(
            "https://images.unsplash.com/photo-1611282712338-63a58e27980a?q="
            + "80&w=2670&auto=format&fit=crop&ixlib=rb-4.0.3&ixid="
            + "M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        ),
    )

    i5 = Image(
        property_id=5,
        storage_key="555",
        url=(
            "https://images.unsplash.com/photo-1601560896164-834d6f61ea66?"
            + "q=80&w=1742&auto=format&fit=crop&ixlib=rb-4.0.3&ixid="
            + "M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"
        ),
    )

    db.session.add_all([i1, i2, i3, i4, i5])
    db.session.commit()
