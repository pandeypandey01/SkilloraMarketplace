# Skillora — Tutorial 5: HTTP Methods & Headers

## Method map

| Action | Method | URL |
|---|---|---|
| List orders | GET | /orders |
| Create order | POST | /orders |
| Read order | GET | /orders/{id} |
| Modify order | PATCH | /orders/{id} |
| Cancel order | POST | /orders/{id}/cancellation |

GET is safe because it does not change server state. POST /orders is not naturally idempotent, so Assignment 4 uses Idempotency-Key. PATCH is protected by If-Match when overwriting state. Cancellation is an action sub-resource.

## OPTIONS

`OPTIONS /orders` returns:

```http
HTTP/1.1 204 No Content
Allow: GET, POST, OPTIONS
```

## Full exchange

```http
POST /orders HTTP/1.1
Host: localhost:5000
Authorization: Bearer demo
Content-Type: application/json
Accept: application/json
Idempotency-Key: demo-200

{"customerId":"C1","address":"Ahmedabad","items":[{"serviceId":"S1","qty":1}]}
```

Response:

```http
HTTP/1.1 201 Created
Location: /orders/ORD-1234
Content-Type: application/json; charset=utf-8

{"id":"ORD-1234","customerId":"C1","address":"Ahmedabad","items":[{"serviceId":"S1","qty":1}],"status":"pending","total":100.0,"version":1}
```

## Header table
| Endpoint             | Request headers                          | Response headers                          |
|----------------------|------------------------------------------|-------------------------------------------|
| POST /orders         | Authorization, Content-Type, Accept, Idempotency-Key | Location, Content-Type |
| GET /orders          | Authorization, Accept                    | Content-Type, X-RateLimit-Limit, X-RateLimit-Remaining, Retry-After |
| GET /orders/{id}     | Authorization, If-None-Match             | ETag, Cache-Control, Content-Type |
| PATCH /orders/{id}   | Authorization, Content-Type, If-Match    | Content-Type, updated OrderResponse |
| POST /orders/{id}/cancellation | Authorization, Accept          | Content-Type |


## Safe vs idempotent

- GET endpoints are safe and idempotent.
- POST /orders is neither naturally safe nor naturally idempotent; Idempotency-Key makes repeated requests return the original result.
- PATCH is not safe; If-Match prevents overwriting a changed version.
- Cancellation changes state and therefore is not safe.

## ETag

Example:
`ETag: "order-ORD-1234-v1"`

A matching `If-None-Match` can return `304 Not Modified`, saving the response body transfer. A stale `If-Match` on a write returns `412 Precondition Failed`, preventing lost updates.

## 422 vs 400

400 is appropriate when the HTTP request is malformed or cannot be parsed. 422 is used when the JSON can be read but the values violate the service's validation/domain rules.

## CORS

A browser may block a cross-origin response even if the server produced 200. The browser enforces the same-origin policy. `Access-Control-Allow-Origin` tells the browser which origins may access the response.

## Cache-Control

A single order GET can use private caching because it is a read. Payment secrets, credentials and sensitive transient data should use `Cache-Control: no-store`.

## GET vs POST search

GET is appropriate for ordinary query-string filtering. POST may be justified for very complex searches whose criteria are too large or structured for a practical URL. Switching to POST loses some normal GET cacheability/bookmarkability semantics.

## Location

On a 201 response, Location identifies the newly created resource. On a redirect, Location identifies the next target URI.
