# Requirements Analysis Report

## Summary

- Missing information: 16
- Ambiguities: 8
- Inconsistencies: 2
- Questions for Product Owner: 15

## Requirements Analysis

The user story and acceptance criteria for retrieving bookings are generally clear and testable for the happy paths (GET /booking, GET /booking/{id}, 200 and 404 responses). However, the requirements leave the filter behaviour, the response schema, error handling for invalid input, and non-functional aspects largely unspecified, so test design would require assumptions.

### Missing information (16)

- **M1.** Definition of the expected response schema (field names, data types, nesting of the booking dates object, and whether 'Additional needs' is optional) — 'Response structure matches the expected schema' references a schema that is not provided
- **M2.** Filter behaviour for GET /booking: accepted query parameter names, case sensitivity, combined firstname and lastname semantics (AND vs OR), and behaviour when no bookings match
- **M3.** Response status and body for invalid or non-numeric booking IDs on GET /booking/{id} (only 404 for non-existent IDs is specified)
- **M4.** Behaviour when the request is malformed or the query parameters are invalid (e.g., empty values, special characters, overly long strings)
- **M5.** Expected response for unsupported methods (POST, PUT, PATCH, DELETE) even though the endpoint is listed as GET-only
- **M6.** Expected behaviour when the requested format is not JSON (e.g., Accept: application/xml) — the criterion says JSON when JSON is requested but does not define the alternative
- **M7.** Error response body format for 404 and other error cases
- **M8.** Performance expectations such as response time limits, timeouts, and behaviour under load or with large numbers of bookings
- **M9.** Pagination or limits on the size of the list returned by GET /booking
- **M10.** Ordering of the returned booking IDs
- **M11.** Security requirements such as HTTPS enforcement, rate limiting, and handling of sensitive booking data
- **M12.** Concurrency and data consistency expectations when bookings are created or deleted during retrieval
- **M13.** Data types and value constraints for total price, deposit paid status, and booking dates (date format, valid ranges)
- **M14.** Localization and accessibility considerations, where applicable to an API (for example, character encoding of names with non-ASCII characters)
- **M15.** Whether the 'registered user' role has any effect, given that authentication is stated as not required
- **M16.** Availability and uptime expectations for the external Heroku-hosted service

### Ambiguities (8)

- **A1.** "User can retrieve booking IDs filtered by firstname and/or lastname" — does not state the parameter names, matching rules (exact or partial, case-sensitive or not), or the result when no match exists
- **A2.** "Response structure matches the expected schema" — refers to an undefined schema
- **A3.** "API returns data in JSON format when JSON is requested" — does not specify how the request states the format or what happens otherwise
- **A4.** "Appropriate HTTP status codes are returned for successful and unsuccessful requests" — 'appropriate' and 'unsuccessful' are not defined, so no specific codes are testable beyond 200 and 404
- **A5.** "As a registered user" versus "Authentication: Not required for retrieving booking information" — the role is stated but has no defined effect
- **A6.** "I want to be able to use the https://restful-booker.herokuapp.com/booking endpoint, so that I can ... manage booking information" — the user story mentions managing bookings, but the API details state only GET is supported
- **A7.** "Booking dates" — does not specify whether this is a checkin and checkout pair, the date format, or whether both are required
- **A8.** "Additional needs" — does not state whether the field is mandatory or may be empty or null

### Inconsistencies (2)

- **I1.** User story states the user wants to "retrieve and manage booking information" while API Details state "Supported methods: GET" only; management (create, update, delete) is implied but not supported or excluded explicitly
- **I2.** "Authentication: Not required for retrieving booking information" versus "As a registered user" — it is unclear whether registration or any credentials are relevant to the scope of this story

### Questions for Product Owner (15)

- [ ] **Q1.** What is the exact expected response schema, including field names, data types, and the structure of the booking dates object?
- [ ] **Q2.** What are the query parameter names for filtering by firstname and lastname, and do they match exactly, partially, or case-insensitively?
- [ ] **Q3.** When both firstname and lastname are supplied, should results match both (AND) or either (OR)?
- [ ] **Q4.** What should GET /booking return when no bookings match the filter: an empty list with 200, or 404?
- [ ] **Q5.** What status code and body should be returned for a non-numeric or malformed booking ID?
- [ ] **Q6.** What status codes are expected for unsupported methods such as POST, PUT, PATCH, and DELETE on /booking and /booking/{id}?
- [ ] **Q7.** How is JSON requested (Accept header or other means), and what response is expected when another format is requested?
- [ ] **Q8.** Is there a defined error response body format for 404 and other error responses?
- [ ] **Q9.** What are the response time targets, timeouts, and expected behaviour under concurrent load?
- [ ] **Q10.** Is pagination or a maximum number of returned IDs required for GET /booking?
- [ ] **Q11.** Is there a defined ordering for the returned booking IDs?
- [ ] **Q12.** Are there any security requirements, such as HTTPS-only access, rate limiting, or restrictions on exposing booking data?
- [ ] **Q13.** Are there validation rules for the data types and ranges of total price, deposit paid status, booking dates, and additional needs?
- [ ] **Q14.** Does the 'registered user' role have any effect on what the user can retrieve, given that no authentication is required?
- [ ] **Q15.** Is the story scope limited to retrieval only, or do the 'manage booking information' goal and any future POST, PUT, PATCH, or DELETE operations belong to this story?
