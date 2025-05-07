from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime, timedelta
import apprise
import os
from sqlalchemy.orm import Session
from models import Task, SessionLocal

# Initialize Apprise
apobj = apprise.Apprise()

# Add notification services from environment variables
apprise_urls = os.getenv("APPRISE_URLS", "").split(",")
for url in apprise_urls:
    if url.strip():
        apobj.add(url.strip())

def send_notification(task_id, task_content, time_remaining):
    """Send notification for a task"""
    # Create mark-as-done link
    mark_done_url = f"{os.getenv('BASE_URL', 'http://localhost:8000')}/tasks/{task_id}/complete"
    
    # Prepare notification message
    message = f"Task Reminder: {task_content}\n"
    message += f"Due in {time_remaining}\n"
    message += f"Mark as done: {mark_done_url}"
    
    # Send notification
    apobj.notify(
        title=f"Task Reminder: Due in {time_remaining}",
        body=message
    )

def check_upcoming_tasks():
    """Check for upcoming tasks and send notifications"""
    db = SessionLocal()
    try:
        # Get all incomplete tasks
        tasks = db.query(Task).filter(Task.completed == False).all()
        
        now = datetime.utcnow()
        
        for task in tasks:
            time_diff = task.due_time - now
            
            # Check if task is due in 3 days, 1 day, 1 hour, 30 minutes, or 15 minutes
            notification_times = [
                (timedelta(days=3), "3 days"),
                (timedelta(days=1), "1 day"),
                (timedelta(hours=1), "1 hour"),
                (timedelta(minutes=30), "30 minutes"),
                (timedelta(minutes=15), "15 minutes")
            ]
            
            for time_delta, time_text in notification_times:
                # Calculate the time window for notification
                # We check if the task is due within 1 minute of the notification time
                lower_bound = time_delta - timedelta(minutes=1)
                upper_bound = time_delta + timedelta(minutes=1)
                
                if lower_bound <= time_diff <= upper_bound:
                    send_notification(task.id, task.content, time_text)
                    break
    finally:
        db.close()

def start_scheduler():
    """Start the background scheduler"""
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        check_upcoming_tasks,
        IntervalTrigger(minutes=1),
        id='check_tasks_job',
        replace_existing=True
    )
    scheduler.start()
    return scheduler