from datetime import datetime, date, timedelta
from flask import (Blueprint, render_template, redirect, url_for, session, flash, jsonify, request)
from models.sleep_entry import SleepEntry, SleepGoal
from models.user import User
from database import db
from forms import SleepEntryForm, SleepGoalForm
from routes.auth import login_required, sanitise

sleep_bp = Blueprint('sleep', __name__)

def current_user():
    return User.query.get(session['user_id'])

@sleep_bp.route('/dashboard')
@login_required
def dashboard():
    user = current_user()
    entries = SleepEntry.query.filter_by(
        user_id=user.id).order_by(
            SleepEntry.bedtime.desc()).limit(7).all()
    avg = round(sum(e.duration_hrs for e in entries)
        / len(entries), 1) if entries else 0 
    goal = SleepGoal.query.filter_by(
        user_id=user.id).first()
    return render_template('dashboard.html', 
        user=user, entries=entries, avg=avg, goal=goal)


@sleep_bp.route('/log', methods=['GET', 'POST'])
@login_required
def log_sleep():
    form = SleepEntryForm()
    if form.validate_on_submit():
        duration = SleepEntry.calculate_duration(
            form.bedtime.data, form.wake_time.data)
        entry = SleepEntry(
            user_id=session['user_id'],
            bedtime=form.bedtime.data,
            wake_time=form.wake_time.data,
            duration_hrs=duration,
            quality=int(form.quality.data),
            notes=sanitise(form.notes.data)
                if form.notes.data else None)
        db.session.add(entry)
        db.session.commit()
        flash(f'Logged! {duration} hours sleep.', 'success')
        return redirect(url_for('sleep.dashboard'))
    return render_template('log_sleep.html', form=form)

@sleep_bp.route('/edit/<int:entry_id>', methods=['GET', 'POST'])
@login_required
def edit_sleep(entry_id):
    entry = SleepEntry.query.filter_by(
        id=entry_id,
        user_id=session['user_id']).first_or_404()
    form = SleepEntryForm(obj=entry)
    if form.validate_on_submit():
        entry.bedtime = form.bedtime.data
        entry.wake_time = form.wake_time.data
        entry.duration_hrs = SleepEntry.calculate_duration(form.bedtime.data, form.wake_time.data)
        entry.quality = int(form.quality.data)
        entry.notes = sanitise(form.notes.data) \
            if form.notes.data else None
        db.session.commit()
        flash('Entry updated.', 'success')
        return redirect(url_for('sleep.history'))
    return render_template('edit_sleep.html', form=form, entry=entry)

@sleep_bp.route('/delete/<int:entry_id>', methods=['POST'])
@login_required 
def delete_sleep(entry_id):
    entry = SleepEntry.query.filter_by(
        id=entry_id,
        user_id=session['user_id']).first_or_404()
    db.session.delete(entry)
    db.session.commit()
    flash('Deleted.', 'info')
    return redirect(url_for('sleep.history'))

@sleep_bp.route('/history')
@login_required
def history():
    page = request.args.get('page', 1, type=int)
    entries = SleepEntry.query.filter_by(
        user_id=session['user_id'])\
        .order_by(SleepEntry.bedtime.desc())\
        .paginate(page=page, per_page=10, error_out=False)
    return render_template('history.html',
         entries=entries)

@sleep_bp.route('/goal', methods=['GET','POST'])
@login_required
def goal():
    user = current_user()
    existing = SleepGoal.query.filter_by(
        user_id=user.id).first()
    form = SleepGoalForm(obj=existing)
    if form.validate_on_submit():
        if existing:
            existing.target_hours = form.target_hours.data
        else:
            db.session.add(SleepGoal(
                user_id=user.id,
                target_hours=form.target_hours.data))
        db.session.commit()
        flash('Goal saved!', 'success')
        return redirect(url_for('sleep.dashboard'))
    return render_template('goal.html',
        form=form, goal=existing)

@sleep_bp.route('/privacy')
def privacy():
    return render_template('privacy.html')

@sleep_bp.route('/api/weekly-data')
@login_required
def api_weekly_data():
    entries = SleepEntry.query.filter_by(
        user_id=session['user_id'])\
        .order_by(SleepEntry.bedtime.asc())\
        .limit(7).all()
    return jsonify([e.to_dict() for e in entries])

...
            
        