from datetime import datetime
try:
    from pydantic import BaseModel, Field, ValidationError
    HAVE_PYDANTIC = True
except ImportError:
    HAVE_PYDANTIC = False


class SpaceStation(BaseModel):
    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.0)
    oxygen_level: float = Field(..., ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(default=None, max_length=200)


def print_station(station: SpaceStation) -> None:
    print("Valid station created:")
    print(f"ID: {station.station_id}")
    print(f"Name: {station.name}")
    print(f"Crew: {station.crew_size} people")
    print(f"Power: {station.power_level}%")
    print(f"Oxygen: {station.oxygen_level}%")
    print(f"Last Maintenance: {station.last_maintenance}")
    if station.is_operational:
        print("Status: Operational")
    if station.notes:
        print(f"Notes: {station.notes}")


def main() -> None:
    print("Space Station Data Validation")
    print("=" * 40)
    if HAVE_PYDANTIC:
        try:
            station = SpaceStation(
                station_id="ISS001",
                name="International space station",
                crew_size=6,
                power_level=85.5,
                oxygen_level=92.3,
                last_maintenance=datetime.now(),
                is_operational=True
            )
            print_station(station)
        except TypeError as ty:
            print(f"Error typing: {ty}")
        except ValidationError as exc:
            print("Expected validation error:")
            print(exc.errors()[0]["msg"])
        except Exception as e:
            print(f"Error: {e}")
        finally:
            print()
            print("=" * 40)
    else:
        print("Pydantic is not installed.")


if __name__ == "__main__":
    main()
