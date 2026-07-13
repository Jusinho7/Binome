try:
    from pydantic import BaseModel, Field, ValidationError, model_validator
    HAVE_PYDANTIC = True
except ImportError:
    HAVE_PYDANTIC = False


_ALLOWED_CONTACT_TYPES = {"radio", "visual", "physical", "telepathic"}


class AlienContact(BaseModel):
    contact_id: str = Field(..., min_length=5, max_length=15)
    timestamp: str
    location: str = Field(..., min_length=3, max_length=100)
    contact_type: str
    signal_strength: float = Field(..., ge=0.0, le=10.0)
    duration_minutes: int = Field(..., ge=1, le=1440)
    witness_count: int = Field(..., ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = False

    @model_validator(mode="after")
    def check_business_rules(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError('Contact ID must start with "AC"')
        if self.contact_type not in _ALLOWED_CONTACT_TYPES:
            raise ValueError(f"Invalid contact_type: {self.contact_type}")
        if (self.contact_type == "physical" and
                not self.is_verified):
            raise ValueError("Physical contact reports must be verified")
        if (self.contact_type == "telepathic" and
                self.witness_count < 3):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses")
        if (self.signal_strength > 7.0 and
                not self.message_received):
            raise ValueError(
                "Strong signals (> 7.0) should include received messages")
        return self


def print_alien(contact: AlienContact) -> None:
    print("Valid contact report:")
    print(f"ID: {contact.contact_id}")
    print(f"Type: {contact.contact_type}")
    print(f"Location: {contact.location}")
    print(f"Signal: {contact.signal_strength}/10")
    print(f"Duration: {contact.duration_minutes} minutes")
    print(f"Witnesses: {contact.witness_count}")
    print(f"Message: '{contact.message_received}'")


def main() -> None:
    print("Alien Contact Log Validation")
    print("=" * 40)
    if HAVE_PYDANTIC:
        try:
            contact = AlienContact(
                contact_id="AC_2024_001",
                timestamp="2026-07-14T00:00:00",
                contact_type="radio",
                location="Area 51, Nevada",
                signal_strength=8.5,
                duration_minutes=45,
                witness_count=5,
                message_received="Greetings from Zeta Reticuli"
            )
            print_alien(contact)
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
