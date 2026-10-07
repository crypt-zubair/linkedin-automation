from __future__ import annotations
import sys
from app.checker import check_post
from app.config import MAX_POSTS, MIN_QUALITY_SCORE, TEST_MODE
from app.database import completed_count, connect, save_post
from app.generator import generate_post
from app.linkedin import publish_post
from app.logger import get_logger
from app.selector import select_unused_fact

def run() -> int:
    logger = get_logger()
    connection = connect()
    try:
        done = completed_count(connection)
        if done >= MAX_POSTS:
            logger.info('Maximum successful posts reached: %s/%s', done, MAX_POSTS)
            return 0
        fact = select_unused_fact(connection)
        logger.info('Selected fact %s (%s)', fact['id'], fact['category'])
        post, style = generate_post(fact)
        score, notes = check_post(post, fact)
        logger.info('Generated style=%s quality=%.1f', style, score)
        if notes: logger.info('Checker notes: %s', '; '.join(notes))
        if score < MIN_QUALITY_SCORE:
            logger.error('Post rejected: quality %.1f is below %.1f', score, MIN_QUALITY_SCORE)
            return 2
        print('\n--- GENERATED POST ---\n' + post + '\n\n----------------------\n')
        if TEST_MODE:
            save_post(connection, fact_id=int(fact['id']), category=fact['category'], fact=fact['fact'], source=fact['source'], post_text=post, quality_score=score, status='TEST_SAVED')
            logger.info('TEST_MODE=true: post saved but not published.')
            return 0
        post_id = publish_post(post)
        save_post(connection, fact_id=int(fact['id']), category=fact['category'], fact=fact['fact'], source=fact['source'], post_text=post, quality_score=score, status='PUBLISHED', linkedin_post_id=post_id)
        logger.info('Published LinkedIn post: %s', post_id)
        return 0
    except Exception:
        logger.exception('Autopilot run failed.')
        return 1
    finally:
        connection.close()

if __name__ == '__main__':
    sys.exit(run())
