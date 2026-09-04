# Zalia Security - Testing Guide

Comprehensive testing guide for Zalia Security developers.

---

## Testing Framework Setup

### Install Testing Dependencies

```bash
pip install pytest pytest-flask pytest-cov black flake8
```

### Create tests directory

```bash
mkdir tests
touch tests/__init__.py
touch tests/test_api.py
touch tests/test_utils.py
```

---

## Unit Tests

### API Tests

**File: `tests/test_api.py`**

```python
import pytest
import json
from app import app, client
from config import TestingConfig

@pytest.fixture
def app_client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.app_context():
        yield app.test_client()

def test_health_check(app_client):
    """Test health check endpoint"""
    response = app_client.get('/api/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_chat_no_message(app_client):
    """Test chat endpoint with no message"""
    response = app_client.post('/api/chat', 
        json={'message': ''})
    assert response.status_code == 400

def test_chat_valid_message(app_client):
    """Test chat endpoint with valid message"""
    response = app_client.post('/api/chat',
        json={'message': 'Hello Zazi'})
    
    # Mock OpenAI response
    if response.status_code == 200:
        data = json.loads(response.data)
        assert 'reply' in data

def test_home_page(app_client):
    """Test home page loads"""
    response = app_client.get('/')
    assert response.status_code == 200

def test_zazi_page(app_client):
    """Test Zazi chat page loads"""
    response = app_client.get('/zazi')
    assert response.status_code == 200

def test_404_error(app_client):
    """Test 404 error handling"""
    response = app_client.get('/nonexistent')
    assert response.status_code == 404

def test_rate_limiting(app_client):
    """Test rate limiting"""
    # Make requests rapidly
    for i in range(25):  # Exceed limit of 20
        response = app_client.post('/api/chat',
            json={'message': f'Test {i}'})
    
    # Last request should be rate limited
    assert response.status_code == 429
```

### Utility Tests

**File: `tests/test_utils.py`**

```python
import pytest
from utils import (
    sanitize_input,
    validate_email,
    validate_phone,
    truncate_text,
    ResponseFormatter
)

def test_sanitize_input():
    """Test input sanitization"""
    assert sanitize_input("  hello  ") == "hello"
    assert sanitize_input("a" * 2500)[:2000]
    assert "<script>" not in sanitize_input("<script>alert('xss')</script>")

def test_sanitize_input_non_string():
    """Test sanitization with non-string input"""
    assert sanitize_input(None) == ""
    assert sanitize_input(123) == ""

def test_validate_email():
    """Test email validation"""
    assert validate_email("user@example.com") == True
    assert validate_email("invalid@") == False
    assert validate_email("notanemail") == False

def test_validate_phone():
    """Test phone validation"""
    assert validate_phone("08012345678") == True
    assert validate_phone("+2348012345678") == True
    assert validate_phone("123") == False

def test_truncate_text():
    """Test text truncation"""
    text = "a" * 150
    result = truncate_text(text, 100)
    assert len(result) <= 100
    assert result.endswith("...")

def test_response_formatter():
    """Test response formatting"""
    # Success response
    success = ResponseFormatter.success(data={"test": "data"})
    assert success['status'] == 'success'
    assert success['data']['test'] == 'data'
    
    # Error response
    error = ResponseFormatter.error("Test error")
    assert error['status'] == 'error'
    assert error['message'] == 'Test error'
```

---

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Specific Test File

```bash
pytest tests/test_api.py
```

### Run Specific Test

```bash
pytest tests/test_api.py::test_health_check
```

### Run with Coverage

```bash
pytest --cov=. --cov-report=html
# Opens coverage/index.html in browser
```

### Verbose Output

```bash
pytest -v
```

---

## Code Quality

### Format Code with Black

```bash
black app.py config.py utils.py tests/
```

### Check Code Style with Flake8

```bash
flake8 app.py config.py utils.py
```

### Check for Common Errors

```bash
pylint app.py
```

---

## Integration Tests

### Browser Automation (Selenium)

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

