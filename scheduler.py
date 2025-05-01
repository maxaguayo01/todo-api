from apscheduler.schedulers.background import BackgroundScheduler
from model import db, Task

def delete_completed_tasks():
    Task.query.filter_by(completed=True).delete()
    db.session.commit()

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=delete_completed_tasks, trigger="interval", minutes=10)
    scheduler.start()
