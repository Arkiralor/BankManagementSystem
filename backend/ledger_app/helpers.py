from datetime import datetime, date, timedelta
from typing import List, Dict, Union, Optional

from django.conf import settings
from django.db.models import Q, QuerySet, Count
from django.utils import timezone

from rest_framework import status

from core.boilerplate.response_template import Resp
from ledger_app.models import EmployeeLedger
from ledger_app.serializers import EmployeeLedgerInputSerializer, EmployeeLedgerOutputSerializer
from user_app.models import User

from ledger_app import logger

class EmployeeLedgerAPIHelper:

    ALLOWED_FIELDS = ("title", "body")

    @classmethod
    def str_to_date(cls, date_str:str=None) -> date:
        if not date_str:
            return timezone.now().date()
        
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except Exception as ex:
            logger.warn(f"{ex}")
            return timezone.now().date()

    @classmethod
    def get(cls, _id:str=None) -> EmployeeLedger:
        ledger = EmployeeLedger.objects.filter(pk=_id).first()
        if not ledger:
            raise ValueError("Invalid Ledger ID")
        
        return ledger
    
    @classmethod
    def retrieve(cls, _id:str=None, user_id: str = None, from_date:str = None, to_date:str=None) -> Resp:
        """
        Retrieves the ledger entries for the given user.

        If `_id` is provided, then `from_date` and `to_date` are ignored.

        """
        resp = Resp()

        user = User.objects.filter(pk=user_id).first()

        if _id:
            ledger = cls.get(_id=_id)
            if not ledger:
                resp.error = "Invalid Ledger ID"
                resp.message = "`ID` is a required field"
                resp.status_code = status.HTTP_400_BAD_REQUEST

                logger.warn(resp.message)
                return resp
            
            if ledger.employee != user and not (user.is_staff or user.is_superuser):
                resp.error = "Unauthorized"
                resp.message = "You are not authorized to perform this action"
                resp.status_code = status.HTTP_401_UNAUTHORIZED

                logger.warn(resp.message)
                return resp

            resp.message = "Ledger entry retrieved successfully"
            resp.data = EmployeeLedgerOutputSerializer(ledger).data
            resp.status_code = status.HTTP_200_OK

            logger.info(resp.message)
            return resp
        
        if from_date:
            from_date = cls.str_to_date(from_date)
        else:
            from_date = timezone.now().date() - timedelta(days=7)
        
        if to_date:
            to_date = cls.str_to_date(to_date)
        else:
            to_date = timezone.now().date()
        
        ledger = EmployeeLedger.objects.filter(
            Q(employee__id=user_id)
            & Q(
                Q(created__date__gte=from_date)
                & Q(created__date__lte=to_date)
            )
        ).annotate(count=Count('created')).order_by('-created')

        resp.message = "Ledger entries retrieved successfully"
        resp.data = EmployeeLedgerOutputSerializer(ledger, many=True).data
        resp.status_code = status.HTTP_200_OK

        logger.info(resp.message)
        return resp


    @classmethod
    def create(cls, data:dict=None, user: User=None) -> Resp:
        resp = Resp()

        if not user or not type(user) == User:
            resp.error = "Invalid User"
            resp.message = "`USER` is a required field"
            resp.status_code = status.HTTP_400_BAD_REQUEST

            logger.warn(resp.message)
            return resp

        if not data:
            resp.error = "Invalid Data"
            resp.message = "`DATA` is a required field"
            resp.status_code = status.HTTP_400_BAD_REQUEST

            logger.warn(resp.message)
            return resp
        
        data['employee'] = f"{user.id}"

        deserialized = EmployeeLedgerInputSerializer(data=data)
        if not deserialized.is_valid():
            resp.error = "Invalid Data"
            resp.message = f"{deserialized.errors}"
            resp.data = data
            resp.status_code = status.HTTP_400_BAD_REQUEST

            logger.warn(resp.message)
            return resp
        
        deserialized.save()

        resp.message = "Ledger entry created successfully"
        resp.data = EmployeeLedgerOutputSerializer(deserialized.instance).data
        resp.status_code = status.HTTP_201_CREATED

        logger.info(resp.message)
        return resp
    
    @classmethod
    def update(cls, _id:str=None, data:dict=None, user: User=None) -> Resp:
        resp = Resp()

        if not user or not type(user) == User:
            resp.error = "Invalid User"
            resp.message = "`USER` is a required field"
            resp.status_code = status.HTTP_400_BAD_REQUEST

            logger.warn(resp.message)
            return resp
        
        if not _id:
            resp.error = "Invalid Ledger ID"
            resp.message = "`ID` is a required field"
            resp.status_code = status.HTTP_400_BAD_REQUEST

            logger.warn(resp.message)
            return resp
        
        if not type(data) == dict:
            resp.error = "Invalid Data"
            resp.message = "`DATA` is a required field"
            resp.status_code = status.HTTP_400_BAD_REQUEST

            logger.warn(resp.message)
            return resp
        
        ledger = cls.get(_id=_id)
        if not ledger.employee == user and not (user.is_staff or user.is_superuser):
            resp.error = "Unauthorized"
            resp.message = "You are not authorized to perform this action"
            resp.status_code = status.HTTP_401_UNAUTHORIZED

            logger.warn(resp.message)
            return resp
        
        ledger_data = EmployeeLedgerInputSerializer(ledger).data
        
        _keys = data.keys()
        for key in _keys:
            if key not in cls.ALLOWED_FIELDS:
                resp.error = "Invalid Data"
                resp.message = f"`{key}` is not a valid field"
                resp.status_code = status.HTTP_400_BAD_REQUEST

                logger.warn(resp.message)
                return resp
            
            ledger_data[key] = data[key]

        deserialized = EmployeeLedgerInputSerializer(ledger, data=ledger_data)
        if not deserialized.is_valid():
            resp.error = "Invalid Data"
            resp.message = f"{deserialized.errors}"
            resp.data = data
            resp.status_code = status.HTTP_400_BAD_REQUEST

            logger.warn(resp.message)
            return resp
        
        deserialized.save()

        resp.message = "Ledger entry updated successfully"
        resp.data = EmployeeLedgerOutputSerializer(deserialized.instance).data
        resp.status_code = status.HTTP_200_OK

        logger.info(resp.message)
        return resp
            
