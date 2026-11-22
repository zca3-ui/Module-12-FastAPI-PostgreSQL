
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.database.models import Calculation
from app.schemas.calculation import (
    CalculationCreate,
    CalculationRead,
    CalculationType,
)
from app.operations.factory import CalculationFactory


# Configure the calculations router
router = APIRouter(
    prefix="/calculations",
    tags=["Calculations"]
)


# Helper function to calculate and format the API response
def build_calculation_response(calculation: Calculation):
    """Build a response containing the calculation and its result."""

    calculation_type = CalculationType(calculation.type)

    result = CalculationFactory.calculate(
        calculation.a,
        calculation.b,
        calculation_type
    )

    return CalculationRead(
        id=calculation.id,
        a=calculation.a,
        b=calculation.b,
        type=calculation_type,
        result=result
    )


# BROWSE: Retrieve all calculations
@router.get(
    "/",
    response_model=list[CalculationRead]
)
def get_calculations(
    db: Session = Depends(get_db)
):
    """Retrieve all calculations from the database."""

    calculations = db.query(Calculation).order_by(
        Calculation.id
    ).all()

    return [
        build_calculation_response(calculation)
        for calculation in calculations
    ]


# READ: Retrieve one calculation by ID
@router.get(
    "/{calculation_id}",
    response_model=CalculationRead
)
def get_calculation(
    calculation_id: int,
    db: Session = Depends(get_db)
):
    """Retrieve a specific calculation by its ID."""

    calculation = db.query(Calculation).filter(
        Calculation.id == calculation_id
    ).first()

    if calculation is None:
        raise HTTPException(
            status_code=404,
            detail="Calculation not found."
        )

    return build_calculation_response(calculation)


# ADD: Create a new calculation
@router.post(
    "/",
    response_model=CalculationRead,
    status_code=status.HTTP_201_CREATED
)
def create_calculation(
    calculation_data: CalculationCreate,
    db: Session = Depends(get_db)
):
    """Create and save a new calculation."""

    new_calculation = Calculation(
        a=calculation_data.a,
        b=calculation_data.b,
        type=calculation_data.type.value
    )

    db.add(new_calculation)
    db.commit()
    db.refresh(new_calculation)

    return build_calculation_response(new_calculation)


# EDIT: Update an existing calculation
@router.put(
    "/{calculation_id}",
    response_model=CalculationRead
)
def update_calculation(
    calculation_id: int,
    calculation_data: CalculationCreate,
    db: Session = Depends(get_db)
):
    """Update an existing calculation."""

    calculation = db.query(Calculation).filter(
        Calculation.id == calculation_id
    ).first()

    if calculation is None:
        raise HTTPException(
            status_code=404,
            detail="Calculation not found."
        )

    calculation.a = calculation_data.a
    calculation.b = calculation_data.b
    calculation.type = calculation_data.type.value

    db.commit()
    db.refresh(calculation)

    return build_calculation_response(calculation)


# DELETE: Remove a calculation by ID
@router.delete(
    "/{calculation_id}"
)
def delete_calculation(
    calculation_id: int,
    db: Session = Depends(get_db)
):
    """Delete a calculation from the database."""

    calculation = db.query(Calculation).filter(
        Calculation.id == calculation_id
    ).first()

    if calculation is None:
        raise HTTPException(
            status_code=404,
            detail="Calculation not found."
        )

    db.delete(calculation)
    db.commit()

    return {
        "message": "Calculation deleted successfully."
    }
