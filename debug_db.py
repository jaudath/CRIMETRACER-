#!/usr/bin/env python3
"""
Debug database to see actual data
"""
import asyncio
import sys
from Backend.models import Complaint, PoliceUser
from Backend.db import get_db_session, init_db

async def debug_db():
    """Debug database contents"""
    try:
        await init_db()
        
        async with get_db_session() as session:
            from sqlalchemy import select
            
            # Get all complaints
            result = await session.execute(
                select(Complaint).order_by(Complaint.created_at.desc())
            )
            complaints = result.scalars().all()
            
            print("=== Database Complaints ===")
            for complaint in complaints:
                print(f"ID: {complaint.complaint_id}")
                print(f"  Status: {complaint.status}")
                print(f"  Assigned Police ID: {complaint.assigned_police_id}")
                print(f"  Accepted By: {complaint.accepted_by}")
                print(f"  Station ID: {complaint.station_id}")
                print(f"  Created: {complaint.created_at}")
                print("---")
            
            # Get all police users
            result = await session.execute(select(PoliceUser))
            users = result.scalars().all()
            
            print("\n=== Police Users ===")
            for user in users:
                print(f"ID: {user.id}, Police ID: {user.police_id}, Name: {user.name}")
                
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(debug_db())