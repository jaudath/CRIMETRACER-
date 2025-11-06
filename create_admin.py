#!/usr/bin/env python3
"""
Quick script to create an admin user in the database
"""
import asyncio
import sys
from Backend.models import PoliceUser
from Backend.db import get_db_session, init_db
from Backend.auth_router import hash_password

async def create_admin():
    """Create an admin user"""
    try:
        # Initialize database first
        await init_db()
        
        async with get_db_session() as session:
            # Check if admin already exists
            from sqlalchemy import select
            result = await session.execute(
                select(PoliceUser).filter(PoliceUser.is_admin == True)
            )
            existing_admins = result.scalars().all()
            
            if existing_admins:
                print(f"Admin(s) already exist:")
                for admin in existing_admins:
                    print(f"  - {admin.police_id} ({admin.name})")
                return
            
            # Create admin user
            admin_user = PoliceUser(
                police_id="ADMIN001",
                name="Admin User",
                password_hash=hash_password("AdminPass123"),
                station_id=1,  # Assign to first station
                email="admin@crimetracer.com",
                phone="9000000000",
                approved=True,
                needs_admin_approval=False,
                is_admin=True
            )
            
            session.add(admin_user)
            await session.commit()
            
            print("Admin user created successfully!")
            print("Police ID: ADMIN001")
            print("Password: AdminPass123")
            
    except Exception as e:
        print(f"Error creating admin user: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(create_admin())