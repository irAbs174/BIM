#!/usr/bin/env python3
"""
Database seeder for creating initial admin user.

This script creates an initial admin user if no admin users exist in the database.
It can be run manually or as part of the application setup process.

Usage:
    python -m app.seeder
    or
    python app/seeder.py
"""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.models import User, Base
from app.core.security import hash_password


def create_admin_user(
    username: str = None,
    email: str = None,
    password: str = None
) -> User:
    """
    Create an admin user with the provided credentials.

    Args:
        username: Admin username (default from env or 'admin')
        email: Admin email (default from env or 'admin@geobiro.ba')
        password: Admin password (default from env or 'admin123')

    Returns:
        The created User object

    Raises:
        ValueError: If user creation fails
    """
    # Set defaults from environment or fallback
    username = username or os.getenv('ADMIN_USERNAME', 'admin')
    email = email or os.getenv('ADMIN_EMAIL', 'admin@geobiro.ba')
    password = password or os.getenv('ADMIN_PASSWORD', 'admin123')

    print(f"Creating admin user: {username} ({email})")
    print(f"Password: '{password}', length: {len(password)}")

    # Create database session
    db = SessionLocal()
    try:
        # Check if admin already exists
        existing_admin = db.query(User).filter(User.is_admin == True).first()
        if existing_admin:
            print(f"Admin user already exists: {existing_admin.username}")
            return existing_admin

        # Check if username or email already taken
        existing_user = db.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            if existing_user.username == username:
                raise ValueError(f"Username '{username}' already exists")
            else:
                raise ValueError(f"Email '{email}' already exists")

        # Create new admin user
        hashed_password = hash_password(password)
        admin_user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_admin=True,
            is_active=True
        )

        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        print(f"Admin user created successfully: {admin_user.username}")
        print(f"Login credentials: {username} / {password}")

        return admin_user

    except Exception as e:
        db.rollback()
        raise ValueError(f"Failed to create admin user: {str(e)}")
    finally:
        db.close()


def main():
    """Main entry point for the seeder script."""
    import argparse

    parser = argparse.ArgumentParser(description='Create initial admin user')
    parser.add_argument('--username', help='Admin username')
    parser.add_argument('--email', help='Admin email')
    parser.add_argument('--password', help='Admin password')
    parser.add_argument('--force', action='store_true',
                       help='Force creation even if admin exists (will skip if exists)')

    args = parser.parse_args()

    try:
        # Ensure database tables exist
        Base.metadata.create_all(bind=engine)
        print("Database tables verified/created")

        # Create admin user
        admin_user = create_admin_user(
            username=args.username,
            email=args.email,
            password=args.password
        )

        print("\n✅ Admin user setup complete!")
        print(f"Username: {admin_user.username}")
        print(f"Email: {admin_user.email}")
        print(f"Admin: {admin_user.is_admin}")
        print("\n⚠️  IMPORTANT: Change the default password after first login!")

    except ValueError as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()