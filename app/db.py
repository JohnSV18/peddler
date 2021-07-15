from flask import g, current_app

def get_db():
    
    if "db" not in g:
        g.db = current_app.app.config["DATABASE"]
        
    return g.db 
