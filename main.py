from typing import List
from typing import Optional

from sqlalchemy.orm import relationship
from sqlalchemy.orm import RelationshipProperty


class Comment:
    def __init__(self, id: Optional[int] = None, comment_id: Optional[int] = None, text: Optional[str] = None):
        self.id = id
        self.comment_id = comment_id
        self.text = text  # Assuming you have a text attribute for the comment

        # Do not manually initialize replies here; SQLAlchemy manages it
        # self.replies: List['Comment'] = []  # Remove this initialization

    # Type hint for replies attribute
    replies: RelationshipProperty[List["Comment"]]

    def add_reply(self, reply_text: str) -> "Comment":
        """
        Adds a reply to the current comment.

        Parameters:
            reply_text (str): The text of the reply.

        Returns:
            Comment: The newly created reply.
        """
        # Create a new Comment object representing the reply
        reply = Comment(comment_id=self.id, text=reply_text)

        # Append the reply to the list of replies using the relationship
        self.replies.append(reply)

        # Return the newly created reply for further use if needed
        return reply
