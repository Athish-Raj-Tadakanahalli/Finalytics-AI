from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Transaction, Category

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/transactions', methods=['GET', 'POST'])
@login_required
def manage_transactions():
    if request.method == 'POST':
        try:
            amount = float(request.form.get('amount'))
            date_str = request.form.get('date')
            category_id = int(request.form.get('category'))
            notes = request.form.get('notes', '').strip()
            
            category = db.session.get(Category, category_id)
            if category and category.user_id == current_user.id:
                from datetime import datetime
                tx_date = datetime.strptime(date_str, '%Y-%m-%d').date()
                
                new_tx = Transaction(
                    user_id=current_user.id,
                    amount=amount,
                    category_id=category.id,
                    date=tx_date,
                    type=category.type,
                    notes=notes
                )
                db.session.add(new_tx)
                db.session.commit()
                flash('Transaction recorded successfully.', 'success')
            else:
                flash('Invalid category selected.', 'danger')
        except Exception as e:
            flash(f'Error saving transaction: {str(e)}', 'danger')
            
        return redirect(url_for('transactions.manage_transactions'))
        
    # Filtering parameters
    search_q = request.args.get('q', '').strip()
    type_filter = request.args.get('type', '').strip()
    cat_filter = request.args.get('category', '').strip()
    
    query = Transaction.query.filter_by(user_id=current_user.id)
    
    if search_q:
        query = query.filter(Transaction.notes.ilike(f'%{search_q}%'))
    if type_filter in ['income', 'expense']:
        query = query.filter(Transaction.type == type_filter)
    if cat_filter and cat_filter.isdigit():
        query = query.filter(Transaction.category_id == int(cat_filter))
        
    transactions = query.order_by(Transaction.date.desc(), Transaction.id.desc()).all()
    categories = Category.query.filter_by(user_id=current_user.id).order_by(Category.name.asc()).all()
    
    # Calculate filtered stats
    total_in = sum(t.amount for t in transactions if t.type == 'income')
    total_out = sum(t.amount for t in transactions if t.type == 'expense')
    
    return render_template('transactions.html', 
                           transactions=transactions, 
                           categories=categories,
                           search_q=search_q,
                           type_filter=type_filter,
                           cat_filter=cat_filter,
                           total_in=total_in,
                           total_out=total_out)


@transactions_bp.route('/transactions/delete/<int:tx_id>', methods=['POST'])
@login_required
def delete_transaction(tx_id):
    tx = db.session.get(Transaction, tx_id)
    if tx and tx.user_id == current_user.id:
        db.session.delete(tx)
        db.session.commit()
        flash('Transaction deleted.', 'success')
    return redirect(url_for('transactions.manage_transactions'))

import pandas as pd
from flask import Response

@transactions_bp.route('/export/csv', methods=['GET'])
@login_required
def export_csv():
    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.date.desc()).all()
    data = []
    for t in transactions:
        data.append({
            'Date': t.date.strftime('%Y-%m-%d'),
            'Category': t.category.name,
            'Type': t.type.capitalize(),
            'Amount': float(t.amount),
            'Notes': t.notes or ''
        })
    df = pd.DataFrame(data)
    csv_data = df.to_csv(index=False)
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=transactions_export.csv"}
    )
