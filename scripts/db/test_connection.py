from __future__ import annotations

from src.common.db import db_connection


def main() -> None:
    with db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                select
                    current_database()::text,
                    current_user::text,
                    inet_server_addr()::text
                """
            )
            row = cur.fetchone()

    if row is None:
        raise RuntimeError("Connection test query returned no rows.")

    db_name, db_user, server_addr = row

    print("Database connection successful.")
    print(f"database   : {db_name}")
    print(f"user       : {db_user}")
    print(f"server_addr: {server_addr}")


if __name__ == "__main__":
    main()