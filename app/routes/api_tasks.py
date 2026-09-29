from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.models import Task
from app import db
from datetime import datetime, timezone

api_tasks_bp = Blueprint('api_tasks', __name__)

@api_tasks_bp.route('/tasks', methods=['GET'])
@login_required
def get_tasks():
    status = request.args.get('status')
    priority = request.args.get('priority')
    category = request.args.get('category')
    search = request.args.get('search')
    sort_by = request.args.get('sort_by', 'created_at')
    order = request.args.get('order', 'desc')
    
    query = Task.query.filter_by(user_id=current_user.id)
    
    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)
    if category:
        query = query.filter(Task.category.ilike(f'%{category}%'))
    if search:
        query = query.filter(Task.title.ilike(f'%{search}%'))
        
    if sort_by == 'due_date':
        if order == 'asc':
            query = query.order_by(Task.due_date.asc())
        else:
            query = query.order_by(Task.due_date.desc())
    else:
        if order == 'asc':
            query = query.order_by(Task.created_at.asc())
        else:
            query = query.order_by(Task.created_at.desc())
            
    tasks = query.all()
    
    if sort_by == 'priority':
        priority_map = {'High': 3, 'Medium': 2, 'Low': 1}
        tasks.sort(key=lambda x: priority_map.get(x.priority, 0), reverse=(order == 'desc'))

    return jsonify({'tasks': [t.to_dict() for t in tasks]}), 200

@api_tasks_bp.route('/tasks', methods=['POST'])
@login_required
def create_task():
    data = request.get_json()
    title = data.get('title', '').strip()
    
    if not title:
        return jsonify({'error': 'Title is required'}), 400
        
    due_date = None
    if data.get('due_date'):
        try:
            # Handle standard ISO formats, including frontend 'YYYY-MM-DD' which we parse directly
            due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Invalid date format.'}), 400

    task = Task(
        user_id=current_user.id,
        title=title,
        description=data.get('description', ''),
        category=data.get('category', ''),
        priority=data.get('priority', 'Medium'),
        status=data.get('status', 'Pending'),
        due_date=due_date
    )
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify({'message': 'Task created successfully', 'task': task.to_dict()}), 201

@api_tasks_bp.route('/tasks/<int:id>', methods=['GET'])
@login_required
def get_task(id):
    task = Task.query.filter_by(id=id, user_id=current_user.id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404
        
    return jsonify({'task': task.to_dict()}), 200

@api_tasks_bp.route('/tasks/<int:id>', methods=['PUT'])
@login_required
def update_task(id):
    task = Task.query.filter_by(id=id, user_id=current_user.id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404
        
    data = request.get_json()
    title = data.get('title', '').strip()
    
    if not title:
        return jsonify({'error': 'Title is required'}), 400
        
    task.title = title
    task.description = data.get('description', task.description)
    task.category = data.get('category', task.category)
    task.priority = data.get('priority', task.priority)
    task.status = data.get('status', task.status)
    
    if 'due_date' in data:
        if data['due_date']:
            try:
                task.due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
            except ValueError:
                return jsonify({'error': 'Invalid date format.'}), 400
        else:
            task.due_date = None
            
    db.session.commit()
    return jsonify({'message': 'Task updated successfully', 'task': task.to_dict()}), 200

@api_tasks_bp.route('/tasks/<int:id>', methods=['DELETE'])
@login_required
def delete_task(id):
    task = Task.query.filter_by(id=id, user_id=current_user.id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404
        
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'}), 200

@api_tasks_bp.route('/tasks/<int:id>/status', methods=['PATCH'])
@login_required
def update_task_status(id):
    task = Task.query.filter_by(id=id, user_id=current_user.id).first()
    if not task:
        return jsonify({'error': 'Task not found'}), 404
        
    data = request.get_json()
    status = data.get('status')
    if status not in ['Pending', 'In Progress', 'Completed']:
        return jsonify({'error': 'Invalid status'}), 400
        
    task.status = status
    db.session.commit()
    return jsonify({'message': 'Task status updated', 'task': task.to_dict()}), 200

@api_tasks_bp.route('/dashboard', methods=['GET'])
@login_required
def get_dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    now = datetime.now(timezone.utc)
    
    # Check for timezone-aware due_date since now is UTC aware
    def is_overdue(t):
        if not t.due_date or t.status == 'Completed':
            return False
        # If due_date is naive (sqlite datetime), make it UTC for comparison
        dt = t.due_date.replace(tzinfo=timezone.utc) if t.due_date.tzinfo is None else t.due_date
        return dt < now
    
    stats = {
        'total': len(tasks),
        'pending': sum(1 for t in tasks if t.status == 'Pending'),
        'in_progress': sum(1 for t in tasks if t.status == 'In Progress'),
        'completed': sum(1 for t in tasks if t.status == 'Completed'),
        'high_priority': sum(1 for t in tasks if t.priority == 'High'),
        'overdue': sum(1 for t in tasks if is_overdue(t))
    }
    
    return jsonify({'stats': stats}), 200
