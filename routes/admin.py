from flask import Blueprint, render_template, session, jsonify, request, flash, redirect, url_for
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Helper function to check if user is admin
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('auth.login'))
        
        if session.get('user_role') != 'admin':
            flash('Admin access required.', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    # Sample data for dashboard
    stats = {
        'total_reports': 9,
        'pending': 5,
        'investigating': 2,
        'resolved': 1
    }
    
    # Sample incidents data for the table
    recent_incidents = [
        {
            'id': 'IR-2024-001',
            'title': 'Phishing Email Campaign',
            'reporter': 'john.doe@company.com',
            'severity': 'High',
            'status': 'Pending',
            'date': '2024-07-19 14:30',
            'type': 'phishing'
        },
        {
            'id': 'IR-2024-002', 
            'title': 'Malware Infection on Workstation',
            'reporter': 'jane.smith@company.com',
            'severity': 'Critical',
            'status': 'Investigating',
            'date': '2024-07-19 12:15',
            'type': 'malware'
        },
        {
            'id': 'IR-2024-003',
            'title': 'Unauthorized Access Attempt',
            'reporter': 'mike.johnson@company.com', 
            'severity': 'Medium',
            'status': 'Investigating',
            'date': '2024-07-19 10:45',
            'type': 'unauthorized_access'
        },
        {
            'id': 'IR-2024-004',
            'title': 'Suspicious Network Traffic',
            'reporter': 'sarah.wilson@company.com',
            'severity': 'Low', 
            'status': 'Resolved',
            'date': '2024-07-18 16:20',
            'type': 'network'
        },
        {
            'id': 'IR-2024-005',
            'title': 'Data Breach Attempt',
            'reporter': 'alex.brown@company.com',
            'severity': 'High',
            'status': 'Pending',
            'date': '2024-07-18 14:10',
            'type': 'data_breach'
        },
        {
            'id': 'IR-2024-006',
            'title': 'Social Engineering Attack',
            'reporter': 'lisa.davis@company.com',
            'severity': 'Medium',
            'status': 'Pending', 
            'date': '2024-07-18 11:30',
            'type': 'social_engineering'
        }
    ]
    
    return render_template('admin/admin.html', stats=stats, recent_incidents=recent_incidents)

@admin_bp.route('/incidents')
@admin_bp.route('/manage-incidents')
@admin_required
def manage_incidents():
    # Sample incidents data with more detailed information
    incidents = [
        {
            'id': 'IR-2024-001',
            'title': 'Phishing Email Campaign Detected',
            'reporter': 'john.doe@company.com',
            'type': 'Phishing',
            'severity': 'High',
            'status': 'Pending',
            'date': '2024-07-19 14:30',
            'description': 'Multiple users received suspicious emails claiming to be from IT support requesting password reset.',
            'assigned_to': None,
            'created_by': 'system',
            'last_updated': '2024-07-19 14:30'
        },
        {
            'id': 'IR-2024-002', 
            'title': 'Malware Infection on Workstation',
            'reporter': 'jane.smith@company.com',
            'type': 'Malware',
            'severity': 'Critical',
            'status': 'Investigating',
            'date': '2024-07-19 12:15',
            'description': 'Workstation showing signs of malware infection with unusual network activity.',
            'assigned_to': 'analyst1',
            'created_by': 'jane.smith',
            'last_updated': '2024-07-19 13:45'
        },
        {
            'id': 'IR-2024-003',
            'title': 'Unauthorized Access Attempt',
            'reporter': 'mike.johnson@company.com', 
            'type': 'Unauthorized Access',
            'severity': 'Medium',
            'status': 'Investigating',
            'date': '2024-07-19 10:45',
            'description': 'Failed login attempts detected from unusual geographic location.',
            'assigned_to': 'analyst2',
            'created_by': 'security_system',
            'last_updated': '2024-07-19 11:20'
        },
        {
            'id': 'IR-2024-004',
            'title': 'Suspicious Network Traffic',
            'reporter': 'sarah.wilson@company.com',
            'type': 'Network', 
            'severity': 'Low',
            'status': 'Resolved',
            'date': '2024-07-18 16:20',
            'description': 'Unusual outbound network traffic patterns detected during off-hours.',
            'assigned_to': 'analyst1',
            'created_by': 'network_monitor',
            'last_updated': '2024-07-19 09:15'
        },
        {
            'id': 'IR-2024-005',
            'title': 'Data Breach Attempt',
            'reporter': 'alex.brown@company.com',
            'type': 'Data Breach',
            'severity': 'High',
            'status': 'Pending',
            'date': '2024-07-18 14:10',
            'description': 'Attempted unauthorized access to customer database detected.',
            'assigned_to': None,
            'created_by': 'db_monitor',
            'last_updated': '2024-07-18 14:10'
        },
        {
            'id': 'IR-2024-006',
            'title': 'Social Engineering Attack',
            'reporter': 'lisa.davis@company.com',
            'type': 'Social Engineering',
            'severity': 'Medium',
            'status': 'Pending', 
            'date': '2024-07-18 11:30',
            'description': 'Employee reported receiving phone call from someone impersonating IT support.',
            'assigned_to': None,
            'created_by': 'lisa.davis',
            'last_updated': '2024-07-18 11:30'
        },
        {
            'id': 'IR-2024-007',
            'title': 'Ransomware Detection',
            'reporter': 'security.team@company.com',
            'type': 'Malware',
            'severity': 'Critical',
            'status': 'Investigating',
            'date': '2024-07-17 22:45',
            'description': 'Potential ransomware activity detected on file server.',
            'assigned_to': 'incident_response_team',
            'created_by': 'edr_system',
            'last_updated': '2024-07-18 08:30'
        },
        {
            'id': 'IR-2024-008',
            'title': 'USB Device Policy Violation',
            'reporter': 'hr@company.com',
            'type': 'Unauthorized Access',
            'severity': 'Low',
            'status': 'Resolved',
            'date': '2024-07-17 15:20',
            'description': 'Employee connected unauthorized USB device to company workstation.',
            'assigned_to': 'compliance_team',
            'created_by': 'usb_monitor',
            'last_updated': '2024-07-17 16:45'
        }
    ]
    
    return render_template('admin/manage_incidents.html', incidents=incidents)

@admin_bp.route('/reports')
@admin_required
def reports():
    return render_template('admin/reports.html')

@admin_bp.route('/users')
@admin_required 
def users():
    # Sample users data
    users = [
        {
            'id': 1, 
            'name': 'John Doe', 
            'email': 'john.doe@company.com', 
            'role': 'user', 
            'status': 'active',
            'last_login': '2024-07-19 14:30',
            'reports_count': 5
        },
        {
            'id': 2, 
            'name': 'Jane Smith', 
            'email': 'jane.smith@company.com', 
            'role': 'user', 
            'status': 'active',
            'last_login': '2024-07-19 12:15', 
            'reports_count': 3
        },
        {
            'id': 3, 
            'name': 'Admin User', 
            'email': 'admin@gmail.com', 
            'role': 'admin', 
            'status': 'active',
            'last_login': '2024-07-19 15:00',
            'reports_count': 0
        },
        {
            'id': 4,
            'name': 'Mike Johnson', 
            'email': 'mike.johnson@company.com', 
            'role': 'user', 
            'status': 'inactive',
            'last_login': '2024-07-15 09:20',
            'reports_count': 2
        }
    ]
    return render_template('admin/users.html', users=users)

@admin_bp.route('/incidents')
@admin_required
def incidents():
    return render_template('admin/incidents.html')

@admin_bp.route('/analytics')
@admin_required
def analytics():
    return render_template('admin/analytics.html')

@admin_bp.route('/settings')
@admin_required
def settings():
    return render_template('admin/settings.html')

@admin_bp.route('/api/chart-data')
@admin_required
def get_chart_data():
    # Sample data for charts - matching your dashboard design
    chart_data = {
        'monthly_reports': {
            'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
            'data': [0, 0, 0, 0, 0, 2, 7, 0, 0, 0, 0, 0]  # Jun: 2, Jul: 7 to match your chart
        },
        'incident_categories': {
            'labels': ['Malware', 'Phishing', 'Unauthorized Access', 'Data Breach', 'Social Engineering'],
            'data': [40, 30, 15, 10, 5],  # Percentages matching your pie chart colors
            'colors': ['#10B981', '#06B6D4', '#F59E0B', '#EF4444', '#8B5CF6']
        }
    }
    return jsonify(chart_data)
