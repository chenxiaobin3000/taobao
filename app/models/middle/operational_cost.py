from decimal import Decimal

from django.db import models
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from django.forms.models import model_to_dict
from django.utils import timezone

from app.models.system.user import User


class OperationalCostManager(models.Manager):
    def getCompanyUserIds(self, user_id):
        user = User.objects.filter(id=user_id).first()
        if not user:
            return []
        return list(
            User.objects.filter(company_id=user.company_id).values_list('id', flat=True)
        )

    def isCompanyUser(self, user_ids, user_id):
        return user_id in user_ids

    def add(self, create_date, user_id, project_name, amount, cost_note):
        return self.create(
            create_date=create_date,
            user_id=user_id,
            project_name=project_name,
            amount=amount,
            cost_note=cost_note
        )

    def addList(self, costs):
        return self.bulk_create(costs)

    def addDataList(self, user_ids, datas):
        costs = []
        for data in datas:
            user_id = int(data.get('uid'))
            if not self.isCompanyUser(user_ids, user_id):
                raise ValueError('负责人不属于当前公司')
            create_date = data.get('cdate')
            project_name = data.get('name')
            amount = data.get('amount')
            if self.exists(user_ids, create_date, project_name, amount):
                continue
            costs.append(self.model(
                create_date=create_date,
                user_id=user_id,
                project_name=project_name,
                amount=amount,
                cost_note=data.get('note') or ''
            ))
        if costs:
            self.addList(costs)
        return len(costs)

    def exists(self, user_ids, create_date, project_name, amount):
        return self.filter(
            user_id__in=user_ids,
            create_date=create_date,
            project_name=project_name,
            amount=Decimal(str(amount))
        ).exists()

    def set(self, pk, create_date, user_id, project_name, amount, cost_note):
        cost = self.get(pk=pk)
        cost.create_date = create_date
        cost.user_id = user_id
        cost.project_name = project_name
        cost.amount = amount
        cost.cost_note = cost_note
        return cost.save()

    def delete(self, pk):
        return self.get(pk=pk).delete()

    def existsByCompany(self, pk, user_ids):
        return self.filter(id=pk, user_id__in=user_ids).exists()

    def deleteByCompany(self, pk, user_ids):
        cost = self.filter(id=pk, user_id__in=user_ids).first()
        if not cost:
            return False
        cost.delete()
        return True

    def total(self, user_ids):
        return self.filter(user_id__in=user_ids).count()

    def getList(self, user_ids, page, num):
        left = (page - 1) * num
        right = page * num
        return self.encoderList(
            self.filter(user_id__in=user_ids).order_by('-create_date', '-id')[left:right]
        )

    def groupByMonth(self, user_id, start_date, end_date):
        user_ids = self.getCompanyUserIds(user_id)
        costs = self.filter(
            user_id__in=user_ids,
            create_date__gte=start_date,
            create_date__lte=end_date
        ).annotate(
            create_month=TruncMonth('create_date')
        ).values('create_month').annotate(
            amount=Sum('amount')
        ).order_by('create_month')
        month_data = {}
        total = Decimal('0')
        for cost in costs:
            month_data[cost['create_month'].strftime('%Y-%m')] = round(cost['amount'], 1)
            total += cost['amount']
        return month_data, round(total, 1)

    def encoderList(self, costs):
        if costs:
            return [
                model_to_dict(
                    cost,
                    fields=[
                        'id',
                        'create_date',
                        'user_id',
                        'project_name',
                        'amount',
                        'cost_note'
                    ]
                )
                for cost in costs
            ]
        return None


class OperationalCost(models.Model):
    objects = OperationalCostManager()
    create_date = models.DateField(db_index=True)
    user_id = models.IntegerField(db_index=True)
    project_name = models.CharField(max_length=32, db_index=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    cost_note = models.CharField(max_length=32)
    ctime = models.DateTimeField(default=timezone.now)

    class Meta(object):
        db_table = 't_operational_cost'
