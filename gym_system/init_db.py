from app import db, MembershipPlan

db.create_all()

# Add sample membership plans
if not MembershipPlan.query.first():
    plans = [
        MembershipPlan(name="Basic Plan", duration_months=1, price=30.0),
        MembershipPlan(name="Standard Plan", duration_months=3, price=80.0),
        MembershipPlan(name="Premium Plan", duration_months=6, price=150.0),
    ]
    db.session.add_all(plans)
    db.session.commit()
    print("Database initialized and membership plans added.")
else:
    print("Database already initialized.")