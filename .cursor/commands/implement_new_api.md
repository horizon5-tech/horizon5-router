# Implement New API Endpoint

## Overview

Step-by-step guide to implement a new API endpoint following the project's patterns and standards.

## Prerequisites

- Use the `todo_write` tool to create and manage a task list before starting
- Break down the implementation into sequential, logical subtasks
- Always include a final validation task to ensure correctness

## Steps

### 1. Review Existing Structure

- Examine `apps/core/controllers/base.py` to understand the base controller pattern
- Review similar existing controllers (e.g., `backtest`, `orders`, `report`)
- Check `apps/core/models/base.py` to understand the model structure
- Review `apps/core/repositories/base.py` to understand data persistence methods

### 2. Create Controller

- Create controller file: `apps/core/controllers/{resource}/__init__.py`
- Extend `BaseController`
- Implement required HTTP methods (GET, POST, etc.)
- Add authentication classes if needed
- Initialize model in constructor: `self._model = {Resource}Model()`

### 3. Implement HTTP Method

- Extract data from `request.data` (POST/PUT) or `request.query_params` (GET)
- Validate request data using Cerberus (create private `_is_{method}_data_valid()` method)
- Use `self._model` methods (`find()`, `store()`, `update()`, `count()`) for data operations
- Handle exceptions with try/except blocks
- Return structured response using `self.response()` method
- Use appropriate `HttpStatus` enum values

### 4. Create Validation Method

- Create private method `_is_{method}_data_valid()` following the pattern in `BaseController`
- Use `Validator` from `cerberus` package
- Define validation schema with required fields, types, and constraints
- Return boolean result from `validator.validate()`

### 5. Update Schemas

- Locate or create schema file: `apps/core/controllers/{resource}/schemas/get.py`
- Create or update schema function (e.g., `post_schema()`, `get_schema()`)
- Define request body structure using `inline_serializer`
- Define response structure with appropriate status codes
- Use `@extend_schema` decorator on controller methods

### 6. Configure URLs

- Open `apps/core/urls.py`
- Add new path with appropriate route pattern
- Use `http_method_names` parameter to restrict methods if needed
- Follow naming convention: plural for collections (GET), singular for actions (POST)

### 7. Final Validation

- Run linter to check for errors
- Verify code follows project standards (no comments, clean structure)
- Ensure error handling is consistent with other controllers
- Confirm all imports are correct
- Test the endpoint functionality

## Important Notes

- Always use `todo_write` tool to track progress
- Follow existing patterns - don't create new conventions
- Validate all inputs with Cerberus
- Use `self.response()` for all JSON responses
- Handle exceptions appropriately
- Keep code clean and maintainable
