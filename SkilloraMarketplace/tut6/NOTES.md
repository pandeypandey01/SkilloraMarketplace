# Skillora — Tutorial 6: Honest Responses, Status Codes, Errors & Validation

## 1. Status map

| Endpoint | Success | Failures and reason |
|---|---|---|
| POST /orders | 201 | 400 malformed JSON; 401 missing auth; 422 invalid fields; 409 state conflict; 429 rate limit; 503 dependency unavailable |
| GET /orders | 200 | 401 missing auth |
| GET /orders/{id} | 200 | 401 missing auth; 404 unknown id; 304 unchanged representation |
| PATCH /orders/{id} | 200 | 400 malformed body; 401; 404; 409 illegal transition; 412 stale ETag; 422 invalid status |
| POST /orders/{id}/cancellation | 200 | 401; 404; 409 illegal transition |

A failure is represented by its HTTP status rather than a misleading 200 response with `ok:false`.

## 2. Type catalogue

| Type | Trigger |
|---|---|
| unauthorized | Missing/empty Authorization |
| validation-error | Invalid field values |
| order-not-found | Unknown order id |
| illegal-transition | Unsupported state change |
| precondition-failed | Stale If-Match |
| payment-declined | Payment partner declines |
| dependency-unavailable | Required service unavailable |

## 3. Problem Details

```http
HTTP/1.1 422 Unprocessable Entity
Content-Type: application/problem+json; charset=utf-8
```

```json
{
  "type": "validation-error",
  "title": "Validation failed",
  "status": 422,
  "detail": "Request contains invalid fields.",
  "errors": [
    {"field": "address", "message": "required"},
    {"field": "items[0].qty", "message": "integer >= 1 required"}
  ]
}
```

Fields:
- type: stable machine-readable category
- title: short human-readable summary
- status: HTTP status
- detail: general explanation
- errors: field-level validation details

## 4. Two bad fields at once

Request:
```json
{
  "customerId": "",
  "address": "",
  "items": [{"serviceId":"S1","qty":0}]
}
```

Response contains errors for customerId, address and items[0].qty in one 422 response.

## 5. Retry safety

GET is safe to retry. POST /orders is made retry-safe with Idempotency-Key. 429 and 503 indicate transient conditions where Retry-After can tell a client when to try again. A 4xx caused by invalid input should not be blindly retried unchanged.

## 6. Internal error mapping

Database exceptions, stack traces, credentials and internal connection details must remain server-side. The client receives a clean problem type and safe detail rather than an implementation-specific error.

## 7. JSON/XML negotiation

The service currently publishes JSON. A client may send:
`Accept: application/xml`

If XML is not implemented, the correct documented behavior is `406 Not Acceptable`. If XML support is later implemented, the same order representation can be serialized as XML.

## Team details

Team ID: 24
Name + Roll No: 
  Pranav Bhawsar  20251651069
	Jayesh Badole 	20251651049
	Shivam Kumar	  20251651082
	Pankaj Singh	  20251651067
	Paras Pandey	  20251651068