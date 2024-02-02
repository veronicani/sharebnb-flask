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
    name="Backyard and Pool",
    description="We have both!",
    price=1000,
    address="address-3",
    backyard=True,
    pool=True,
    user_id=2,
)

db.session.add_all([p1, p2, p3])
db.session.commit()

# Images ##############################
i1 = Image(
    property_id=1,
    aws_key="123",
    url=("https://images.unsplash.com/" +
        "photo-1536745511564-a5fa6e596e7b?q=80&w=992&auto=format&fit" +
        "=crop&ixlib=rb-4.0.3&ixid=" +
        "M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"),
)


i2 = Image(
    property_id=2,
    aws_key="456",
    url= ("https://images.unsplash.com/photo-1560749003-f4b1e17e2dff" +
          "?q=80&w=1674&auto=format&fit=crop&ixlib=rb-4.0.3" +
          "&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"),
)

i3 = Image(
    property_id=3,
    aws_key="789",
    url= ("https://st.hzcdn.com/simgs/pictures/pools/" +
          "natural-private-residence-pool-environments-inc-img" +
          "~66e1401200abf6be_14-3383-1-325dc2d.jpg"),
)

db.session.add_all([i1, i2, i3])
db.session.commit()