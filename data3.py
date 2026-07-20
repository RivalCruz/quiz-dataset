"""
AI vs Human quiz dataset.

Each item has:
- id: unique identifier (used to look up answers without leaking the source)
- content: path to the image, served as a static file
- source: "AI" or "Human"  (never sent to the client before they guess)
- explanation: shown after the player answers
"""

quiz_data = {
    "ai_work": [
        {
            "id": "ai_001",
            "content": "/images/test.jpg",
            "source": "AI",
            "explanation": "Fine detail and lighting are impressive, but small structural "
                           "inconsistencies (misaligned windows, odd shadow angles) are a "
                           "common AI image generation artifact.",
        },
        {
            "id": "ai_002",
            "content": "/images/ai_work_2.jpg",
            "source": "AI",
            "explanation": "Skin texture looks smooth and even, but the earrings are "
                           "asymmetrical and one hand has six fingers — a classic AI-image tell.",
        },
        {
            "id": "ai_003",
            "content": "/images/ai_work_3.jpg",
            "source": "AI",
            "explanation": "The background text on the sign is garbled and unreadable, "
                           "another common failure mode for AI-generated images.",
        },
    ],
    "human_work": [
        {
            "id": "human_001",
            "content": "/images/human_work_1.jpg",
            "source": "Human",
            "explanation": "Visible brush strokes and a slightly uneven horizon line reflect "
                           "the physical, imperfect process of a human artist.",
        },
        {
            "id": "human_002",
            "content": "/images/human_work_2.jpg",
            "source": "Human",
            "explanation": "The photo has natural depth-of-field blur and a slightly "
                           "off-center composition, consistent with a handheld human-taken photograph.",
        },
        {
            "id": "human_003",
            "content": "/images/human_work_3.jpg",
            "source": "Human",
            "explanation": "Fine anatomical details (hands, ears) are consistent and correctly "
                           "proportioned, with visible pencil sketch lines underneath the ink.",
        },
    ],
}

# Flat lookup used by the API
all_items = quiz_data["ai_work"] + quiz_data["human_work"]
items_by_id = {item["id"]: item for item in all_items}
