# Skillora — Tutorial 2: Services, Contracts & Schema

## Team details
Team ID: 24

| Roll No.    | Name | Responsibility |

| 20251651069 | Pranav Bhawsa | Identity  |
| 20251651049 | Jayesh Badole | Catalogue |
| 20251651082 | Shivam Kumar  | Orders    |
| 20251651067 | Pankaj Singh  | Payments  |
| 20251651068 | Paras Pandey  | Notifications |

## 1. Capabilities
- Register and authenticate users
- Publish and browse services
- Search/filter services
- Place orders
- Process payments
- Update order status
- Cancel eligible orders
- Issue refunds
- Send notifications

## 2. Service design

```text
+-------------------+       +-------------------+
| Identity          |       | Catalogue         |
| Owns: users,      |       | Owns: categories, |
| roles, addresses  |       | services          |
+---------+---------+       +---------+---------+
          |                           |
          | validateUser()            | checkService()
          v                           v
                 +-------------------+
                 | Orders            |
                 | Owns: orders,     |
                 | order_items      |
                 +----+---------+----+
                      |         |
              createPayment()   | notify()
                      v         v
             +-------------+  +----------------+
             | Payments    |  | Notifications  |
             | Owns: txns, |  | Owns: messages |
             | refunds     |  +----------------+
             |             |
             +-------------+
```

No service shares ownership of another service's tables.

## 3. Contracts

### Identity
| Operation | Input | Output | Errors |
|---|---|---|---|
| authenticate | email, password | user identity/token | invalid credentials |
| getUser | userId | public user profile | user not found |
| validateUser | userId | active/inactive result | user not found |

### Catalogue
| Operation | Input | Output | Errors |
|---|---|---|---|
| getService | serviceId | service representation | service not found |
| searchServices | query, category, page | service list | invalid query |
| checkService | serviceId | availability/price | service not found |

### Orders
| Operation | Input | Output | Errors |
|---|---|---|---|
| placeOrder | customerId, items, address | order | invalid items, unavailable service |
| getOrder | orderId | order | order not found |
| listOrders | customerId, status | order list | invalid filter |
| cancelOrder | orderId | updated order | illegal transition |

### Payments
| Operation | Input | Output | Errors |
|---|---|---|---|
| authorize | orderId, amount | transaction result | declined, unavailable |
| refund | transactionId, amount | refund result | invalid transaction |

### Notifications
| Operation | Input | Output | Errors |
|---|---|---|---|
| sendNotification | userId, message | notification id | unavailable |
| getNotifications | userId | notification list | user not found |

## 4. Central operation — placeOrder

### Input
- customerId
- items: serviceId + quantity
- addressId
- optional idempotency key

### Output
- orderId
- status
- total
- createdAt

### Errors
- customer not found
- service not found
- service unavailable
- invalid quantity
- payment declined
- dependency unavailable

### Hidden implementation details
Callers do not see SQL tables, database IDs internal to other services, database credentials, provider credentials, payment gateway credentials or internal stack traces.

## 5. Service validation

| Property | Result | Explanation |
|---|---|---|
| Reachable | Yes | HTTP API endpoint |
| Self-contained | Yes | Owns its data |
| Contract | Yes | REST/OpenAPI contracts |
| Independent | Yes | Separate service boundary |
| Loosely coupled | Mostly | Calls other services only through contracts |

## 6. Files
See `schema.sql`, `services.mmd` and the contract tables above.
