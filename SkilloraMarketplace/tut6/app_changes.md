# Tutorial 6 implementation notes

The Tutorial 4 `app.py` already contains:
- request validation before business processing
- one Problem Details helper
- 201 + Location for create
- 401, 404, 409, 412 and 422 failure paths
- Idempotency-Key handling
- ETag / If-None-Match
- If-Match precondition
- CORS and security headers

For a complete production implementation, add:
- strict Accept negotiation with 406
- explicit 429 rate-limit accounting per client
- 503 mapping around outbound payment calls
- Retry-After on 429/503
- XML serialization if application/xml is to be supported
- HTTPS in production
