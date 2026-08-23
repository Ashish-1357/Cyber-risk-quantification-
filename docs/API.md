# API Documentation

## Authentication

Currently, the API is open (no authentication required for demo).
In production, add API key header:

```
X-API-Key: your-secret-key
```

## Rate Limiting

No rate limiting in demo mode. In production, configure via Nginx or FastAPI middleware.

## Error Handling

All errors return JSON with detail:

```json
{
  "detail": "Error description"
}
```

## Examples

### Get Risk Scenarios
```bash
curl http://localhost:8000/api/v1/risk/scenarios
```

### Run Optimization
```bash
curl -X POST http://localhost:8000/api/v1/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "budget": 5000000,
    "staff_capacity": 75,
    "risk_appetite": 3000000,
    "method": "budget_constrained"
  }'
```

### Custom Risk Calculation
```bash
curl -X POST "http://localhost:8000/api/v1/risk/calculate?name=Custom%20Scenario" \
  -H "Content-Type: application/json" \
  -d '{
    "threat_event_freq": [1, 3, 10],
    "threat_capability": [0.5, 0.7, 0.9],
    "control_strength": [0.3, 0.5, 0.7],
    "loss_magnitude": [100000, 500000, 5000000]
  }'
```
