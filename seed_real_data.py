#!/usr/bin/env python3
"""
Seed Crime Tracer with real Chennai police station data
"""
import asyncio
import sys
import logging
import csv
from datetime import datetime
from collections import defaultdict

from Backend.db import get_db_session, init_db
from Backend.models import Station, PoliceUser
from Backend.auth_router import hash_password
from sqlalchemy import select, func, text, delete

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def clear_existing_data():
    """Clear existing stations and users"""
    async with get_db_session() as session:
        # Delete all users first (due to foreign key constraints)
        await session.execute(delete(PoliceUser))
        # Delete all stations
        await session.execute(delete(Station))
        await session.commit()
        logger.info("Cleared existing data")

async def load_chennai_police_data():
    """Load real Chennai police station data from CSV"""
    
    # Read the CSV file
    csv_file = "Datasets/officer_roster_enriched.csv"
    stations_data = defaultdict(list)
    
    with open(csv_file, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            station_name = row['Police Station'].strip()
            if station_name and station_name != '':
                stations_data[station_name].append(row)
    
    logger.info(f"Found {len(stations_data)} unique police stations")
    
    # Create station code mapping (since we need unique codes)
    station_codes = {}
    station_counter = 1
    
    # Create stations
    async with get_db_session() as session:
        created_stations = {}
        
        for station_name, officers in stations_data.items():
            if not station_name or station_name.strip() == '':
                continue
                
            # Generate a unique station code
            station_code = f"CHE{station_counter:03d}"
            station_counter += 1
            
            # Get representative data from first officer entry
            first_officer = officers[0]
            zone = first_officer.get('Zone_x', '').strip()
            contact_no = first_officer.get('Contact No._x', '').strip()
            available_officers = first_officer.get('Available Officers', '0')
            
            try:
                officer_count = int(available_officers) if available_officers.isdigit() else len(officers)
            except:
                officer_count = len(officers)
            
            # Create station (we don't have lat/lng in this dataset)
            station = Station(
                station_name=station_name,
                station_code=station_code,
                address=f"{zone}, Chennai, Tamil Nadu" if zone else "Chennai, Tamil Nadu",
                officer_count=officer_count,
                created_at=datetime.utcnow()
            )
            
            session.add(station)
            await session.flush()  # Get the ID
            
            created_stations[station_name] = station
            logger.info(f"Created station: {station_name} ({station_code}) - {officer_count} officers")
        
        await session.commit()
        logger.info(f"Created {len(created_stations)} police stations")
        
        return created_stations

async def create_demo_users(stations):
    """Create demo admin and police users"""
    
    # Get a list of stations for assignment
    station_list = list(stations.values())
    
    users_data = [
        # Admin Users
        {
            "name": "Chennai Police Admin",
            "police_id": "ADMIN001",
            "password": "admin123",
            "email": "admin@chennaipolice.gov.in",
            "phone": "+91-9876543210",
            "batch": "2020",
            "is_admin": True,
            "approved": True,
            "station_id": station_list[0].id if station_list else None
        },
        {
            "name": "Zone Commander",
            "police_id": "ADMIN002", 
            "password": "admin456",
            "email": "zonecommander@chennaipolice.gov.in",
            "phone": "+91-9876543211",
            "batch": "2018",
            "is_admin": True,
            "approved": True,
            "station_id": station_list[1].id if len(station_list) > 1 else station_list[0].id if station_list else None
        },
        # Police Officers - using real station assignments
        {
            "name": "Inspector Kumar",
            "police_id": "POL001",
            "password": "police123",
            "email": "inspector.kumar@chennaipolice.gov.in", 
            "phone": "+91-9876543212",
            "batch": "2019",
            "is_admin": False,
            "approved": True,
            "station_id": station_list[0].id if station_list else None
        },
        {
            "name": "Constable Priya",
            "police_id": "POL002",
            "password": "police456", 
            "email": "constable.priya@chennaipolice.gov.in",
            "phone": "+91-9876543213",
            "batch": "2021",
            "is_admin": False,
            "approved": True,
            "station_id": station_list[1].id if len(station_list) > 1 else station_list[0].id if station_list else None
        },
        {
            "name": "Sub-Inspector Rajan",
            "police_id": "POL003",
            "password": "police789",
            "email": "si.rajan@chennaipolice.gov.in",
            "phone": "+91-9876543214", 
            "batch": "2020",
            "is_admin": False,
            "approved": True,
            "station_id": station_list[2].id if len(station_list) > 2 else station_list[0].id if station_list else None
        },
        {
            "name": "Inspector Meera",
            "police_id": "POL004",
            "password": "police101",
            "email": "inspector.meera@chennaipolice.gov.in",
            "phone": "+91-9876543215",
            "batch": "2018",
            "is_admin": False,
            "approved": True,
            "station_id": station_list[3].id if len(station_list) > 3 else station_list[0].id if station_list else None
        },
        {
            "name": "Constable Rajesh",
            "police_id": "POL005", 
            "password": "police202",
            "email": "constable.rajesh@chennaipolice.gov.in",
            "phone": "+91-9876543216",
            "batch": "2022",
            "is_admin": False,
            "approved": True,
            "station_id": station_list[4].id if len(station_list) > 4 else station_list[0].id if station_list else None
        }
    ]
    
    async with get_db_session() as session:
        for user_data in users_data:
            # Check if user already exists
            existing = await session.execute(
                select(PoliceUser).where(PoliceUser.police_id == user_data["police_id"])
            )
            if existing.scalar_one_or_none():
                logger.info(f"User {user_data['police_id']} already exists")
                continue
            
            # Hash password
            hashed_password = hash_password(user_data.pop("password"))
            user_data["password_hash"] = hashed_password
            user_data["created_at"] = datetime.utcnow()
            user_data["updated_at"] = datetime.utcnow()
            
            user = PoliceUser(**user_data)
            session.add(user)
            logger.info(f"Created user: {user.name} ({user.police_id})")
            
        await session.commit()
        logger.info("Demo users created successfully!")

async def display_station_summary(stations):
    """Display summary of loaded stations"""
    print("\n" + "="*80)
    print("CHENNAI POLICE STATIONS LOADED")
    print("="*80)
    
    for i, (name, station) in enumerate(stations.items(), 1):
        print(f"{i:2d}. {station.station_name} ({station.station_code})")
        print(f"    Officers: {station.officer_count}")
        if station.address:
            print(f"    Address: {station.address}")
        print()
    
    print(f"Total Stations: {len(stations)}")
    print("="*80)

async def display_login_credentials():
    """Display login credentials for testing"""
    print("\n" + "="*60)
    print("CRIME TRACER - LOGIN CREDENTIALS")
    print("="*60)
    print("\n🔐 ADMIN USERS:")
    print("┌─────────────┬──────────┬─────────────────────┐")
    print("│ Username    │ Password │ Role                │")
    print("├─────────────┼──────────┼─────────────────────┤")
    print("│ ADMIN001    │ admin123 │ Chennai Police Admin│")
    print("│ ADMIN002    │ admin456 │ Zone Commander      │")
    print("└─────────────┴──────────┴─────────────────────┘")
    
    print("\n👮 POLICE OFFICERS:")
    print("┌─────────────┬──────────┬─────────────────────┐")
    print("│ Username    │ Password │ Officer Name        │")
    print("├─────────────┼──────────┼─────────────────────┤")
    print("│ POL001      │ police123│ Inspector Kumar     │")
    print("│ POL002      │ police456│ Constable Priya     │")
    print("│ POL003      │ police789│ Sub-Inspector Rajan │")
    print("│ POL004      │ police101│ Inspector Meera     │")
    print("│ POL005      │ police202│ Constable Rajesh    │")
    print("└─────────────┴──────────┴─────────────────────┘")
    
    print("\n🌐 APPLICATION URLS:")
    print("• Frontend: http://localhost:5173")
    print("• Backend API: http://localhost:8000")
    print("• API Documentation: http://localhost:8000/docs")
    print("\n" + "="*60)

async def main():
    """Main execution function"""
    try:
        logger.info("Starting Crime Tracer real data seeding...")
        
        # Initialize database
        await init_db()
        
        # Clear existing data
        await clear_existing_data()
        
        # Load Chennai police station data
        logger.info("Loading Chennai police stations from dataset...")
        stations = await load_chennai_police_data()
        
        # Create demo users
        logger.info("Creating demo users...")
        await create_demo_users(stations)
        
        # Display summary
        await display_station_summary(stations)
        await display_login_credentials()
        
        logger.info("Real data seeding completed successfully!")
        
    except Exception as e:
        logger.error(f"Error during seeding: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())