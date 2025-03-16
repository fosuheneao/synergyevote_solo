from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models import Election, Position, Candidate, Vote, Voter, YesNoOption
from .serializers import ElectionSerializer, PositionSerializer, CandidateSerializer, VoteSerializer, VoterSerializer

# 🔹 1️⃣ Voter Authentication (Step 1: Login with Voter ID & Password)
class VoterLoginView(APIView):
    #Authenticate Voter ID & Password"""
    def post(self, request):
        voter_id = request.data.get("voter_id")
        password = request.data.get("password")

        voter = Voter.objects.filter(voter_id=voter_id).first()
        if not voter or not check_password(password, voter.password):
            return Response({"error": "Invalid Voter ID or Password"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"message": "Proceed to enter VPass", "voter_id": voter.voter_id}, status=status.HTTP_200_OK)


# 🔹 2️⃣ VPass Authentication (Step 2)
class VoterSecondAuthView(APIView):
    #Authenticate VPass"""
    def post(self, request):
        voter_id = request.data.get("voter_id")
        vpass = request.data.get("vpass")

        voter = Voter.objects.filter(voter_id=voter_id, vpass=vpass).first()
        if not voter:
            return Response({"error": "Invalid VPass"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response({"message": "Access granted", "voter_id": voter.voter_id}, status=status.HTTP_200_OK)


#Retrieve Elections
class ElectionListView(APIView):
    #Retrieve all elections along with their positions & candidates"""
    def get(self, request):
        elections = Election.objects.all()
        data = ElectionSerializer(elections, many=True).data
        return Response(data, status=status.HTTP_200_OK)


#Vote Submission (Prevent Multiple Voting)
class VoteView(APIView):
    #Voter submits vote (Ensures one-time voting)"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        voter_id = request.data.get("voter_id")
        election_id = request.data.get("election_id")
        votes = request.data.get("votes")  # List of candidate IDs or Yes/No selection

        voter = get_object_or_404(Voter, voter_id=voter_id)
        election = get_object_or_404(Election, id=election_id)

        # Prevent duplicate voting
        if Vote.objects.filter(voter=voter, election=election).exists():
            return Response({"error": "You have already voted in this election"}, status=status.HTTP_400_BAD_REQUEST)

        # Process votes for each position
        for vote_data in votes:
            position_id = vote_data.get("position_id")
            candidate_ids = vote_data.get("candidate_ids", [])
            yes_no_vote = vote_data.get("yes_no_vote", None)

            position = get_object_or_404(Position, id=position_id, election=election)

            # Handle Single & Multiple Candidate Selection
            if position.vote_type in ["single", "multiple"]:
                if len(candidate_ids) > position.max_vote:
                    return Response({"error": f"Maximum {position.max_vote} candidates allowed"}, status=status.HTTP_400_BAD_REQUEST)

                for candidate_id in candidate_ids:
                    candidate = get_object_or_404(Candidate, id=candidate_id, position=position)
                    Vote.objects.create(voter=voter, election=election, position=position, candidate=candidate)

            # Handle Yes/No Voting
            elif position.vote_type == "yes_no":
                yes_no_option = get_object_or_404(YesNoOption, position=position, vote_yn=yes_no_vote)
                Vote.objects.create(voter=voter, election=election, position=position, voteVal=yes_no_option.vote_yn)

        return Response({"message": "Vote successfully cast"}, status=status.HTTP_201_CREATED)


# Election & Position API ViewSets
class ElectionViewSet(viewsets.ModelViewSet):
    queryset = Election.objects.all()
    serializer_class = ElectionSerializer
    permission_classes = [permissions.IsAuthenticated]

class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [permissions.IsAuthenticated]

class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [permissions.IsAuthenticated]
