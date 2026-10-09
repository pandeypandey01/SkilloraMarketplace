# Skillora Tutorial 4 Notes

## Resource table

| Method | URL | Purpose | Success | Failures |
|---|---|---|---|---|
| POST | /orders | Create order | 201 | 400, 401, 409, 422, 429, 503 |
| GET | /orders/{id} | Read order | 200 | 401, 404, 304 |
| GET | /orders | Filter orders | 200 | 401 |
| PATCH | /orders/{id} | Change state | 200 | 400, 401, 404, 409, 412, 422 |
| POST | /orders/{id}/cancellation | Cancel | 200 | 401, 404, 409, 422 |

## A5 hard choice

Cancellation is an action rather than a normal CRUD noun. The resource model therefore uses `POST /orders/{id}/cancellation`, which represents creation of a cancellation action/sub-resource. A verb URL such as `/cancelOrder` was rejected because it hides the resource boundary and does not follow the resource-oriented style.

## D3 fallback

If the payment dependency is unreachable, the order should not be reported as successfully paid. The service can keep the order in a pending state and return a transient 503 response so the client can retry safely. A degraded success would be incorrect because it could make the platform claim an order is paid when the payment has not been confirmed.

## Assignment 3 vs OpenAPI

The WSDL explicitly describes XML Schema types, messages, port types, SOAP bindings and service/port structures. OpenAPI focuses on HTTP paths, methods, parameters, request/response schemas and status codes, so it does not need the SOAP-specific message/binding structures.

## Fault mapping

SOAP fault:
`card_declined`

REST:
`422 application/problem+json` with type `payment-declined`.

Returning the fault as HTTP 200 would make intermediaries and generic HTTP clients treat the operation as successful even though the business operation failed. The HTTP status communicates failure at the transport/API boundary.

## UDDI moves

Publish, find and bind existed conceptually in classic service discovery. In this REST design, an API description/OpenAPI document and a service catalogue or configuration system take over discovery and binding. Dynamic UDDI is not required.

## XML Schema responsibility

`validate_create()` performs request validation before accessing request fields. Without it, missing `items`, invalid quantities or missing address data could reach business logic.

## SOAP use case retained

An external payment integration could still use SOAP where the partner contract requires a formal XML contract and message-level security. The guarantee being purchased is contractually structured SOAP messaging rather than a generic REST JSON interaction.

## Team details

Team ID: TEAM_ID_HERE
Members: ROLL_1 NAME_1; ROLL_2 NAME_2; ROLL_3 NAME_3; ROLL_4 NAME_4; ROLL_5 NAME_5
