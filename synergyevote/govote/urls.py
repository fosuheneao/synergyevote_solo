from django.urls import path
from .views import VoterLoginView, VPassVerifyView, ElectionListView, CandidateListView, VoteView, vote_stats_api

urlpatterns = [
    path('voter/login/', VoterLoginView.as_view(), name='voter-login'),
    path('voter/vpass/', VPassVerifyView.as_view(), name='voter-vpass'),
    path('elections/', ElectionListView.as_view(), name='election-list'),
    path('candidates/<int:election_id>/', CandidateListView.as_view(), name='candidate-list'),
    path('vote/', VoteView.as_view(), name='vote'),
    path("api/vote-stats/", vote_stats_api, name="vote-stats-api"),
]