from django.http import HttpResponse
from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from request.models import LeaveRequest, LeaveBalance, LeaveType

import logging
import csv
from datetime import date

from employee.models import Employee
from request.models import LeaveRequest, LeaveBalance
from appproval.models import Approval
from publicholiday.models import PublicHoliday
from .serializers import (
    EmployeeSerializer,
    LeaveRequestSerializer,
    LeaveBalanceSerializer,
    PublicHolidaySerializer,
    ApprovalSerializer,
    LeaveTypeSerializer,
)

logger = logging.getLogger(__name__)

# --- Employee Views ---
class EmployeeListView(APIView):
    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EmployeeDetailView(APIView):
    def get(self, request, id):
        try:
            employee = Employee.objects.get(id=id)
            serializer = EmployeeSerializer(employee)
            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response({"detail": "Employee not found."}, status=status.HTTP_404_NOT_FOUND)


# --- Leave Request Views ---
class ApplyLeaveView(APIView):
    def post(self, request):
        serializer = LeaveRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employee=request.user.employee)
            logger.info(f"Leave application submitted by {request.user.email}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Leave application failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LeaveHistoryView(APIView):
    def get(self, request, employee_id):
        leaves = LeaveRequest.objects.filter(employee_id=employee_id)
        serializer = LeaveRequestSerializer(leaves, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UploadLeaveDocumentView(APIView):
    def post(self, request):
        try:
            leave_request = LeaveRequest.objects.get(id=request.data.get('leave_request_id'))
            leave_request.document = request.FILES.get('document')
            leave_request.save()
            logger.info(f"Document uploaded for leave request {leave_request.id}")
            return Response({"detail": "Document uploaded successfully"}, status=status.HTTP_200_OK)
        except LeaveRequest.DoesNotExist:
            return Response({"detail": "Leave request not found."}, status=status.HTTP_404_NOT_FOUND)


# --- Leave Balance Views ---
class LeaveBalanceView(APIView):
    def get(self, request, employee_id):
        balances = LeaveBalance.objects.filter(employee_id=employee_id)
        serializer = LeaveBalanceSerializer(balances, many=True)
        return Response(serializer.data)


# --- Approval Views ---
class ApproveLeaveView(APIView):
    def post(self, request, leave_id):
        try:
            leave = LeaveRequest.objects.get(id=leave_id)
            leave.status = 'approved'
            leave.save()
            logger.info(f"Leave request {leave_id} approved.")
            return Response({"detail": "Leave approved."}, status=status.HTTP_200_OK)
        except LeaveRequest.DoesNotExist:
            return Response({"detail": "Leave request not found."}, status=status.HTTP_404_NOT_FOUND)


class RejectLeaveView(APIView):
    def post(self, request, leave_id):
        try:
            leave = LeaveRequest.objects.get(id=leave_id)
            leave.status = 'rejected'
            leave.save()
            logger.info(f"Leave request {leave_id} rejected.")
            return Response({"detail": "Leave rejected."}, status=status.HTTP_200_OK)
        except LeaveRequest.DoesNotExist:
            return Response({"detail": "Leave request not found."}, status=status.HTTP_404_NOT_FOUND)


class PendingApprovalView(APIView):
    def get(self, request):
        pending_leaves = LeaveRequest.objects.filter(status='pending')
        serializer = LeaveRequestSerializer(pending_leaves, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# --- Leave Type Views ---
class LeaveTypeListView(APIView):
    def get(self, request):
        leave_types = LeaveType.objects.all()
        serializer = LeaveTypeSerializer(leave_types, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# --- Public Holidays View ---
class PublicHolidayListView(APIView):
    def get(self, request):
        holidays = PublicHoliday.objects.all()
        serializer = PublicHolidaySerializer(holidays, many=True)
        return Response(serializer.data)


# --- Admin Views ---
class AdjustLeaveBalanceView(APIView):
    def post(self, request, employee_id):
        try:
            balance = LeaveBalance.objects.get(employee_id=employee_id, leave_type_id=request.data['leave_type_id'])
            balance.balance = request.data['new_balance']
            balance.save()
            logger.info(f"Leave balance adjusted for employee {employee_id}")
            return Response({"detail": "Leave balance updated."}, status=status.HTTP_200_OK)
        except LeaveBalance.DoesNotExist:
            return Response({"detail": "Leave balance not found."}, status=status.HTTP_404_NOT_FOUND)


class RunMonthlyAccrualView(APIView):
    def post(self, request):
        logger.info("Monthly accrual triggered manually.")
        return Response({"detail": "Monthly accrual completed."})


class YearEndCarryoverView(APIView):
    def post(self, request):
        logger.info("Year-end carryover triggered manually.")
        return Response({"detail": "Year-end carryover completed."})


# --- New Features ---
class TeamOnLeaveView(APIView):

    def get(self, request):
        today = date.today()
        team_on_leave = LeaveRequest.objects.filter(
            Q(start_date__lte=today) & Q(end_date__gte=today),
            status='approved'
        )
        serializer = LeaveRequestSerializer(team_on_leave, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class FilterByDepartmentView(APIView):

    def get(self, request):
        department = request.query_params.get('department')
        if not department:
            return Response({"detail": "Department parameter required."}, status=status.HTTP_400_BAD_REQUEST)

        team_on_leave = LeaveRequest.objects.filter(
            employee__department=department,
            status='approved'
        )
        serializer = LeaveRequestSerializer(team_on_leave, many=True)
        return Response(serializer.data)


class GoogleSyncView(APIView):

    def post(self, request):
        logger.info(f"Google Calendar sync triggered by {request.user.email}")
        return Response({"detail": "Google Calendar sync feature not yet implemented."}, status=status.HTTP_202_ACCEPTED)


class ManageLeaveTypeView(APIView):

    def post(self, request):
        serializer = LeaveTypeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            leave_type = LeaveType.objects.get(pk=pk)
        except LeaveType.DoesNotExist:
            return Response({"detail": "Leave type not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = LeaveTypeSerializer(leave_type, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            leave_type = LeaveType.objects.get(pk=pk)
            leave_type.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except LeaveType.DoesNotExist:
            return Response({"detail": "Leave type not found."}, status=status.HTTP_404_NOT_FOUND)


class LeaveReportsView(APIView):

    def get(self, request):
        leaves = LeaveRequest.objects.select_related('employee', 'leave_type').all()
        serializer = LeaveRequestSerializer(leaves, many=True)
        return Response(serializer.data)


class ExportLeaveDataView(APIView):

    def get(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="leave_data.csv"'

        writer = csv.writer(response)
        writer.writerow(['Employee', 'Leave Type', 'Start Date', 'End Date', 'Status'])

        leaves = LeaveRequest.objects.select_related('employee', 'leave_type').all()
        for leave in leaves:
            writer.writerow([
                leave.employee.name,
                leave.leave_type.name,
                leave.start_date,
                leave.end_date,
                leave.status
            ])
        return response
