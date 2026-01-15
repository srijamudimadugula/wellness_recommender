class UserContextManager:
    """
    Manages user session data and interaction history in-memory.
    """
    def __init__(self):
        # {user_id: {'interactions': int, 'avg_feedback': float, 'success_count': int}}
        self.user_store = {}

    def get_user_context(self, user_id):
        """
        Retrieve context stats for a user.
        Args:
            user_id: string identifier
        Returns:
            dict with context features
        """
        if user_id not in self.user_store:
            # Cold user
            return {
                'avg_feedback': 0.0,
                'interaction_count': 0,
                'success_rate': 0.0
            }
        
        data = self.user_store[user_id]
        total = data['interactions']
        success_rate = data['success_count'] / total if total > 0 else 0.0
        
        return {
            'avg_feedback': data['avg_feedback'],
            'interaction_count': total,
            'success_rate': success_rate
        }

    def update_user_context(self, user_id, reward):
        """
        Update user stats after feedback.
        Reward is assumed -1 to 1.
        """
        if user_id not in self.user_store:
            self.user_store[user_id] = {
                'interactions': 0,
                'avg_feedback': 0.0,
                'success_count': 0
            }
        
        data = self.user_store[user_id]
        
        # Update running average
        n = data['interactions']
        current_avg = data['avg_feedback']
        new_avg = (current_avg * n + reward) / (n + 1)
        
        data['avg_feedback'] = new_avg
        data['interactions'] += 1
        
        if reward > 0:
            data['success_count'] += 1
            
        self.user_store[user_id] = data
