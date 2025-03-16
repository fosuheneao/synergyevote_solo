# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.db.models import Count
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .models import Voter, Election, Candidate, Vote
from .api.serializers import VoterSerializer, ElectionSerializer, CandidateSerializer, VoteSerializer
import jwt
from django.conf import settings

class VoterLoginView(APIView):
    def post(self, request):
        voter_id = request.data.get('voter_id')
        password = request.data.get('password')

        voter = Voter.objects.filter(voter_id=voter_id, password=password).first()
        if not voter:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        token = jwt.encode({"voter_id": voter.voter_id}, settings.SECRET_KEY, algorithm="HS256")
        return Response({"token": token}, status=status.HTTP_200_OK)

class VPassVerifyView(APIView):
    def post(self, request):
        token = request.data.get('token')
        vpass = request.data.get('vpass')

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            voter = Voter.objects.get(voter_id=payload["voter_id"])

            if voter.vpass != vpass:
                return Response({"error": "Invalid VPass"}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({"message": "Access granted"}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({"error": "Token expired"}, status=status.HTTP_401_UNAUTHORIZED)

        except jwt.DecodeError:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)

class ElectionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        elections = Election.objects.filter(active=True)
        serializer = ElectionSerializer(elections, many=True)
        return Response(serializer.data)

class CandidateListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, election_id):
        candidates = Candidate.objects.filter(election_id=election_id)
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data)

class VoteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        voter_id = request.data.get("voter_id")
        candidate_id = request.data.get("candidate_id")
        election_id = request.data.get("election_id")

        if Vote.objects.filter(voter_id=voter_id, election_id=election_id).exists():
            return Response({"error": "You have already voted"}, status=status.HTTP_400_BAD_REQUEST)

        vote = Vote.objects.create(voter_id=voter_id, candidate_id=candidate_id, election_id=election_id)
        return Response({"message": "Vote cast successfully"}, status=status.HTTP_201_CREATED)

def vote_stats_api(request):
    #API to provide live voting statistics"""
    candidates = Candidate.objects.all()
    data = {
        "candidates": [f"{c.firstname} {c.lastname}" for c in candidates],
        "votes": [Vote.objects.filter(candidate=c).count() for c in candidates],
    }
    return JsonResponse(data)