import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import db_init
    
    def main():
        """Main function to set up the database"""
        print("=" * 60)
        print("GYM MANAGEMENT SYSTEM - DATABASE SETUP")
        print("=" * 60)
        
        try:
            # Check if database already exists
            if db_init.check_database_exists():
                print("✓ Database already exists and is properly configured.")
                
                # Ask user if they want to reinitialize
                response = input("\nDo you want to reinitialize the database? (y/N): ").lower()
                if response not in ['y', 'yes']:
                    print("Database setup cancelled.")
                    return
                
                print("\nReinitializing database...")
            else:
                print("Database not found. Creating new database...")
            
            # Initialize the database
            db_init.initialize_database()
            
            print("\n" + "=" * 60)
            print("✓ DATABASE SETUP COMPLETED SUCCESSFULLY!")
            print("=" * 60)
            print("\nYour gym management system is now ready to use.")
            print("You can start the application with: python app.py")
            print("\nDefault login credentials:")
            print(f"Username: {os.getenv('ADMIN_USER', 'admin')}")
            print(f"Password: {os.getenv('ADMIN_PASS', 'admin')}")
            
        except Exception as e:
            print(f"\n❌ ERROR: Database setup failed!")
            print(f"Error details: {e}")
            print("\nPlease check your database configuration and try again.")
            sys.exit(1)
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    print(f"❌ ERROR: Could not import required modules: {e}")
    print("Please ensure all dependencies are installed.")
    sys.exit(1) 