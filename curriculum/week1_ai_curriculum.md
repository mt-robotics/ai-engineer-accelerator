# Week 1: Exception Handling for AI Systems
## Complete Learning Curriculum

---

## 🎯 **Week Overview**
**Goal**: Master bulletproof error handling for AI applications  
**Time**: 18 hours total (3 hours/day × 6 days)  
**Outcome**: Build a production-ready AI data processing system  
**Portfolio Piece**: Robust AI Pipeline with comprehensive error handling

---

## 📚 **Day 1: Foundation & AI Context (3 hours)**

### **Hour 1: Review Your Existing Knowledge**
**Action**: Read your `1-python-exception-handling.md` file completely
- Focus on sections 6 (Real-World Examples), 12 (Practical Patterns)
- Take notes on patterns you haven't used before
- Identify which examples feel most/least familiar

### **Hour 2: AI-Specific Error Patterns**
**New Concepts I'm Teaching You:**

#### **1. Model Loading Failures**
```python
# Common AI Error Pattern
import joblib
import tensorflow as tf

class ModelLoadError(Exception):
    """Custom exception for model loading failures"""
    pass

def load_ai_model(model_path, model_type="sklearn"):
    """Load ML model with proper error handling"""
    try:
        if model_type == "sklearn":
            model = joblib.load(model_path)
        elif model_type == "tensorflow":
            model = tf.keras.models.load_model(model_path)
        else:
            raise ValueError(f"Unsupported model type: {model_type}")
            
        # Validate model is actually loaded
        if model is None:
            raise ModelLoadError("Model loaded but is None")
            
        return model
        
    except FileNotFoundError:
        raise ModelLoadError(f"Model file not found: {model_path}")
    except Exception as e:
        raise ModelLoadError(f"Failed to load {model_type} model: {e}") from e
```

#### **2. API Rate Limiting & Retry Patterns**
```python
import time
import random
from functools import wraps

def ai_api_retry(max_retries=3, base_delay=1):
    """Decorator for retrying AI API calls with exponential backoff"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except (ConnectionError, TimeoutError) as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        # Exponential backoff with jitter
                        delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                        time.sleep(delay)
                    
            raise last_exception
        return wrapper
    return decorator

@ai_api_retry(max_retries=3)
def call_openai_api(prompt, model="gpt-3.5-turbo"):
    """Example AI API call with retry logic"""
    # Simulated API call that might fail
    if random.random() < 0.3:  # 30% failure rate
        raise ConnectionError("API temporarily unavailable")
    
    return f"AI response to: {prompt}"
```

### **Hour 3: Error Classification for AI Systems**
**Learn the 4 Types of AI Errors:**

