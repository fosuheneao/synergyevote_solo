from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from ..models import Election, Position, Candidate, Vote, Voter, YesNoOption

User = get_user_model()

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)


# Voter Serializer
class VoterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voter
        fields = '__all__'


# Yes/No Option Serializer
class YesNoOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = YesNoOption
        fields = ["id", "vote_yn"]


# Candidate Serializer
class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ["id", "title", "firstname", "lastname", "profile", "photo"]


# Position Serializer
# class PositionSerializer(serializers.ModelSerializer):
#     candidates = CandidateSerializer(many=True, read_only=True, source="candidate_set")
#     yes_no_options = YesNoOptionSerializer(many=True, read_only=True, source="yes_no_options")

#     class Meta:
#         model = Position
#         fields = ["id", "description", "vote_type", "max_vote", "priority", "instructions", "candidates", "yes_no_options"]

class PositionSerializer(serializers.ModelSerializer):
    candidates = CandidateSerializer(many=True, read_only=True)  # No need for source="candidate_set"
    yes_no_options = YesNoOptionSerializer(many=True, read_only=True)  # Remove source="yes_no_options"

    class Meta:
        model = Position
        fields = ["id", "description", "vote_type", "max_vote", "priority", "instructions", "candidates", "yes_no_options"]


# Election Serializer  
class ElectionSerializer(serializers.ModelSerializer):
    positions = PositionSerializer(many=True, read_only=True, source="position_set")

    class Meta:
        model = Election
        fields = ["id", "name", "status", "start_date", "end_date", "start_time", "end_time", "max_vote", "golive", "priority", "instructions", "positions"]



# Ensure VoteSerializer is properly defined
class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'

    def validate(self, data):
        """Ensure a voter can only vote once per position in an election."""
        voter = data.get('voter')
        candidate = data.get('candidate')

        if Vote.objects.filter(voter=voter, candidate__position=candidate.position).exists():
            raise serializers.ValidationError("You have already voted for this position.")

        return data