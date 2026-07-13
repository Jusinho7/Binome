from enum import Enum
from datetime import datetime
from typing import List
try:
    from pydantic import BaseModel, Field, ValidationError, model_validator
    HAVE_PYDANTIC = True
except ImportError:
    HAVE_PYDANTIC = False


class Rank(str, Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(..., ge=1, le=3650)
    crew: List[CrewMember] = Field(..., min_length=1, max_length=12)
    mission_status: str = "planned"
    budget_millions: float = Field(..., ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def check_safety_requirements(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError('Mission ID must start with "M"')
        if not any(
            member.rank in {Rank.COMMANDER, Rank.CAPTAIN}
            for member in self.crew
        ):
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )
        if (
            self.duration_days > 365
            and sum(member.years_experience >= 5 for member in self.crew)
            < len(self.crew) / 2
        ):
            raise ValueError(
                "Long missions (> 365 days) need 50% experienced crew "
                "(5+ years)"
            )
        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")
        return self


def print_mission(mission: SpaceMission) -> None:
    print("Valid mission created:")
    print(f"Mission: {mission.mission_name}")
    print(f"ID: {mission.mission_id}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days} days")
    print(f"Budget: ${mission.budget_millions}M")
    print(f"Crew size: {len(mission.crew)}")
    print("Crew members:")
    for member in mission.crew:
        print(
            f"- {member.name} ({member.rank.value}) - {member.specialization}"
        )


def main() -> None:
    print("Space Mission Crew Validation")
    print("=" * 40)
    crew = [
        CrewMember(
            member_id="C001",
            name="Sarah Connor",
            rank=Rank.COMMANDER,
            age=45,
            specialization="Mission Command",
            years_experience=20,
        ),
        CrewMember(
            member_id="C002",
            name="John Smith",
            rank=Rank.LIEUTENANT,
            age=34,
            specialization="Navigation",
            years_experience=8,
        ),
        CrewMember(
            member_id="C003",
            name="Alice Johnson",
            rank=Rank.OFFICER,
            age=29,
            specialization="Engineering",
            years_experience=6,
        ),
    ]
    if HAVE_PYDANTIC:
        try:
            mission = SpaceMission(
                mission_id="M2024_MARS",
                mission_name="Mars Colony Establishment",
                destination="Mars",
                launch_date=datetime(2024, 6, 1, 8, 0, 0),
                duration_days=900,
                crew=crew,
                budget_millions=2500.0,
            )
            print_mission(mission)
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
