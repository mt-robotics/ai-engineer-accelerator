from typing import List, Dict, Any
from .progress import ProgressData


# Enhanced Progress Analytics
class ProgressAnalytics:
    @staticmethod
    def calculate_learning_velocity(progress: ProgressData) -> Dict[str, float]:
        """Calculate learning velocity metrics"""
        days_active = max(1, len(progress.completedTasks) / 3)  # Rough estimate

        return {
            "xp_per_day": progress.totalXP / days_active,
            "tasks_per_day": len(progress.completedTasks) / days_active,
            "efficiency_score": progress.totalXP
            / max(1, len(progress.struggledTasks) + 1),
            "consistency_score": (
                progress.streak / days_active if days_active > 0 else 0
            ),
        }

    @staticmethod
    def predict_certification_readiness(
        progress: ProgressData,
    ) -> Dict[str, Dict[str, Any]]:
        """Predict certification readiness based on progress"""
        readiness = {}

        for cert, progress_pct in progress.certificationProgress.items():
            estimated_days = max(1, (100 - progress_pct) / 2)  # 2% per day estimate

            readiness[cert] = {
                "current_progress": progress_pct,
                "estimated_days_to_ready": estimated_days,
                "confidence_level": (
                    "high"
                    if progress_pct > 70
                    else "medium" if progress_pct > 40 else "low"
                ),
                "recommended_focus": (
                    "practice_exams" if progress_pct > 60 else "foundation_building"
                ),
            }

        return readiness

    @staticmethod
    def generate_personalized_recommendations(progress: ProgressData) -> List[str]:
        """Generate AI-powered learning recommendations"""
        recommendations = []

        # Difficulty adjustment recommendations
        struggle_rate = len(progress.struggledTasks) / max(
            1, len(progress.completedTasks)
        )
        if struggle_rate > 0.3:
            recommendations.append(
                "Consider reviewing fundamentals - high struggle rate detected"
            )
        elif struggle_rate < 0.1:
            recommendations.append(
                "You're doing great! Consider taking on more challenging projects"
            )

        # Progress velocity recommendations
        if progress.totalXP < progress.currentWeek * 1000:
            recommendations.append(
                "Increase daily study time to meet weekly XP targets"
            )

        # Certification recommendations
        max_cert_progress = max(progress.certificationProgress.values())
        if max_cert_progress > 80:
            recommendations.append(
                "You're close to certification! Schedule your exam soon"
            )

        # Portfolio recommendations
        if len(progress.portfolioItems) < progress.currentWeek:
            recommendations.append("Focus on completing more portfolio projects")

        return recommendations[:3]  # Limit to top 3 recommendations


# Create singleton instance
analytics = ProgressAnalytics()
