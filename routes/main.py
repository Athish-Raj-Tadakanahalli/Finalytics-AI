from flask import Blueprint, render_template
from flask_login import login_required, current_user
from datetime import datetime, timedelta

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/dashboard')
@login_required
def dashboard():
    from models import db, Transaction, Category, Budget
    from sqlalchemy import func
    
    # Calculate Totals
    income = db.session.query(func.sum(Transaction.amount)).filter_by(user_id=current_user.id, type='income').scalar() or 0.0
    expense = db.session.query(func.sum(Transaction.amount)).filter_by(user_id=current_user.id, type='expense').scalar() or 0.0
    balance = income - expense
    
    # Savings Rate
    savings_rate = 0.0
    if income > 0:
        savings_rate = max(0.0, round(((income - expense) / income) * 100, 1))
        
    # Pie Chart Data: Expenses by Category
    expenses_by_cat = db.session.query(Category.name, func.sum(Transaction.amount))\
        .join(Transaction, Category.id == Transaction.category_id)\
        .filter(Transaction.user_id == current_user.id, Transaction.type == 'expense')\
        .group_by(Category.name).all()
        
    pie_labels = [row[0] for row in expenses_by_cat]
    pie_data = [float(row[1]) for row in expenses_by_cat]
    
    # Budgets Progress
    budgets = Budget.query.filter_by(user_id=current_user.id).all()
    budget_progress = []
    budget_exceeded_count = 0
    for b in budgets:
        spent = db.session.query(func.sum(Transaction.amount)).filter_by(
            user_id=current_user.id, category_id=b.category_id, type='expense'
        ).scalar() or 0.0
        pct = (spent / b.limit_amount * 100) if b.limit_amount > 0 else 0
        if pct >= 100:
            budget_exceeded_count += 1
        budget_progress.append({
            'category': b.category.name,
            'limit': float(b.limit_amount),
            'spent': float(spent),
            'percent': min(100, round(pct, 1)),
            'raw_percent': round(pct, 1)
        })
        
    # Financial Health Score (0 - 100)
    # Starts at 50; savings rate adds up to 30; budget adherence adds up to 20; deductions for overspending
    health_score = 50
    if income > 0:
        if savings_rate >= 20:
            health_score += 25
        elif savings_rate > 10:
            health_score += 15
        elif savings_rate > 0:
            health_score += 5
        else:
            health_score -= 20
    if budgets:
        if budget_exceeded_count == 0:
            health_score += 25
        else:
            health_score = max(10, health_score - (budget_exceeded_count * 12))
    else:
        health_score += 10
    health_score = max(5, min(100, health_score))
    
    # 6-Month Cashflow Trend Calculation
    today = datetime.utcnow().date()
    month_labels = []
    monthly_incomes = []
    monthly_expenses = []
    
    for i in range(5, -1, -1):
        # Approximate first day of the target month
        # Subtract ~30 days * i
        target_date = today.replace(day=1) - timedelta(days=i * 30)
        target_year = target_date.year
        target_month = target_date.month
        month_name = target_date.strftime('%b')
        month_labels.append(month_name)
        
        # Calculate sum for this month
        all_txs = Transaction.query.filter_by(user_id=current_user.id).all()
        m_inc = sum(t.amount for t in all_txs if t.type == 'income' and t.date.year == target_year and t.date.month == target_month)
        m_exp = sum(t.amount for t in all_txs if t.type == 'expense' and t.date.year == target_year and t.date.month == target_month)
        monthly_incomes.append(float(m_inc))
        monthly_expenses.append(float(m_exp))
        
    # Categorized AI Rule-based Insights
    insights = []
    if expense > income and income > 0:
        insights.append({
            'badge': 'Budget Alert',
            'type': 'danger',
            'icon': 'bi-exclamation-triangle-fill',
            'message': f'Expenses exceed income by ${(expense - income):,.2f}. Urgent deficit review recommended.'
        })
    elif expense > income * 0.8 and income > 0:
        insights.append({
            'badge': 'High Burn Rate',
            'type': 'warning',
            'icon': 'bi-lightning-charge-fill',
            'message': 'Your expenses consume over 80% of your earnings. Target a 20% savings buffer.'
        })
        
    if budget_exceeded_count > 0:
        insights.append({
            'badge': 'Budget Exceeded',
            'type': 'danger',
            'icon': 'bi-pie-chart-fill',
            'message': f'{budget_exceeded_count} category budget(s) have passed their spending ceiling.'
        })
        
    if pie_data and expense > 0 and max(pie_data) > expense * 0.4:
        max_cat = pie_labels[pie_data.index(max(pie_data))]
        pct_spent = round((max(pie_data) / expense) * 100)
        insights.append({
            'badge': 'Spending Concentration',
            'type': 'info',
            'icon': 'bi-bullseye',
            'message': f"'{max_cat}' represents {pct_spent}% of all expenditures this cycle."
        })
        
    if savings_rate >= 20:
        insights.append({
            'badge': 'Strong Savings',
            'type': 'success',
            'icon': 'bi-trophy-fill',
            'message': f'Healthy savings rate of {savings_rate}%. You are exceeding the standard 50/30/20 benchmark.'
        })
        
    if not insights:
        insights.append({
            'badge': 'Optimal Health',
            'type': 'success',
            'icon': 'bi-check-circle-fill',
            'message': 'Your spending habits appear balanced and stable. Keep maintaining consistent tracking!'
        })

    # Recent Transactions (Last 5)
    recent_transactions = Transaction.query.filter_by(user_id=current_user.id)\
        .order_by(Transaction.date.desc(), Transaction.id.desc()).limit(5).all()
        
    return render_template('dashboard.html', 
                           income=income, expense=expense, balance=balance,
                           savings_rate=savings_rate, health_score=health_score,
                           pie_labels=pie_labels, pie_data=pie_data,
                           trend_labels=month_labels, trend_incomes=monthly_incomes, trend_expenses=monthly_expenses,
                           budget_progress=budget_progress,
                           insights=insights,
                           recent_transactions=recent_transactions)

