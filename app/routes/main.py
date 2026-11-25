from flask import Blueprint, render_template, redirect, url_for, request
from datetime import datetime
from extension import db
from app.models.event import Event, Zone, Book
from sqlalchemy import or_
from flask_login import login_required, current_user

import cloudinary
import cloudinary.uploader

main = Blueprint("main", __name__)


@main.route('/')
def index():
    return redirect(url_for('main.get_events'))


@main.route("/events", methods=["GET"])
@login_required
def get_events():
    search_query = request.args.get("q", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 3
    
    query = Event.query.order_by(Event.start_date.desc())
    
    if search_query:
        query = query.filter(
            or_(
                Event.title.ilike(f"%{search_query}%"),
                Event.location.ilike(f"%{search_query}%"),
                Event.description.ilike(f"%{search_query}%")
            )
        )

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return render_template(
        "./page/events.html",
        events=pagination.items,
        pagination=pagination,
        search_query=search_query
    )



@main.route("/event/create", methods=["POST"])
@login_required
def create_event():
    
    if request.method == "POST":
        title = request.form.get("title")
        location = request.form.get("location")
        location_link = request.form.get("location_link")
        description = request.form.get("description")
            
        image = request.files.get("image")

        start_date_str = request.form.get("start_date") # Expected: YYYY-MM-DD
        end_date_str = request.form.get("end_date")     # Expected: YYYY-MM-DD
        time_str = request.form.get("time")             # Expected: HH:MM

        start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        event_time = datetime.strptime(time_str, "%H:%M").time()

        upload_result = None
        
        try:
            upload_result = cloudinary.uploader.upload(
                image,
                resource_type="auto"
            )
            
            image_url = upload_result["secure_url"]
            public_url = upload_result["public_id"]
            
            # Create Event
            event = Event(
                title=title,
                location=location,
                location_link=location_link,
                start_date=start_date,
                end_date=end_date,
                time=event_time,
                image_url=image_url,
                public_id=public_url,
                description=description
            )
            db.session.add(event)
            db.session.commit()
            print("Successfully added event")
        except Exception as e:
            db.session.rollback()
             
            print("Error Uploading", e)

    return redirect(url_for('main.get_events'))


# update , delete
@main.route("/event/<event_id>/delete", methods=["POST"])
@login_required
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    
    if not event:
        print("Event does not exist")
        return redirect(url_for('main.get_events'))
        
        
    try:
        cloudinary.uploader.destroy(
            event.public_id
        )
        
        db.session.delete(event)
        db.session.commit()
        print("successfull deleted event")
            
    except:
        print("Error deleting event")
    return redirect(url_for('main.get_events'))


# View detail event

@main.route("/event/<event_id>", methods=['GET'])
@login_required
def event(event_id):
    event = Event.query.get_or_404(event_id)
    
    zones = event.zones
    print(event_id)
    return render_template('page/event_detail.html', event=event, zones=zones)


#create zone for event

@main.route("/zone/<event_id>", methods=['POST'])
@login_required
def create_zone(event_id):
    
    
    if request.method == "POST":
        title = request.form.get("title")
        vehicle = request.form.get("vehicle")
        location = request.form.get("location")
        location_link = request.form.get("location_link")
        
        try:
            zone = Zone(
                title=title,
                vehicle=vehicle,
                location=location,
                location_link=location_link,
                event_id=event_id
            )
            
            db.session.add(zone)
            db.session.commit()
            print("Successfull Added")
        except:
            db.session.rollback()
            print("Errorr creating zone")
    return redirect(url_for("main.event", event_id=event_id))




@main.route("/zone/<zone_id>", methods=["POST"])
@login_required
def delete_zone(zone_id):
    
    zone = Zone.query.get_or_404(zone_id)
    
    if not zone:
        print("zone does not exist")
        return redirect(url_for(request.referrer or "/"))
    try:
        db.session.delete(zone)
        db.session.commit()
        print("Successfully delete zone")
    except Exception as e:
        print("Error could not delete zone")

    
    return redirect(request.referrer)


@main.route("/click-caputure", methods=["GET"])
@login_required
def click_capture():
    
    book = Book.query.get_or_404("5cff327a-7736-4871-adc1-05c53e692ec9")
    
    book.number_of_clicked += 1
    db.session.commit()
    
    return redirect(request.referrer or "/")



@main.route("/ai-chat", methods=["GET"])
@login_required
def ai_chat():
    return render_template("tools/ai_chat.html")