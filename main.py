from app import app_main

"""
this only happened when we deploy this application
"""
apps = app_main()
apps.app_context().push()
if __name__ == "__main__":
    apps.run(debug=True)