1. **Input Validation Errors** (User's fault)
2. **System/Resource Errors** (Infrastructure issues)
3. **Model/Algorithm Errors** (AI-specific failures)
4. **External Service Errors** (Third-party API issues)

**Classification Exercise:**
```python
# EXERCISE: Classify these AI error scenarios
scenarios = [
    "User uploads corrupted image file",
    "GPU runs out of memory during training",
    "OpenAI API returns 429 rate limit error",
    "Model predicts invalid output format",
    "Database connection fails during data loading",
    "User inputs text in unsupported language"
]

# Your task: Write exception handling for each scenario type
```

---

## 🛠 **Day 2: Basic AI Error Handling (3 hours)**

### **Exercise 1: Fix the Broken AI Data Loader (1 hour)**

**Problem Context:**
You're working at an AI startup. The junior developer wrote this data loader for your ML pipeline, but it crashes constantly in production. Your job: make it bulletproof.

**Broken Code:**
```python
import json
import pandas as pd

def load_training_data(file_path):
    """Load training data - CURRENTLY BROKEN!"""
    file = open(file_path, 'r')
    data = json.load(file)
    
    features = data['X']
    labels = data['y']
    
    df = pd.DataFrame(features)
    return df, labels

# This code fails on:
# - Missing files
# - Corrupted JSON
# - Missing 'X' or 'y' keys
# - Invalid data types
# - Memory issues with large files
```

**Your Task:**
1. Identify all possible failure points
2. Add appropriate exception handling
3. Use custom exceptions where appropriate
4. Add logging for debugging
5. Make it fail gracefully (return None instead of crashing)

**Success Criteria:**
- ✅ Handles missing files gracefully
- ✅ Validates JSON structure before processing
- ✅ Provides helpful error messages
- ✅ Logs errors for debugging
- ✅ Never crashes the main program

**Time Limit: 1 hour**

---

### **Exercise 2: Build a Safe Model Prediction Endpoint (2 hours)**

**Scenario:**
You need to create a FastAPI endpoint that serves ML model predictions. It must handle all possible errors gracefully since this will face real users.

**Requirements (Blank Canvas - Build from Scratch):**
```python
# BUILD THIS: Complete FastAPI endpoint

"""
POST /predict
{
    "input_data": [1.2, 3.4, 5.6, 7.8],
    "model_version": "v1.0"
}

Response Success:
{
    "prediction": 0.85,
    "confidence": 0.92,
    "model_version": "v1.0",
    "status": "success"
}

Response Error:
{
    "error": "Invalid input format",
    "error_type": "validation_error",
    "details": "Input must be numeric array",
    "status": "error"
}
"""
```

**Must Handle:**
- Invalid input formats
- Model loading failures
- Prediction errors
- Memory overflow
- API timeout
- Invalid model versions

**Starter Template:**
```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np

app = FastAPI()

class PredictionRequest(BaseModel):
    input_data: list
    model_version: str = "v1.0"

class PredictionResponse(BaseModel):
    # Define your response model here
    pass

@app.post("/predict")
async def predict(request: PredictionRequest):
    """
    YOUR CODE HERE:
    1. Validate input
    2. Load appropriate model
    3. Make prediction
    4. Handle all possible errors
    5. Return structured response
    """
    pass
```

**Challenge Points:**
- 🎯 **Basic (50 XP)**: Handle basic input validation
- 🎯 **Intermediate (100 XP)**: Implement custom exceptions
- 🎯 **Advanced (200 XP)**: Add retry logic and circuit breaker pattern

---

## 🔧 **Day 3: Intermediate Error Recovery (3 hours)**

### **Exercise 3: AI Pipeline with Error Recovery (3 hours)**

**Real-World Scenario:**
You're building an AI content processing pipeline that:
1. Downloads content from URLs
2. Extracts text using AI
3. Analyzes sentiment
4. Stores results in database

**The Challenge:** Individual steps can fail, but the pipeline should:
- Continue processing other items
- Retry failed items with exponential backoff
- Maintain detailed error logs
- Provide status reporting

**Architecture Overview:**
```python
# PIPELINE STAGES:
# URL -> Download -> Extract -> Analyze -> Store
#  |        |          |         |        |
#  v        v          v         v        v
# Can    Network    AI API    Model    Database
# fail   timeout    error     error    error
```

**Your Mission:**
Build a `ProcessingPipeline` class that handles a batch of URLs and processes them robustly.

**Code Template:**
```python
import asyncio
import aiohttp
import logging
from dataclasses import dataclass
from typing import List, Optional, Dict
from enum import Enum

class ProcessingStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"
    RETRYING = "retrying"

@dataclass
class ProcessingItem:
    url: str
    status: ProcessingStatus = ProcessingStatus.PENDING
    result: Optional[Dict] = None
    error: Optional[str] = None
    retry_count: int = 0
    max_retries: int = 3

class AIProcessingPipeline:
    def __init__(self, max_concurrent=5):
        self.max_concurrent = max_concurrent
        self.items: List[ProcessingItem] = []
        self.logger = logging.getLogger(__name__)
    
    async def download_content(self, url: str) -> str:
        """Download content from URL - CAN FAIL"""
        # YOUR CODE: Implement with proper error handling
        pass
    
    async def extract_text(self, content: str) -> str:
        """Extract text using AI - CAN FAIL"""
        # YOUR CODE: Simulate AI text extraction
        pass
    
    async def analyze_sentiment(self, text: str) -> float:
        """Analyze sentiment - CAN FAIL"""
        # YOUR CODE: Simulate sentiment analysis
        pass
    
    async def store_result(self, item: ProcessingItem) -> bool:
        """Store in database - CAN FAIL"""
        # YOUR CODE: Simulate database storage
        pass
    
    async def process_single_item(self, item: ProcessingItem):
        """Process one item through the entire pipeline"""
        # YOUR CODE: Implement full pipeline with error handling
        pass
    
    async def process_batch(self, urls: List[str]) -> Dict:
        """Process multiple URLs concurrently"""
        # YOUR CODE: Implement batch processing
        pass
    
    def get_status_report(self) -> Dict:
        """Return processing status report"""
        # YOUR CODE: Generate status summary
        pass

# USAGE EXAMPLE:
async def main():
    pipeline = AIProcessingPipeline(max_concurrent=3)
    urls = [
        "https://example.com/article1",
        "https://invalid-url-that-will-fail.com",
        "https://example.com/article3",
        # ... more URLs
    ]
    
    results = await pipeline.process_batch(urls)
    print(pipeline.get_status_report())

if __name__ == "__main__":
    asyncio.run(main())
```

**Success Criteria:**
- ✅ Individual failures don't stop batch processing
- ✅ Failed items are retried with exponential backoff
- ✅ Detailed logging at each stage
- ✅ Comprehensive status reporting
- ✅ Proper resource cleanup (async context managers)
- ✅ Configurable retry policies

**Bonus Challenges:**
- 🚀 Add circuit breaker pattern for external services
- 🚀 Implement priority queuing for retries
- 🚀 Add metrics collection (processing times, error rates)

---

## 🎯 **Day 4: Production Error Patterns (3 hours)**

### **Exercise 4: Circuit Breaker for AI Services (2 hours)**

**Problem:** Your AI application calls multiple external services (OpenAI, image processing API, database). When one service fails, your entire app shouldn't crash.

**Your Task:** Implement a production-ready circuit breaker system.

**Template:**
```python
import time
import asyncio
from enum import Enum
from typing import Callable, Any, Optional
from dataclasses import dataclass

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, blocking requests
    HALF_OPEN = "half_open" # Testing if service recovered

@dataclass
class CircuitConfig:
    failure_threshold: int = 5
    success_threshold: int = 3
    timeout: int = 60
    monitor_window: int = 300

class AIServiceCircuitBreaker:
    """Circuit breaker specifically designed for AI services"""
    
    def __init__(self, service_name: str, config: CircuitConfig):
        # YOUR CODE: Initialize circuit breaker
        pass
    
    async def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function through circuit breaker"""
        # YOUR CODE: Implement circuit breaker logic
        pass
    
    def _should_attempt_call(self) -> bool:
        """Determine if call should be attempted"""
        # YOUR CODE: State-based decision logic
        pass
    
    def _record_success(self):
        """Record successful call"""
        # YOUR CODE: Update success metrics
        pass
    
    def _record_failure(self, exception: Exception):
        """Record failed call"""
        # YOUR CODE: Update failure metrics
        pass
    
    def get_metrics(self) -> dict:
        """Return circuit breaker metrics"""
        # YOUR CODE: Return current metrics
        pass

# USAGE EXAMPLE:
async def test_circuit_breaker():
    config = CircuitConfig(failure_threshold=3, timeout=30)
    breaker = AIServiceCircuitBreaker("openai_api", config)
    
    async def flaky_ai_service(prompt: str):
        """Simulates unreliable AI service"""
        if random.random() < 0.7:  # 70% failure rate
            raise ConnectionError("Service unavailable")
        return f"AI response to: {prompt}"
    
    # Test the circuit breaker
    for i in range(10):
        try:
            result = await breaker.call(flaky_ai_service, f"prompt_{i}")
            print(f"Success: {result}")
        except Exception as e:
            print(f"Failed: {e}")
        
        await asyncio.sleep(1)
        print(f"Metrics: {breaker.get_metrics()}")
```

### **Exercise 5: Error Monitoring Dashboard Data (1 hour)**

**Scenario:** You need to collect error data for monitoring dashboard.

**Build This:** Error collector that categorizes and aggregates AI system errors.

```python
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from typing import Dict, List, Optional
from dataclasses import dataclass, field

@dataclass
class ErrorEvent:
    timestamp: datetime
    error_type: str
    service: str
    severity: str  # "low", "medium", "high", "critical"
    message: str
    context: Dict = field(default_factory=dict)

class AIErrorMonitor:
    """Collect and analyze AI system errors for monitoring"""
    
    def __init__(self, retention_hours: int = 24):
        # YOUR CODE: Initialize error storage and metrics
        pass
    
    def record_error(self, error_type: str, service: str, 
                    severity: str, message: str, **context):
        """Record an error event"""
        # YOUR CODE: Store error with metadata
        pass
    
    def get_error_summary(self, hours: int = 1) -> Dict:
        """Get error summary for last N hours"""
        # YOUR CODE: Generate error analytics
        return {
            "total_errors": 0,
            "by_service": {},
            "by_severity": {},
            "by_type": {},
            "error_rate": 0.0,
            "trending_errors": []
        }
    
    def get_health_status(self) -> str:
        """Return system health based on error patterns"""
        # YOUR CODE: Analyze errors and return health status
        # Return: "healthy", "degraded", "critical"
        pass
    
    def cleanup_old_errors(self):
        """Remove errors outside retention window"""
        # YOUR CODE: Clean up old error data
        pass

# INTEGRATION EXAMPLE:
monitor = AIErrorMonitor(retention_hours=24)

# In your AI code:
try:
    result = await ai_model.predict(data)
except ModelLoadError as e:
    monitor.record_error("model_error", "ml_service", "high", 
                        str(e), model_path=model_path)
except ValidationError as e:
    monitor.record_error("validation_error", "api", "medium", 
                        str(e), input_data=data)
```

---

## 🏆 **Day 5: Mini-Project Integration (3 hours)**

### **Project: Bulletproof AI Data Processor**

**Business Context:**
You're building a production AI service that processes user-uploaded files, runs AI analysis, and returns results. This will handle thousands of requests daily and must never crash.

**System Requirements:**
```
Input: File upload (JSON, CSV, or text)
Processing: 
  1. Validate file format and content
  2. Extract/clean data
  3. Run AI analysis (sentiment, classification, etc.)
  4. Store results
  5. Return structured response

Must Handle:
- Invalid file formats
- Corrupted files
- Large files (memory limits)
- AI service failures
- Database errors
- Concurrent processing
```

**Architecture:**
```python
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import asyncio
import pandas as pd
import json
from typing import Optional, Dict, Any

app = FastAPI(title="Bulletproof AI Processor")

class AIDataProcessor:
    """Production-ready AI data processing system"""
    
    def __init__(self):
        # YOUR CODE: Initialize with all error handling components
        # - Circuit breakers for external services
        # - Error monitor
        # - Resource managers
        # - Retry handlers
        pass
    
    async def process_file(self, file: UploadFile) -> Dict[str, Any]:
        """Main processing pipeline with comprehensive error handling"""
        # YOUR CODE: Implement full pipeline
        processing_id = self._generate_processing_id()
        
        try:
            # Stage 1: File validation and parsing
            data = await self._validate_and_parse_file(file)
            
            # Stage 2: Data cleaning and preparation
            cleaned_data = await self._clean_data(data)
            
            # Stage 3: AI analysis
            analysis_results = await self._run_ai_analysis(cleaned_data)
            
            # Stage 4: Store results
            await self._store_results(processing_id, analysis_results)
            
            # Stage 5: Return success response
            return self._format_success_response(processing_id, analysis_results)
            
        except Exception as e:
            # YOUR CODE: Comprehensive error handling and recovery
            return self._format_error_response(processing_id, e)
    
    async def _validate_and_parse_file(self, file: UploadFile) -> Any:
        """Validate file and parse content safely"""
        # YOUR CODE: Implement with proper error handling
        pass
    
    async def _clean_data(self, data: Any) -> Any:
        """Clean and prepare data for AI analysis"""
        # YOUR CODE: Data validation and cleaning
        pass
    
    async def _run_ai_analysis(self, data: Any) -> Dict:
        """Run AI analysis with retry and fallback"""
        # YOUR CODE: AI processing with circuit breaker
        pass
    
    async def _store_results(self, processing_id: str, results: Dict):
        """Store results with error recovery"""
        # YOUR CODE: Database operations with retries
        pass
    
    def _format_success_response(self, processing_id: str, results: Dict) -> Dict:
        """Format successful response"""
        # YOUR CODE: Structure success response
        pass
    
    def _format_error_response(self, processing_id: str, error: Exception) -> Dict:
        """Format error response with proper classification"""
        # YOUR CODE: Classify error and format response
        pass

# FastAPI endpoints
processor = AIDataProcessor()

@app.post("/process")
async def process_data(file: UploadFile):
    """Process uploaded file with AI analysis"""
    # YOUR CODE: Implement endpoint with validation
    pass

@app.get("/health")
async def health_check():
    """System health endpoint"""
    # YOUR CODE: Return system health status
    pass

@app.get("/metrics")
async def get_metrics():
    """Error and performance metrics"""
    # YOUR CODE: Return error monitoring data
    pass
```

**Success Criteria:**
- ✅ Handles all file format errors gracefully
- ✅ Processes files within memory limits
- ✅ AI failures don't crash the system
- ✅ Provides detailed error reporting
- ✅ Maintains performance under load
- ✅ Comprehensive logging and monitoring
- ✅ Clean, production-ready code

**Deliverable:** Complete FastAPI application that you can deploy to Railway.app

---

## 📊 **Day 6: Assessment & Reflection (3 hours)**

### **Hour 1: Code Review Session**
**Self-Assessment Questions:**
1. Can your code handle any file input without crashing?
2. Are your error messages helpful for debugging?
3. Would this code work in production with real users?
4. What happens under high load or memory pressure?
5. How would you monitor this system in production?

### **Hour 2: Performance Challenge**
**Stress Test Your Code:**
```python
# CHALLENGE: Run your processor against these edge cases
test_cases = [
    "empty_file.json",
    "huge_file_10mb.csv", 
    "corrupted_data.json",
    "unsupported_format.xyz",
    "malicious_input.txt",
    "unicode_nightmare.csv"
]

# Can your code handle all of these gracefully?
```

### **Hour 3: Portfolio Preparation**
**GitHub Repository Setup:**
1. Clean up your code with proper documentation
2. Add comprehensive README with usage examples
3. Include error handling patterns as learning examples
4. Deploy to Railway.app and test live
5. Write a blog post about production error handling

---

## 🎯 **Week 1 Success Metrics**

**Technical Skills Gained:**
- ✅ Can write bulletproof error handling for any Python application
- ✅ Understands AI-specific error patterns and recovery strategies
- ✅ Can design production-ready error monitoring systems
- ✅ Implements circuit breakers and retry patterns correctly
- ✅ Writes clean, maintainable error handling code

**Portfolio Additions:**
- ✅ Production-ready AI processing system
- ✅ Comprehensive error handling examples
- ✅ Deployed application with monitoring
- ✅ Technical blog post demonstrating expertise

**Confidence Indicators:**
- ✅ Can debug any Python error systematically
- ✅ Confident in production deployment
- ✅ Can explain error handling patterns in interviews
- ✅ Ready for Week 2: JSON Operations & API Integration

---

## 🚀 **Week 2 Preview**
**Next Week:** "JSON Operations & AI API Integration"
- Master complex JSON data structures for AI
- Build robust API integrations with AI services
- Handle real-time data streaming
- Create intelligent data transformation pipelines

**Get Ready:** Review your `2-json-operations-python.md` file this weekend!

---

## 📈 **Progress Tracking**

**Daily XP Breakdown:**
- Day 1: 100 XP (Foundation)
- Day 2: 200 XP (Basic Exercises)
- Day 3: 300 XP (Intermediate Pipeline)
- Day 4: 400 XP (Production Patterns)
- Day 5: 500 XP (Complete Project)
- Day 6: 100 XP (Assessment)

**Total Week 1 XP: 1,600**

**Achievement Unlocks:**
- 🏆 **Error Handler** - Complete all basic exercises
- 🏆 **Pipeline Builder** - Build working AI pipeline
- 🏆 **Production Ready** - Deploy bulletproof system
- 🏆 **Week 1 Master** - Complete all challenges with excellence

**Your AI Engineer Level: Apprentice → Practitioner** 🎓