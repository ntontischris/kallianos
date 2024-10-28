from flask import Blueprint, jsonify, request
from models import db, Payment, Invoice, FinancialReport

financial_bp = Blueprint('financial', __name__)

@financial_bp.route('/payments', methods=['GET'])
def get_payments():
    """Retrieve all payments for a specific user."""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID must be provided'}), 400

    payments = Payment.query.filter_by(user_id=user_id).all()
    return jsonify([p.to_dict() for p in payments])

@financial_bp.route('/payments', methods=['POST'])
def create_payment():
    """Record a new payment."""
    data = request.json
    user_id = data.get('user_id')
    amount = data.get('amount')
    date = data.get('date')

    if not all([user_id, amount, date]):
        return jsonify({'error': 'All fields are required'}), 400

    new_payment = Payment(user_id=user_id, amount=amount, date=date)
    db.session.add(new_payment)
    db.session.commit()
    return jsonify(new_payment.to_dict()), 201

@financial_bp.route('/invoices', methods=['GET'])
def get_invoices():
    """Retrieve all invoices for a specific user."""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': 'User ID must be provided'}), 400

    invoices = Invoice.query.filter_by(user_id=user_id).all()
    return jsonify([i.to_dict() for i in invoices])

@financial_bp.route('/invoices', methods=['POST'])
def create_invoice():
    """Create a new invoice."""
    data = request.json
    user_id = data.get('user_id')
    amount = data.get('amount')
    due_date = data.get('due_date')

    if not all([user_id, amount, due_date]):
        return jsonify({'error': 'All fields are required'}), 400

    new_invoice = Invoice(user_id=user_id, amount=amount, due_date=due_date)
    db.session.add(new_invoice)
    db.session.commit()
    return jsonify(new_invoice.to_dict()), 201

@financial_bp.route('/financial-reports', methods=['GET'])
def get_financial_reports():
    """Retrieve financial reports."""
    reports = FinancialReport.query.all()
    return jsonify([r.to_dict() for r in reports])
