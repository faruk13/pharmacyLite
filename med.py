from App import app, db
from App.models import User, Manuf, MedStock, ManufStock, BoughtBy, OrderMedFor

@app.shell_context_processor
def make_shell_context():
    return { 'db': db, 'User': User,
            'Manuf': Manuf, 'MedStock': MedStock,
            'ManufStock': ManufStock, 'BoughtBy': BoughtBy,
            'OrderMedFor': OrderMedFor}

