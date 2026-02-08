import uuid
from datetime import datetime
from sqlmodel import Session
from src.database import engine
from src.models.conversation import Conversation

print("Testing conversation creation directly...")

try:
    with Session(engine) as session:
        conversation = Conversation(
            user_id="test-user-id",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        print(f"Created conversation object with ID: {conversation.id}")
        
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        
        print(f"Conversation saved successfully with ID: {conversation.id}")
        
except Exception as e:
    print(f"Error creating conversation: {e}")
    import traceback
    traceback.print_exc()