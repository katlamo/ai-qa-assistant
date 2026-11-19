# Test Cases Report

## Summary

- Test cases: 11
  - High: 5
  - Medium: 5
  - Low: 1
- Need clarification: 4

## Test Cases

### Overview

| ID | Title | Type | Priority | Need clarification |
|---|---|---|---|---|
| TC-01 | Get all bookings returns HTTP 200 with list of booking IDs | Positive | High | No |
| TC-02 | Get bookings filtered by firstname returns matching booking IDs | Positive | High | No |
| TC-03 | Get bookings filtered by lastname returns matching booking IDs | Positive | High | No |
| TC-04 | Get booking by valid ID returns HTTP 200 with all required details | Positive | High | No |
| TC-05 | Get booking by non-existent ID returns HTTP 404 | Negative | High | No |
| TC-06 | Get bookings filtered by both firstname and lastname returns matching booking IDs | Positive | Medium | No |
| TC-07 | Get bookings filtered by non-existent name returns empty list | Negative | Medium | Yes |
| TC-08 | Get booking with non-numeric ID is handled with an appropriate error response | Negative | Medium | Yes |
| TC-09 | Response is returned in JSON format when JSON is requested | Positive | Medium | No |
| TC-10 | Response structure of booking details matches expected schema | Positive | Medium | Yes |
| TC-11 | Get booking with ID zero or negative value | Boundary | Low | Yes |

### Details

### TC-01: Get all bookings returns HTTP 200 with list of booking IDs

- Type: Positive
- Priority: High

**Steps**

1. Send GET request to https://restful-booker.herokuapp.com/booking without any query parameters
2. Inspect the HTTP status code of the response
3. Inspect the response body

**Expected result:** API returns HTTP 200 OK and the response body contains a list of booking IDs

### TC-02: Get bookings filtered by firstname returns matching booking IDs

- Type: Positive
- Priority: High

**Preconditions**

- At least one booking exists with a known firstname

**Steps**

1. Send GET request to /booking with query parameter firstname set to a known existing first name
2. Inspect the HTTP status code and response body

**Expected result:** API returns HTTP 200 OK and a list of booking IDs whose bookings have the specified firstname

### TC-03: Get bookings filtered by lastname returns matching booking IDs

- Type: Positive
- Priority: High

**Preconditions**

- At least one booking exists with a known lastname

**Steps**

1. Send GET request to /booking with query parameter lastname set to a known existing last name
2. Inspect the HTTP status code and response body

**Expected result:** API returns HTTP 200 OK and a list of booking IDs whose bookings have the specified lastname

### TC-04: Get booking by valid ID returns HTTP 200 with all required details

- Type: Positive
- Priority: High

**Preconditions**

- A booking with a known valid ID exists

**Steps**

1. Send GET request to /booking/{id} using a valid existing booking ID
2. Inspect the HTTP status code
3. Inspect the response body for firstname, lastname, totalprice, depositpaid, bookingdates, and additionalneeds

**Expected result:** API returns HTTP 200 OK and the response body contains firstname, lastname, totalprice, depositpaid, bookingdates (checkin and checkout), and additionalneeds

### TC-05: Get booking by non-existent ID returns HTTP 404

- Type: Negative
- Priority: High

**Preconditions**

- A booking ID that does not exist is identified

**Steps**

1. Send GET request to /booking/{id} using an ID that does not exist
2. Inspect the HTTP status code

**Expected result:** API returns HTTP 404 Not Found

### TC-06: Get bookings filtered by both firstname and lastname returns matching booking IDs

- Type: Positive
- Priority: Medium

**Preconditions**

- At least one booking exists with a known firstname and lastname combination

**Steps**

1. Send GET request to /booking with query parameters firstname and lastname set to a known existing combination
2. Inspect the HTTP status code and response body

**Expected result:** API returns HTTP 200 OK and only booking IDs matching both firstname and lastname are returned

### TC-07: Get bookings filtered by non-existent name returns empty list

- Type: Negative
- Priority: Medium
- Requires clarification with the Product Owner

**Steps**

1. Send GET request to /booking with firstname set to a name that does not exist in the system
2. Inspect the HTTP status code and response body

**Expected result:** API returns HTTP 200 OK with an empty list of booking IDs; the requirements do not specify this behavior explicitly

### TC-08: Get booking with non-numeric ID is handled with an appropriate error response

- Type: Negative
- Priority: Medium
- Requires clarification with the Product Owner

**Steps**

1. Send GET request to /booking/abc
2. Inspect the HTTP status code and response body

**Expected result:** API returns an error response; the requirements do not specify the exact status code for invalid ID format

### TC-09: Response is returned in JSON format when JSON is requested

- Type: Positive
- Priority: Medium

**Preconditions**

- A booking with a known valid ID exists

**Steps**

1. Send GET request to /booking/{id} with header Accept set to application/json
2. Inspect the Content-Type header of the response
3. Parse the response body as JSON

**Expected result:** Response Content-Type is application/json and the body is valid JSON

### TC-10: Response structure of booking details matches expected schema

- Type: Positive
- Priority: Medium
- Requires clarification with the Product Owner

**Preconditions**

- A booking with a known valid ID exists

**Steps**

1. Send GET request to /booking/{id} with a valid ID
2. Validate that the response contains firstname as string, lastname as string, totalprice as number, depositpaid as boolean, bookingdates as object with checkin and checkout, and additionalneeds as string
3. Validate the response contains no unexpected top-level fields

**Expected result:** Response body conforms to the expected schema with correct field names and data types as defined in the acceptance criteria

### TC-11: Get booking with ID zero or negative value

- Type: Boundary
- Priority: Low
- Requires clarification with the Product Owner

**Steps**

1. Send GET request to /booking/0
2. Send GET request to /booking/-1
3. Inspect the HTTP status code for each request

**Expected result:** API returns HTTP 404 Not Found for IDs that do not correspond to an existing booking; the requirements do not explicitly define behavior for zero or negative IDs
