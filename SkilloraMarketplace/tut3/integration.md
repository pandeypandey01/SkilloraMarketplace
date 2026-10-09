# Skillora — Tutorial 3: Integrate an External SOAP Partner

## Context

Skillora uses REST for most internal web services because resource-oriented JSON APIs are simple for browser and service-to-service integration. For the external payment partner, SOAP is useful when a strong XML contract, explicit message structure and message-level security are required by the partner. The partner operation used here is `charge`, which authorizes a payment for an order. Skillora maps the partner's vocabulary into its own public error vocabulary so partner-specific terms do not leak to customers.

## Partner
Securepay SOAP Gateway

Operation:
`charge(orderId, amount, currency, cardToken)`

## HTTP binding

```http
POST /soap/payment HTTP/1.1
Host: api.securepay.com
Content-Type: text/xml; charset=utf-8
SOAPAction: "http://securepay.com/payment/processPayment"
Content-Length: <computed-length>

<SOAP envelope from soap-request.xml>
```

Endpoint:
`https://api.securepay.com/soap/payment`

## Discovery

Skillora can obtain the WSDL from a direct HTTPS URL or from an internal service catalogue.

### Registry entry
```yaml
business: SecurePay
service: PaymentGateway
endpoint: https://api.securepay.com/soap/payment
wsdl: https://api.securepay.com/wsdl/payment.wsdl
tModel:
  name: SecurePayPaymentContract
  reference: https://api.securepay.com/wsdl/payment.wsdl
```

No live UDDI server is required.

## Fault mapping

Partner fault:
`card_declined`

Skillora public error:
```json
{
  "type": "payment-declined",
  "title": "Payment declined",
  "status": 422,
  "detail": "The payment could not be authorised."
}
```

The partner's `card_declined` vocabulary is deliberately not exposed to Skillora customers.
