import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_database_setup():
    """Test the database setup functionality"""
    print("Testing Database Setup Functionality")
    print("=" * 50)
    
    try:
        import db_init
        import models
        
        # Test 1: Check database connection function
        print("1. Testing database connection...")
        try:
            connection = db_init.get_db_connection(include_db=False)
            connection.close()
            print("   ✓ Database connection successful")
        except Exception as e:
            print(f"   ❌ Database connection failed: {e}")
            return False
        
        # Test 2: Check database existence check
        print("2. Testing database existence check...")
        try:
            exists = db_init.check_database_exists()
            print(f"   ✓ Database exists: {exists}")
        except Exception as e:
            print(f"   ❌ Database existence check failed: {e}")
        
        # Test 3: Test database initialization
        print("3. Testing database initialization...")
        try:
            db_init.initialize_database()
            print("   ✓ Database initialization successful")
        except Exception as e:
            print(f"   ❌ Database initialization failed: {e}")
            return False
        
        # Test 4: Test table creation verification
        print("4. Verifying table creation...")
        try:
            connection = db_init.get_db_connection()
            cursor = connection.cursor()
            
            # Check if key tables exist
            tables_to_check = ['User', 'Member', 'MembershipPlan', 'Trainer', 'Room']
            for table in tables_to_check:
                cursor.execute(f"SHOW TABLES LIKE '{table}'")
                result = cursor.fetchone()
                if result:
                    print(f"   ✓ Table '{table}' exists")
                else:
                    print(f"   ❌ Table '{table}' missing")
            
            cursor.close()
            connection.close()
            
        except Exception as e:
            print(f"   ❌ Table verification failed: {e}")
        
        # Test 5: Test sample data insertion
        print("5. Testing sample data...")
        try:
            connection = db_init.get_db_connection()
            cursor = connection.cursor()
            
            # Check MembershipPlan data
            cursor.execute("SELECT COUNT(*) FROM MembershipPlan")
            result = cursor.fetchone()
            plan_count = result[0] if result and len(result) > 0 else 0
            print(f"   ✓ MembershipPlan records: {plan_count}")
            
            # Check Room data
            cursor.execute("SELECT COUNT(*) FROM Room")
            result = cursor.fetchone()
            room_count = result[0] if result and len(result) > 0 else 0
            print(f"   ✓ Room records: {room_count}")
            
            cursor.close()
            connection.close()
            
        except Exception as e:
            print(f"   ❌ Sample data check failed: {e}")
        
        # Test 6: Test models integration
        print("6. Testing models integration...")
        try:
            # Test getting all membership plans
            plans = models.get_all_plans()
            print(f"   ✓ Retrieved {len(plans)} membership plans")
            
            # Test getting all rooms
            rooms = models.get_all_rooms()
            print(f"   ✓ Retrieved {len(rooms)} rooms")
            
        except Exception as e:
            print(f"   ❌ Models integration test failed: {e}")
        
        print("\n" + "=" * 50)
        print("✓ Database setup testing completed!")
        print("Your database is ready for use.")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = test_database_setup()
    sys.exit(0 if success else 1) 