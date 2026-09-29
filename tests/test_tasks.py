def login(client):
    client.post('/api/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    client.post('/api/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })

def test_create_task(client):
    login(client)
    response = client.post('/api/tasks', json={
        'title': 'Test Task',
        'priority': 'High'
    })
    assert response.status_code == 201
    assert b'Test Task' in response.data

def test_get_tasks(client):
    login(client)
    client.post('/api/tasks', json={'title': 'Test Task 1'})
    client.post('/api/tasks', json={'title': 'Test Task 2'})
    
    response = client.get('/api/tasks')
    assert response.status_code == 200
    assert b'Test Task 1' in response.data
    assert b'Test Task 2' in response.data

def test_update_task(client):
    login(client)
    res = client.post('/api/tasks', json={'title': 'Test Task 1'})
    task_id = res.get_json()['task']['id']
    
    response = client.put(f'/api/tasks/{task_id}', json={
        'title': 'Updated Task'
    })
    assert response.status_code == 200
    assert b'Updated Task' in response.data

def test_delete_task(client):
    login(client)
    res = client.post('/api/tasks', json={'title': 'Test Task 1'})
    task_id = res.get_json()['task']['id']
    
    response = client.delete(f'/api/tasks/{task_id}')
    assert response.status_code == 200
    
    res = client.get(f'/api/tasks/{task_id}')
    assert res.status_code == 404
