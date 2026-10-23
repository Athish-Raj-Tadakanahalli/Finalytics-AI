from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Budget, Category, Transaction
from sqlalchemy import func

budgets_bp = Blueprint('budgets', __name__)

@budgets_bp.route('/budgets', methods=['GET', 'POST'])
@login_required
def manage_budgets():
    if request.method == 'POST':
        try:
            category_id = int(request.form.get('category'))
            limit_amount = float(request.form.get('limit_amount'))
            
            category = db.session.get(Category, category_id)
            if category and category.user_id == current_user.id:
                budget = Budget.query.filter_by(user_id=current_user.id, category_id=category_id).first()
                if budget:
                    budget.limit_amount = limit_amount
                    flash(f'Budget for {category.name} updated to ${limit_amount:,.2f}.', 'success')
                else:
                    new_budget = Budget(user_id=current_user.id, category_id=category_id, limit_amount=limit_amount)
                    db.session.add(new_budget)
                    flash(f'Budget for {category.name} set to ${limit_amount:,.2f}.', 'success')
                db.session.commit()
            else:
                flash('Invalid category selected.', 'danger')
        except Exception as e:
            flash(f'Error updating budget: {str(e)}', 'danger')
            
        return redirect(url_for('budgets.manage_budgets'))
        
    budgets = Budget.query.filter_by(user_id=current_user.id).all()
    categories = Category.query.filter_by(user_id=current_user.id, type='expense').all()
    
    # Calculate spending for each budget
    budget_items = []
    for b in budgets:
        spent = db.session.query(func.sum(Transaction.amount)).filter_by(
            user_id=current_user.id, category_id=b.category_id, type='expense'
        ).scalar() or 0.0
        pct = (spent / b.limit_amount * 100) if b.limit_amount > 0 else 0
        budget_items.append({
            'id': b.id,
            'category_id': b.category_id,
            'category_name': b.category.name,
            'limit_amount': b.limit_amount,
            'spent': spent,
            'remaining': max(0.0, b.limit_amount - spent),
            'percent': min(100, round(pct, 1)),
            'raw_percent': round(pct, 1)
        })
        
    return render_template('budgets.html', budgets=budget_items, categories=categories)

@budgets_bp.route('/budgets/delete/<int:budget_id>', methods=['POST'])
@login_required
def delete_budget(budget_id):
    budget = db.session.get(Budget, budget_id)
    if budget and budget.user_id == current_user.id:
        cat_name = budget.category.name
        db.session.delete(budget)
        db.session.commit()
        flash(f'Budget for {cat_name} removed.', 'success')
    return redirect(url_for('budgets.manage_budgets'))

