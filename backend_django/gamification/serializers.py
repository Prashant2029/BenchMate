from rest_framework import serializers
from .models import UserProfile, UserAchievement, QuizResult

class AchievementSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='achievement.name')
    description = serializers.CharField(source='achievement.description')
    icon = serializers.CharField(source='achievement.icon')

    class Meta:
        model = UserAchievement
        fields = ('name', 'description', 'icon', 'earned_at')

class QuizResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizResult
        fields = ('score', 'total_questions', 'xp_earned', 'created_at')

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    achievements = AchievementSerializer(source='user.achievements', many=True, read_only=True)
    quiz_history = QuizResultSerializer(source='user.quiz_results', many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = ('username', 'xp', 'weekly_xp', 'level', 'rank', 'achievements', 'quiz_history')
