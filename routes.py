from flask import render_template, flash, redirect, url_for, session
from App import app, db
from App.forms import LoginForm, AddToMedStock, CustomerOrder
from flask_login import current_user, login_user
from App.models import User, Manuf, MedStock, ManufStock, BoughtBy, OrderMedFor
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from datetime import date
import datetime

@app.route('/')
@app.route('/index')
@login_required
def index():
   # user = {'username': 'admin'}
    info=None
    for m in MedStock.query.all():
        g=m.availQnty
        if g < 300 :
            flash(str(m.medName + ' is low on stock, Order now!'), 'info')
    return render_template('index.html' ,title='Pharmacy', medicinestock=MedStock.query.all(), info=info)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated: #already logged in ..so dont login again
        return redirect(url_for('index'))
    form= LoginForm()
    if form.validate_on_submit(): #checks if all reqd fields are entered?
        flash('Login requested for user {}'.format(form.username.data))
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            #checks with pass entered by input user
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=True) #form.rememberMe.data
        next_page = request.args.get('next')
        #using next as one of the arg to get next page url
        if not next_page or url_parse(next_page).netloc != '': 
            #next arg has no val in url then go to index
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/addToMedStock', methods=['GET', 'POST'])
def addToMedStock():
    form=AddToMedStock()
    info=None
    flash('To add to our Pharmacy Medicine Stock we need to order from manufacturer')
    if form.validate_on_submit():
        o1=MedStock.query.filter_by(medName=form.medName.data).first()
        orders=OrderMedFor(medId=o1.medId,
                           medName=form.medName.data,
                           toManufId=form.toManufId.data,
                           wantQnty=form.wantQnty.data,  
                           byDate=date.today())

        db.session.add(orders)
        db.session.commit()
        flash('Order placed successfully!')
        med2=MedStock.query.filter_by(medName=form.medName.data,manufId=form.toManufId.data).first()
        newQnty=int(form.wantQnty.data)
        med2.availQnty += newQnty 
        med2.CO1= int(form.CO1.data)
        med2.expDate = form.expDate.data
        db.session.commit()

        flash(str(form.medName.data + ' stock has been updated(increased) in MedStock'),'info') 
        man=ManufStock.query.filter_by(manufId=form.toManufId.data,
                                       availMedId=o1.medId).first()
        man.availManufQnty -= newQnty
        db.session.commit()       
        return redirect(url_for('index'))
    return render_template('addToMedStock.html',  title='Order Medicine', 
                                            form=form,     
                                            manufacturerstock= ManufStock.query.all(),
                                            manufList=Manuf.query.all(),info=info)

@app.route('/customerOrder', methods=['GET', 'POST'])
def customerOrder():
    form=CustomerOrder()
    info1=None
    info2=None
    if form.validate_on_submit():
        m=MedStock.query.filter_by(medId=form.medId.data).first()
        if form.buyQnty.data > m.availQnty :
            flash(str('Your order for '+str(form.buyQnty.data)+' '+m.medName + ' is out of stock, We only have '+ str(m.availQnty)+ ' pieces.' ), 'info')
            return redirect(url_for('customerOrder'))
        cus=BoughtBy(cusName=form.cusName.data, medId=form.medId.data,
                    buyQnty=form.buyQnty.data, date=datetime.datetime.now(),
                    CO1=m.CO1)
        db.session.add(cus)
        db.session.commit()
        flash(str('Buyer '+ form.cusName.data+ ' is added to Customer List. '), 'info2')

        med1=MedStock.query.filter_by(medId=form.medId.data).first()
        med1.availQnty -= int(form.buyQnty.data)       
        db.session.commit()
        flash(str(med1.medName + ' stock has been updated(reduced) in MedStock'), 'info1')

        return redirect(url_for('index')) ##who bought what url should also be added
    return render_template('customerOrder.html', title='Customer Order', form=form,
                                                    medicinestock=MedStock.query.all(), 
                                                    info1=info1, info2=info2)
        
@app.route('/previousOrders', methods=['GET', 'POST'])
def previousOrders():
    #m=MedStock.query.filter_by(medId=form.medId.data).first()
    totCost=int(1)
    return render_template('previousOrders.html', title='Previous Orders',
                                                boughtList=BoughtBy.query.all(),
                                                m=MedStock.query.all(),
                                                totCost=totCost)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
    
