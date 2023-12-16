from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

from flask import Flask, render_template, request, url_for, redirect, flash

import random

app = Flask(__name__)
app.config['SECRET_KEY'] = str(random.random())

db = SQLAlchemy(app)

class Manufacturers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.Date)
    revenue = db.Column(db.Integer)

class Circuits(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.Date)
    frequency = db.Column(db.Numeric(10, 3))
    manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturers.id'))
    manufacturers = db.relationship('Manufacturers')

@app.route('/manufacturer_add', methods=['GET', 'POST'])
def manufacturer_add():
    if request.method == 'POST':
        name = request.form['name']
        created_at = datetime.strptime(request.form['created_at'], '%Y-%m-%d')
        revenue = int(request.form['revenue'])

        new_manufacturer = Manufacturers(name=name, created_at=created_at, revenue=revenue)
        db.session.add(new_manufacturer)
        try:
            db.session.commit()
            return redirect(url_for('manufacturers'))
        except Exception:
            db.session.rollback()
            flash('There was an error adding the manufacturer. Please try again.', 'error')
    return render_template('manufacturer_add.html')

@app.route('/manufacturer_edit/<int:manufacturer_id>', methods=['GET', 'POST'])
def manufacturer_edit(manufacturer_id):
    manufacturer = Manufacturers.query.get_or_404(manufacturer_id)
    if request.method == 'POST':
        manufacturer.name = request.form['name']
        manufacturer.created_at = datetime.strptime(request.form['created_at'], '%Y-%m-%d')
        manufacturer.revenue = int(request.form['revenue'])

        try:
            db.session.commit()
            flash('Manufacturer updated successfully!', 'success')
            return redirect(url_for('manufacturers'))
        except Exception:
            db.session.rollback()
            flash('There was an error updating the Manufacturer. Please try again.', 'error')

    return render_template('manufacturer_edit.html', manufacturer=manufacturer)

@app.route('/manufacturer_delete/<int:manufacturer_id>', methods=['GET'])
def manufacturer_delete(manufacturer_id):
    manufacturer = Manufacturers.query.get_or_404(manufacturer_id)
    circuits = Circuits.query.filter_by(manufacturer_id=manufacturer.id).all()
    if circuits:
        flash(f'Cannot delete manufacturer {manufacturer.name} because there are circuits that use it.', 'error')
        return redirect(url_for('manufacturers'))
    db.session.delete(manufacturer)
    db.session.commit()
    return redirect(url_for('manufacturers'))

@app.route('/')
def manufacturers():
    manufacturers = Manufacturers.query.all()
    highlight = request.args.get('highlight')
    return render_template('manufacturers.html', manufacturers=manufacturers, hightlight=highlight)

@app.route('/circuits')
def circuits():
    circuits = Circuits.query.all()
    manufacturers = Manufacturers.query.all()
    return render_template('circuits.html', circuits=circuits, manufacturers=manufacturers)

@app.route('/circuit_add', methods=['GET', 'POST'])
def circuit_add():
    if request.method == 'POST':
        name = request.form['name']
        frequency = float(request.form['frequency'])
        created_at = datetime.strptime(request.form['created_at'], '%Y-%m-%d')
        manufacturer_id = int(request.form['manufacturer_id'])

        if manufacturer_id:
            new_circuit = Circuits(
                name=name,
                frequency=frequency,
                created_at=created_at,
                manufacturer_id=manufacturer_id
            )
            db.session.add(new_circuit)
            try:
                db.session.commit()
                flash('Circuit added successfully!', 'success')
                return redirect(url_for('circuits'))
            except Exception as e:
                db.session.rollback()
                flash(str(e), 'error')
        else:
            flash('Manufacturer must be selected.', 'error')
    manufacturers = Manufacturers.query.all()
    return render_template('circuit_add.html', manufacturers=manufacturers)

@app.route('/circuit_edit/<int:circuit_id>', methods=['GET', 'POST'])
def circuit_edit(circuit_id):
    circuit = Circuits.query.get_or_404(circuit_id)
    if request.method == 'POST':
        circuit.name = request.form['name']
        circuit.frequency = float(request.form['frequency'])
        circuit.created_at = datetime.strptime(request.form['created_at'], '%Y-%m-%d')
        circuit.manufacturer_id = int(request.form['manufacturer_id'])

        if circuit.manufacturer_id:
            try:
                db.session.commit()
                flash('Circuit added successfully!', 'success')
                return redirect(url_for('circuits'))
            except Exception as e:
                db.session.rollback()
                flash(str(e), 'error')
        else:
            flash('Manufacturer must be selected.', 'error')
    manufacturers = Manufacturers.query.all()
    return render_template('circuit_edit.html', circuit=circuit, manufacturers=manufacturers)

@app.route('/circuit_delete/<int:circuit_id>', methods=['GET'])
def circuit(circuit_id):
    circuit = Circuits.query.get_or_404(circuit_id)
    db.session.delete(circuit)
    db.session.commit()
    return redirect(url_for('circuits'))


db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
