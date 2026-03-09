from src.common.db import get_connection


def main() -> None:
    print("1) opening DB connection...")

    with get_connection() as conn:
        print("2) connected")

        with conn.cursor() as cur:
            print("3) running validation query...")
            cur.execute("SELECT current_database(), current_user, now();")
            row = cur.fetchone()
            print("4) result:", row)

    print("5) DB connection successful")


if __name__ == "__main__":
    main()