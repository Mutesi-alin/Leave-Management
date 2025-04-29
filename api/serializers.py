from rest_framework import serializers
from employee.models import Employee
from request.models import LeaveRequest, LeaveBalance, LeaveType
from appproval.models import Approval
from publicholiday.models import PublicHoliday

# --- Employee Serializer ---
class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = [
            'id', 'first_name', 'last_name', 'email', 'role', 
            'department'
        ]
        read_only_fields = ['id']


# --- Leave Request Serializer ---
class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = [
            'id', 'employee', 'leave_type', 'start_date', 'end_date', 
            'reason', 'status', 'document', 'applied_at'
        ]
        read_only_fields = ['id', 'status', 'applied_at']


# --- Leave Balance Serializer ---
class LeaveBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveBalance
        fields = [
            'id', 'employee', 'leave_type', 'balance'
        ]
        read_only_fields = ['id']


# --- Public Holiday Serializer ---
class PublicHolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PublicHoliday
        fields = [
            'id', 'name', 'date'
        ]
        read_only_fields = ['id']


# --- Approval Serializer ---
class ApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Approval
        fields = [
            'id', 'leave_request', 'approver', 'status', 'comment', 'decision_date'
        ]
        read_only_fields = ['id', 'decision_date']


# --- Leave Type Serializer (List and Manage) ---
class LeaveTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveType
        fields = [
            'id', 'name', 'description', 'days_allowed'
        ]
        read_only_fields = ['id']
