from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmployeeListView,
    EmployeeDetailView,
    ApplyLeaveView,
    LeaveHistoryView,
    UploadLeaveDocumentView,
    LeaveBalanceView,
    ApproveLeaveView,
    RejectLeaveView,
    PendingApprovalView,
    LeaveTypeListView,
    ManageLeaveTypeView,
    PublicHolidayListView,
    AdjustLeaveBalanceView,
    RunMonthlyAccrualView,
    YearEndCarryoverView,
    LeaveReportsView, 
    TeamOnLeaveView,
    FilterByDepartmentView,
GoogleSyncView
)

router = DefaultRouter()

urlpatterns = [
    # Employee Management
    path('employees/', EmployeeListView.as_view(), name='employee-list'),
    path('employees/<int:id>/', EmployeeDetailView.as_view(), name='employee-detail'),

    # Leave Requests
    path('leaves/apply/', ApplyLeaveView.as_view(), name='apply-leave'),
    path('leaves/history/<int:employee_id>/', LeaveHistoryView.as_view(), name='leave-history'),
    path('leaves/upload-document/', UploadLeaveDocumentView.as_view(), name='upload-leave-document'),

    # Leave Balance
    path('leave-balance/<int:employee_id>/', LeaveBalanceView.as_view(), name='leave-balance'),

    # Approvals
    path('leave/approve/<int:leave_id>/', ApproveLeaveView.as_view(), name='approve-leave'),
    path('leave/reject/<int:leave_id>/', RejectLeaveView.as_view(), name='reject-leave'),
    path('leave/pending-approvals/', PendingApprovalView.as_view(), name='pending-approvals'),

    # Leave Types
    path('leave-types/', LeaveTypeListView.as_view(), name='leave-type-list'),
    path('admin/manage-leave-types/', LeaveReportsView.as_view(), name='manage-leave-types'),

    # Public Holidays
    path('public-holidays/', PublicHolidayListView.as_view(), name='public-holiday-list'),

    # Admin actions
    path('admin/adjust-leave-balance/<int:employee_id>/', AdjustLeaveBalanceView.as_view(), name='adjust-leave-balance'),
    path('admin/run-monthly-accrual/', RunMonthlyAccrualView.as_view(), name='run-monthly-accrual'),
    path('admin/year-end-carryover/', YearEndCarryoverView.as_view(), name='year-end-carryover'),
    path('admin/export-leave-data/', LeaveReportsView.as_view(), name='export-leave-data'),

    # Team and Calendar
    path('team/on-leave/', TeamOnLeaveView.as_view(), name='team-on-leave'),
    path('team/filter-by-department/', FilterByDepartmentView.as_view(), name='filter-by-department'),
    path('team/google-sync/',GoogleSyncView.as_view(), name='google-calendar-sync'),

    # Include Router if needed
    path('', include(router.urls)),
]
