from fastapi import FastAPI, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.database import engine, Base, get_db
from app.models import Person
from app.schemas import PersonRequest, PersonUpdate, PersonResponse


Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/api/v1/persons", response_model=list[PersonResponse])
def get_persons(db: Session = Depends(get_db)):
    return db.query(Person).all()


@app.get("/api/v1/persons/{person_id}", response_model=PersonResponse)
def get_person(person_id: int, db: Session = Depends(get_db)):
    person = db.query(Person).filter(Person.id == person_id).first()

    if person is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Person not found"
        )

    return person


@app.post("/api/v1/persons", status_code=status.HTTP_201_CREATED)
def create_person(person: PersonRequest, db: Session = Depends(get_db)):
    new_person = Person(
        name=person.name,
        age=person.age,
        address=person.address,
        work=person.work
    )

    db.add(new_person)
    db.commit()
    db.refresh(new_person)

    return Response(
        status_code=status.HTTP_201_CREATED,
        headers={
            "Location": f"/api/v1/persons/{new_person.id}"
        }
    )


@app.patch("/api/v1/persons/{person_id}", response_model=PersonResponse)
def update_person(
    person_id: int,
    person: PersonUpdate,
    db: Session = Depends(get_db)
):
    existing_person = (
        db.query(Person)
        .filter(Person.id == person_id)
        .first()
    )

    if existing_person is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Person not found"
        )

    update_data = person.model_dump(exclude_unset=True, exclude_none=True)

    for field, value in update_data.items():
        setattr(existing_person, field, value)

    db.commit()
    db.refresh(existing_person)

    return existing_person


@app.delete("/api/v1/persons/{person_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(person_id: int, db: Session = Depends(get_db)):
    person = db.query(Person).filter(Person.id == person_id).first()

    if person is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Person not found"
        )

    db.delete(person)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)