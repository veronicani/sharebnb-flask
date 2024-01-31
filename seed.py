# Seed for ShareBnb
from app import app
from models import db, User, Property, Image

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
    name="Pool-1",
    description="description-1",
    price=10,
    address="address-1",
    backyard=False,
    pool=True,
    user_id=1,
)

p2 = Property(
    name="Backyard-1",
    description="description-2",
    price=100,
    address="address-2",
    backyard=True,
    pool=False,
    user_id=1,
)

p3 = Property(
    name="BackyardPool",
    description="got both!",
    price=1000,
    address="address-3",
    backyard=True,
    pool=True,
    user_id=2,
)

db.session.add_all([p1, p2, p3])
db.session.commit()