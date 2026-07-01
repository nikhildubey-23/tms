from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Trip

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def dashboard():
    trips = Trip.query.all()
    total_freight = sum(float(t.total_freight) for t in trips)
    total_paid = sum(float(t.total_paid) for t in trips)
    total_balance = sum(float(t.balance) for t in trips)
    pending_trips = Trip.query.filter(Trip.status == "Pending").count()
    completed_trips = Trip.query.filter(Trip.status == "Completed").count()
    total_trips = len(trips)
    return render_template(
        "dashboard.html",
        total_freight=total_freight,
        total_paid=total_paid,
        total_balance=total_balance,
        pending_trips=pending_trips,
        completed_trips=completed_trips,
        total_trips=total_trips,
        recent_trips=Trip.query.order_by(Trip.date.desc()).limit(5).all(),
    )
