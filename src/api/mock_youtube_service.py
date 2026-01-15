
import logging

logger = logging.getLogger(__name__)

class MockYouTubeService:
    """
    Mock implementation of YouTubeService for testing and offline development.
    Returns deterministic, safe dummy data.
    """
    def __init__(self):
        logger.info("Initialized Mock YouTube Service")

    def build_bio_query(self, emotion: str, phase: str, just_ate: bool, keywords: list[str] = None) -> str:
        parts = [emotion, phase]
        if just_ate:
            parts.append("gentle")
        if keywords:
            parts.extend(keywords)
        return " ".join(parts)

    def search_and_enrich(self, query: str, max_results: int = 20) -> list[dict]:
        """Return hardcoded mock videos covering different quality tiers."""
        
        # 1. High Quality Match
        v1 = {
            'video_id': 'mock_01',
            'title': 'Perfect Morning Yoga Flow',
            'url': 'https://youtube.com/watch?v=mock_01',
            'thumbnail': 'https://placehold.co/600x400/png',
            'channel_name': 'Yoga With Adriene',
            'channel_id': 'UCFKE7WVJfvaHW5q283SxchA',
            'views': 5000000,
            'likes': 150000,
            'comments': 5000,
            'channel_subscribers': 11000000,
            'duration_minutes': 20.0,
            'published_days_ago': 30,
            'engagement_ratio': 0.03,
            'demo_boost': 10.0 # Premium channel
        }
        
        # 2. Average Quality
        v2 = {
            'video_id': 'mock_02',
            'title': 'Simple Stretching',
            'url': 'https://youtube.com/watch?v=mock_02',
            'thumbnail': 'https://placehold.co/600x400/png',
            'channel_name': 'Daily Stretch',
            'channel_id': 'UC_mock_ch_02',
            'views': 50000,
            'likes': 1000,
            'comments': 50,
            'channel_subscribers': 100000,
            'duration_minutes': 10.5,
            'published_days_ago': 100,
            'engagement_ratio': 0.02,
            'demo_boost': 0.0
        }
        
        # 3. New/Low Stats
        v3 = {
            'video_id': 'mock_03',
            'title': 'My First Yoga Vlog',
            'url': 'https://youtube.com/watch?v=mock_03',
            'thumbnail': 'https://placehold.co/600x400/png',
            'channel_name': 'New Yogi',
            'channel_id': 'UC_mock_ch_03',
            'views': 100,
            'likes': 5,
            'comments': 0,
            'channel_subscribers': 10,
            'duration_minutes': 5.0,
            'published_days_ago': 2,
            'engagement_ratio': 0.05,
            'demo_boost': 0.0
        }

        # Return enough to satisfy max_results, cycling through mocks
        import itertools
        cycle_vids = itertools.cycle([v1, v2, v3])
        return [next(cycle_vids) for _ in range(max_results)]

    def get_video_details(self, video_ids):
        return [] # Not used in main flow if search_and_enrich is mocked
