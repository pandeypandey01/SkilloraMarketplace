# HTTP Log — Skillora Tutorial 1

Public read-only JSON API used for practice: JSONPlaceholder.

## Request 1 — List users

```http
GET https://jsonplaceholder.typicode.com/users HTTP/1.1
Host: jsonplaceholder.typicode.com
Accept: application/json
```

Equivalent curl:
```bash
curl -i https://jsonplaceholder.typicode.com/users
```

Expected response begins with:
```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
```

**200 OK:** request was successfully processed.
**application/json:** response body is JSON.

## Request 2 — Read one user

```bash
curl -i https://jsonplaceholder.typicode.com/users/1
```

Expected:
```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
```

**Meaning:** one JSON resource was returned.

## Request 3 — Read another resource

```bash
curl -i https://jsonplaceholder.typicode.com/posts/1
```

Expected:
```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
```

## Request 4 — List posts

```bash
curl -i https://jsonplaceholder.typicode.com/posts
```

Expected:
```http
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8
```

## Request 5 — Deliberate failure

```bash
curl -i https://jsonplaceholder.typicode.com/users/999999
```

Expected:
```http
HTTP/1.1 404 Not Found
```

**404 Not Found:** the requested resource does not exist.
