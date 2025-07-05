from flask import Blueprint, request, jsonify
from flask_login import login_required
from members import roles_required
import models

api = Blueprint("api", __name__, url_prefix="/api")

def make_endpoint(name, get_all, create_fn, fields, required):
    @api.route(f"/{name}", methods=["GET","POST"])
    @login_required
    @roles_required("admin","manager")
    def generic():
        if request.method == "GET":
            return jsonify(get_all())

        data = request.get_json() or {}
        # 1) Validate required fields
        for f in required:
            if not data.get(f):
                return jsonify({"error": f"{f} is required"}), 400

        # 2) Build argument list in the correct order,
        #    missing values default to None → SQL NULL
        args = [data.get(f) for f in fields]
        create_fn(*args)
        return jsonify({"message": f"{name[:-1].capitalize()} created"}), 201

    # Give each route a unique function name
    generic.__name__ = f"{name}_endpoint"
    return generic

# MEMBERS
make_endpoint(
    name="members",
    get_all=models.get_all_members,
    create_fn=models.create_member,
    fields=[
      "firstName","lastName","email",
      "dateOfBirth","phoneNumber",
      "currentPlanID","membershipStatus","membershipStartDate"
    ],
    required=["firstName","lastName","email"]
)

# PLANS
make_endpoint(
    name="plans",
    get_all=models.get_all_plans,
    create_fn=models.create_plan,
    fields=["planName","monthlyFee","accessLevel"],
    required=["planName","monthlyFee"]
)

# TRAINERS
make_endpoint(
    name="trainers",
    get_all=models.get_all_trainers,
    create_fn=models.create_trainer,
    fields=["firstName","lastName","email","specialty"],
    required=["firstName","lastName","email"]
)

# ROOMS
make_endpoint(
    name="rooms",
    get_all=models.get_all_rooms,
    create_fn=models.create_room,
    fields=["roomName","capacity"],
    required=["roomName","capacity"]
)

# EQUIPMENT
make_endpoint(
    name="equipment",
    get_all=models.get_all_equipment,
    create_fn=models.create_equipment,
    fields=["equipmentName","purchaseDate","condition","roomID"],
    required=["equipmentName","roomID"]
)

# STAFF
make_endpoint(
    name="staff",
    get_all=models.get_all_staff,
    create_fn=models.create_staff,
    fields=["firstName","lastName","email","role"],
    required=["firstName","lastName","email","role"]
)