def test_chat_flow():
    """Test complete chat flow"""
    driver = webdriver.Chrome()
    
    try:
        driver.get("http://localhost:5000/zazi")
        
        # Find chat input
        chat_input = driver.find_element(By.ID, "userInput")
        
        # Type message
        chat_input.send_keys("Hello Zazi")
        
        # Find and click submit
        submit_btn = driver.find_element(By.ID, "zaziForm")
        submit_btn.submit()
        
        # Wait for response
        wait = WebDriverWait(driver, 10)
        response = wait.until(
            lambda d: d.find_element(By.CLASS_NAME, "message-zazi")
        )
        
        assert response is not None
    finally:
        driver.quit()
```

---

## Performance Tests

### Load Testing with Locust

**File: `locustfile.py`**

```python
from locust import HttpUser, task, between
import json

class ZaliaUser(HttpUser):
    wait_time = between(1, 3)
    
    @task(3)
    def chat(self):
        """Simulate chat requests"""
        self.client.post("/api/chat", 
            json={"message": "Hello Zazi"})
    
    @task(1)
    def health_check(self):
        """Simulate health checks"""
        self.client.get("/api/health")
```

Run tests:
```bash
locust -f locustfile.py --host=http://localhost:5000
# Then open http://localhost:8089
```

---

## Manual Testing Checklist

### Frontend Testing

- [ ] Home page loads correctly
- [ ] Dark/Light theme toggles
- [ ] Chat interface responsive on mobile
- [ ] Service Worker registers
- [ ] Offline mode works
- [ ] Images load properly
- [ ] Links work correctly
- [ ] Accessibility (keyboard navigation)

### Backend Testing

- [ ] API responds to requests
- [ ] Rate limiting works
- [ ] Error messages clear
- [ ] Logging captures events
- [ ] CORS headers present
- [ ] Security headers present
- [ ] Input validation works
- [ ] OpenAI integration works

### PWA Testing

- [ ] Can install as app
- [ ] Works offline
- [ ] Cache strategy working
- [ ] Manifests loads
- [ ] Icons display
- [ ] Theme persists

### Cross-Browser Testing

Test on:
- Chrome/Chromium
- Firefox
- Safari
- Edge

### Mobile Testing

Test on:
- iPhone/Safari
- Android/Chrome
- Tablets

---

## Debugging

### Flask Debugger

```python
# In development
app.run(debug=True)
```

### Print Statements

```python
print(f"Debug: {variable}")
```

### Logging

```python
import logging
logger = logging.getLogger(__name__)
logger.debug("Debug message")
logger.info("Info message")
logger.error("Error message")
```

### Browser DevTools

- F12 to open
- Console for JS errors
- Network tab for API calls
- Application tab for Storage

---

## Continuous Integration

### GitHub Actions (`.github/workflows/tests.yml`)

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: pytest --cov=.
    
    - name: Upload coverage
      uses: codecov/codecov-action@v2
```

---

## Test Data

### Sample Chat Messages

```python
TEST_MESSAGES = [
    "How are you?",
    "How do I stay safe in a taxi?",
    "What is phishing?",
    "Where's the nearest police station?",
    "Help! Someone is following me",
    "What do I do in a fire?",
    "Is the weather good today?",
]
```

---

## Common Issues

### Issue: Tests Fail Locally But Pass in CI
**Solution:** Ensure test environment matches CI environment

### Issue: Flaky Tests
**Solution:** Add proper waits/timeouts, mock external services

### Issue: Slow Tests
**Solution:** Use test database, mock API calls, parallel execution

---

## Best Practices

1. **Test Early & Often**
   - Write tests alongside code
   - Run tests before commits

2. **Keep Tests Simple**
   - One assertion per test (ideally)
   - Clear test names

3. **Use Fixtures**
   - Reuse test setup
   - Reduce code duplication

4. **Mock External Services**
   - Don't hit real APIs
   - Control test data

5. **Maintain Test Coverage**
   - Aim for >80% coverage
   - Document untestable code

---

## Resources

- [pytest Documentation](https://docs.pytest.org/)
- [Flask Testing](https://flask.palletsprojects.com/testing/)
- [Selenium Documentation](https://www.selenium.dev/documentation/)
- [Locust Documentation](https://locust.io/)

---

**Test early, test often. Keep Zalia safe. 🐾✨**
