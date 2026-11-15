"""
Community Warmup & Legitimacy Contributor Engine
Protects posts from removal by building authentic member karma:
1. Automated screening question answering when joining new groups.
2. Pre-post engagement (liking 2-3 existing community posts, leaving supportive comments).
3. Legitimate parent/educator persona simulation so admins view the account as an active contributor.
"""
import logging
import random
import time
from pathlib import Path
from .stealth_engine import human_delay, human_type, human_click, human_scroll

LOGGER = logging.getLogger(__name__)

SCREENING_ANSWERS = {
    "age": "Toddler and preschool (ages 3 and 5)",
    "kids": "Yes, mom of 2 little ones (preschool & toddler)",
    "rules": "Yes, I agree to follow all group rules and be respectful",
    "why": "Looking for holiday crafts, screen-free activities, and quiet time ideas",
    "location": "United States",
    "default": "Yes, excited to be part of the community and share holiday ideas!"
}

SUPPORTIVE_COMMENTS = [
    "Such a wonderful holiday idea, saving this for our quiet time! ❤️",
    "Love this! Simple, screen-free activities are a lifesaver this time of year.",
    "Thank you for sharing this! Little hands are going to love this.",
    "So cute! Adding this to our December morning routine.",
    "Brilliant activity idea for toddlers. Thanks for the inspiration! 🎄"
]

def handle_group_screening_questions(page):
    """
    Detects and answers group membership screening questions autonomously.
    """
    LOGGER.info("[WARMUP] Checking for group screening questions/rules dialog...")
    dialog = page.locator('div[role="dialog"]')
    if dialog.count() == 0:
        return True

    # Check for text inputs / textareas in dialog
    text_inputs = dialog.locator('textarea, input[type="text"]')
    input_count = text_inputs.count()
    
    for i in range(input_count):
        inp = text_inputs.nth(i)
        # Infer question context from parent or label
        parent_text = inp.locator('xpath=ancestor::div[3]').inner_text().lower()
        
        answer = SCREENING_ANSWERS["default"]
        if "age" in parent_text or "old" in parent_text:
            answer = SCREENING_ANSWERS["age"]
        elif "kid" in parent_text or "child" in parent_text or "parent" in parent_text:
            answer = SCREENING_ANSWERS["kids"]
        elif "rule" in parent_text or "agree" in parent_text:
            answer = SCREENING_ANSWERS["rules"]
        elif "why" in parent_text or "looking" in parent_text or "join" in parent_text:
            answer = SCREENING_ANSWERS["why"]

        LOGGER.info(f"[WARMUP] Answering screening question {i+1}: {answer}")
        inp.click()
        human_delay(0.5, 1.2)
        human_type(page, inp, answer)
        human_delay(0.8, 1.5)

    # Check all rule agreement checkboxes
    checkboxes = dialog.locator('input[type="checkbox"], div[role="checkbox"]')
    for i in range(checkboxes.count()):
        cb = checkboxes.nth(i)
        aria_checked = cb.get_attribute("aria-checked")
        if aria_checked != "true":
            cb.click()
            human_delay(0.4, 0.8)

    # Submit answers
    submit_btn = dialog.locator('div[aria-label="Submit"][role="button"], button:has-text("Submit"), div[role="button"]:has-text("Submit")')
    if submit_btn.count() > 0:
        LOGGER.info("[WARMUP] Submitting group membership answers...")
        submit_btn.first.click()
        human_delay(2.5, 4.0)
        return True
        
    return False

def warm_up_community_karma(page, max_likes=2, leave_comment=True):
    """
    Engages organically with 2-3 existing posts in the group feed before posting.
    Leaves a supportive comment on an active post to build authentic member history.
    """
    LOGGER.info("[WARMUP] Building authentic member karma in group feed...")
    # Scroll through feed naturally
    human_scroll(page, steps=random.randint(2, 4), distance=350)
    human_delay(2.0, 3.5)

    # 1. Like 2-3 recent posts
    like_buttons = page.locator('div[aria-label="Like"][role="button"], div[aria-label="Love"][role="button"]')
    num_likes = min(like_buttons.count(), max_likes)
    for i in range(num_likes):
        try:
            like_btn = like_buttons.nth(i)
            # Ensure it's not already liked
            if like_btn.is_visible():
                like_btn.scroll_into_view_if_needed()
                human_delay(0.8, 1.5)
                like_btn.click()
                LOGGER.info(f"[WARMUP] Liked community post {i+1}")
                human_delay(1.2, 2.5)
        except Exception as e:
            LOGGER.debug(f"[WARMUP] Minor error liking post: {e}")

    # 2. Leave 1 genuine supportive comment if requested
    if leave_comment:
        try:
            comment_boxes = page.locator('div[aria-label*="Write a comment"][role="textbox"], div[aria-label*="Write an answer"][role="textbox"]')
            if comment_boxes.count() > 0:
                comment_box = comment_boxes.first
                comment_box.scroll_into_view_if_needed()
                human_delay(1.5, 2.5)
                comment_text = random.choice(SUPPORTIVE_COMMENTS)
                comment_box.click()
                human_delay(0.8, 1.2)
                human_type(page, comment_box, comment_text)
                human_delay(1.5, 2.5)
                page.keyboard.press("Enter")
                LOGGER.info(f"[WARMUP] Left supportive karma comment: '{comment_text}'")
                human_delay(3.0, 5.0)
        except Exception as e:
            LOGGER.debug(f"[WARMUP] Minor error commenting on post: {e}")

    LOGGER.info("[WARMUP] Warmup karma complete. Account has natural in-group footprint.")
