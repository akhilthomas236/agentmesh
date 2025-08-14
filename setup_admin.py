#!/usr/bin/env python3
"""
Setup script for AutoGen A2A system.
Creates initial admin user and configures basic security.
"""

import asyncio
import sys
from getpass import getpass

from src.autogen_a2a.security import get_auth_manager
from src.autogen_a2a.security.permissions import Role


async def create_admin_user():
    """Create the initial admin user."""
    print("AutoGen A2A System Setup")
    print("=" * 30)
    print("This script will create the initial admin user for your system.\n")
    
    # Get user input
    username = input("Admin username [admin]: ").strip() or "admin"
    email = input("Admin email: ").strip()
    
    if not email:
        print("Error: Email is required")
        return False
    
    password = getpass("Admin password (min 8 chars): ")
    if len(password) < 8:
        print("Error: Password must be at least 8 characters")
        return False
    
    confirm_password = getpass("Confirm password: ")
    if password != confirm_password:
        print("Error: Passwords do not match")
        return False
    
    full_name = input("Full name (optional): ").strip() or None
    
    # Confirm details
    print(f"\nCreating admin user:")
    print(f"  Username: {username}")
    print(f"  Email: {email}")
    print(f"  Full name: {full_name or 'Not provided'}")
    
    confirm = input("\nProceed? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Setup cancelled.")
        return False
    
    # Create the user
    try:
        auth_manager = get_auth_manager()
        await auth_manager.connect()
        
        # Check if user already exists
        existing_user = await auth_manager.get_user_by_username(username)
        if existing_user:
            print(f"Error: User '{username}' already exists")
            return False
        
        # Create admin user
        user = await auth_manager.create_user(
            username=username,
            email=email,
            password=password,
            full_name=full_name,
            roles=[Role.ADMIN]
        )
        
        print(f"\n✓ Admin user created successfully!")
        print(f"  User ID: {user.id}")
        print(f"  Username: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Roles: {user.roles}")
        
        print(f"\nYou can now start the API server and login with these credentials.")
        print(f"API server command: python -m uvicorn src.autogen_a2a.api.main:app --reload")
        
        return True
        
    except Exception as e:
        print(f"Error creating admin user: {e}")
        return False
    finally:
        await auth_manager.disconnect()


def main():
    """Main setup function."""
    try:
        success = asyncio.run(create_admin_user())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nSetup cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"Setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
