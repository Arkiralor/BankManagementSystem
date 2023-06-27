from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from job_handlers.utils import enqueue_job

from experiments_app import logger


def find_prime_numbers(lower_bound: int, upper_bound: int) -> None:
    prime_numbers = []
    for number in range(lower_bound, upper_bound + 1):
        if number > 1:
            for i in range(2, number//2):
                if (number % i) == 0:
                    break
            else:
                print(number)
                prime_numbers.append(number)


class TestEnqueue(APIView):
    permission_classes = (AllowAny,)

    def get(self, request: Request) -> Response:
        """
        Test endpoint to enqueue a job.
        """
        lower_bound = int(request.query_params.get('lower', 1))
        upper_bound = int(request.query_params.get('upper', 100))
        job = enqueue_job(
            func=find_prime_numbers,
            job_q='default',
            lower_bound=lower_bound, 
            upper_bound=upper_bound
        )
        logger.info(
            f"Enqueued job {job.id} to find prime numbers between {lower_bound} and {upper_bound}")
        logger.info(f"{job.__dict__}")
        return Response({'job': job.id}, status=status.HTTP_200_OK)
