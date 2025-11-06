#!/usr/bin/env python3
"""
Reset admin password
"""
import asyncio
import sys
from Backend.models import PoliceUser
from Backend.db import get_db_session, init_db
from Backend.auth_router import hash_password

async def reset_admin_password():
    """Reset admin password"""
    try:
        # Initialize database first
        await init_db()
        
        async with get_db_session() as session:
            # Get admin user
            from sqlalchemy import select
            result = await session.execute(
                select(PoliceUser).filter(PoliceUser.police_id == "ADMIN001")
            )
            admin = result.scalar_one_or_none()
            
            if not admin:
                print("ADMIN001 not found")
                return
            
            # Update password
            admin.password_hash = hash_password("AdminPass123")
            await session.commit()
            
            print("Admin password reset successfully!")
            print("Police ID: ADMIN001")
            print("Password: AdminPass123")
            
    except Exception as e:
        print(f"Error resetting admin password: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(reset_admin_password())