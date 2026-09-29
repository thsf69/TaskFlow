def test_register(client):
    response = client.post('/api/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 201
    assert b'Registration successful' in response.data

def test_login(client):
    client.post('/api/register', json={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    
    response = client.post('/api/login', json={
        'email': 'test@example.com',
        'password': 'password123'
    })
    assert response.status_code == 200
    assert b'Login successful' in response.data
