import numpy as np
import matplotlib.pyplot as plt
import os

class LinUCBEvaluator:
    def __init__(self):
        self.rewards = []
        
    def log_interaction(self, reward):
        self.rewards.append(reward)
        
    def get_metrics(self):
        total = len(self.rewards)
        if total == 0:
            return {'total': 0, 'cumulative_reward': 0, 'success_rate': 0.0}
            
        cum_reward = sum(self.rewards)
        success_rate = len([r for r in self.rewards if r > 0]) / total
        
        return {
            'total': total,
            'cumulative_reward': cum_reward,
            'success_rate': success_rate
        }
        
    def plot_learning_curve(self, save_path='./evaluation/learning_curve.png'):
        if not self.rewards:
            return
            
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        cumulative = np.cumsum(self.rewards)
        
        plt.figure(figsize=(10, 5))
        plt.plot(cumulative, label='Cumulative Reward')
        plt.title('LinUCB Learning Curve')
        plt.xlabel('Interactions')
        plt.ylabel('Reward')
        plt.legend()
        plt.grid(True)
        plt.savefig(save_path)
        plt.close()
