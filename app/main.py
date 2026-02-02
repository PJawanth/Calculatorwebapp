"""FastAPI Calculator Application Entry Point."""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app.calculator import DivisionByZeroError, add, divide, multiply, subtract
from app.config import get_settings

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    description="A production-ready calculator REST API",
    version="1.0.0",
)

# Serve static files
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


@app.get("/", include_in_schema=False)
async def root():
    """Serve the calculator UI."""
    return FileResponse(static_dir / "index.html")


class OperationRequest(BaseModel):
    """Request model for calculator operations."""

    a: float
    b: float


class OperationResponse(BaseModel):
    """Response model for calculator operations."""

    result: float


class HealthResponse(BaseModel):
    """Response model for health check."""

    status: str


@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check() -> HealthResponse:
    """Health check endpoint.

    Returns:
        Health status of the application.
    """
    return HealthResponse(status="ok")


@app.post("/add", response_model=OperationResponse, tags=["Operations"])
async def add_numbers(request: OperationRequest) -> OperationResponse:
    """Add two numbers.

    Args:
        request: Operation request containing two numbers.

    Returns:
        Result of the addition.
    """
    result = add(request.a, request.b)
    return OperationResponse(result=result)


@app.post("/sub", response_model=OperationResponse, tags=["Operations"])
async def subtract_numbers(request: OperationRequest) -> OperationResponse:
    """Subtract two numbers.

    Args:
        request: Operation request containing two numbers.

    Returns:
        Result of the subtraction.
    """
    result = subtract(request.a, request.b)
    return OperationResponse(result=result)


@app.post("/mul", response_model=OperationResponse, tags=["Operations"])
async def multiply_numbers(request: OperationRequest) -> OperationResponse:
    """Multiply two numbers.

    Args:
        request: Operation request containing two numbers.

    Returns:
        Result of the multiplication.
    """
    result = multiply(request.a, request.b)
    return OperationResponse(result=result)


@app.post("/div", response_model=OperationResponse, tags=["Operations"])
async def divide_numbers(request: OperationRequest) -> OperationResponse:
    """Divide two numbers.

    Args:
        request: Operation request containing two numbers.

    Returns:
        Result of the division.

    Raises:
        HTTPException: If division by zero is attempted.
    """
    try:
        result = divide(request.a, request.b)
        return OperationResponse(result=result)
    except DivisionByZeroError as e:
        raise HTTPException(status_code=400, detail=e.message) from None
