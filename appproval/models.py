from django.db import models
from .leave_request import LeaveRequest

# CORRECT (if employee is in the same models.py file)
from employee.models import Employee
# OR just use Employee directly if it's defined in the same file

class Approval(models.Model):
    approved_by = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="approvals")
    approved_at = models.DateTimeField(auto_now_add=True)
    decision = models.CharField(max_length=20, choices=(('approved', 'Approved'), ('rejected', 'Rejected')))

    def __str__(self):
        return f"{self.leave_request} - {self.decision}"
