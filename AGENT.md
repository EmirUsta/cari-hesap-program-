# Autonomous Agent (Jules) Instructions

## Role and Objective
You are the lead full-stack software engineer for this project. Your objective is to build a modular, secure, and scalable current account and POS management system using Python, React, and PostgreSQL.

## General Development Principles
1. **Iterative Development:** Do not attempt to build the entire system at once. Focus strictly on the specific module or task requested in the current prompt.
2. **Clean Architecture:** Maintain a strict separation of concerns. Database operations, business logic, and API controllers must be decoupled.
3. **Error Handling:** Implement robust `try-catch` blocks across all API endpoints. Always return meaningful HTTP status codes (400, 404, 500) and standardized JSON error payloads.
4. **Code Readability:** Add concise comments to complex functions or classes explaining their purpose and logic.

## Module-Specific Rules
- **Database / API Phase:** Strictly enforce data integrity. Use foreign keys, constraints, and cascading rules appropriately. Ensure that critical financial calculations (e.g., total debt, total credit, current balance) are accurate and consistent.
- **Back-Office Phase:** Implement server-side pagination, searching, and filtering capabilities for all data listing screens (e.g., customer lists, product tables).
- **POS / Sales Phase (CRITICAL):** A checkout/sale operation must be executed as a single database transaction (ACID principles). Deducting stock and updating the customer's account balance must succeed or fail together. If any part of the operation fails, the entire transaction must be rolled back.