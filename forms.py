from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import IntegerField, DateField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    rememberMe = BooleanField('Remember Me')
    submit = SubmitField('Sign In for Admin')

class AddToMedStock(FlaskForm):
    #medId=IntegerField('Med Id', validators=[DataRequired()]) 
    medName=StringField('MedName', validators=[DataRequired()])
    toManufId=StringField('Manufacturer Id', validators=[DataRequired()])
    wantQnty=IntegerField('Order Quantity', validators=[DataRequired()])
    CO1=IntegerField('Price', validators=[DataRequired()])
    expDate=DateField('Expiry Date', format="%Y-%m-%d", validators=[DataRequired()])
    submit = SubmitField('Place Order to Manufacturer')

class CustomerOrder(FlaskForm):
    cusName=StringField('Customer Name', validators=[DataRequired()])
    medId=IntegerField('Med Id', validators=[DataRequired()])
    buyQnty=IntegerField('Buy Quantity', validators=[DataRequired()])
    #CO1=IntegerField('Price', validators=[DataRequired()])
    submit = SubmitField('Buy')
