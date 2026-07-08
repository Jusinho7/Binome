#!/usr/bin/env python3
import os
try:
    from dotenv import load_dotenv
    HAVE_DOTENV = True
except Exception:
    HAVE_DOTENV = False


def main() -> None:
    print("ORACLE STATUS: Reading the Matrix...\n")
    key = [
        "MATRIX_MODE",
        "DATABASE_URL",
        "API_KEY",
        "LOG_LEVEL",
        "ZION_ENDPOINT"
    ]
    loaded_file = None
    if HAVE_DOTENV:
        try:
            load_dotenv()
        except Exception:
            pass

        overridden = any(keys in os.environ for keys in key)
        env_file = bool(loaded_file)

        matrix_mode = os.getenv("MATRIX_MODE")
        db_url = os.getenv("DATABASE_URL")
        api_key = os.getenv("API_KEY")
        log_level = os.getenv("LOG_LEVEL")
        zion_endpoint = os.getenv("ZION_ENDPOINT")

        print("Configuration loaded:")
        print(f"Mode: {matrix_mode}")
        print(f"Database: {db_url}")
        print(f"API Access: {api_key}")
        print(f"Log Level: {log_level}")
        print(f"Zion Network: {zion_endpoint}\n")

        print("Environment security check:")
        if matrix_mode not in ["production", "development"]:
            print(
                "Invalid MATRIX_MODE (expected 'production' or 'development')")
        print(
            "[OK] No hardcoded secrets detected"
            if not db_url and not api_key else "[KO] hardcoded secrets"
            "detected")
        print(
            "[OK] No override found"
            if not overridden else "[KO] Production overrides")
        print(
            "[OK] .env file properly configured"
            if env_file else "[KO] No .env file loaded")
        print("\nThe oracle sees all configurations.")

    else:
        print("No dotenv found")


if __name__ == "__main__":
    main()
