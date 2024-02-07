import base64
import uuid


def new_feed_name():
    # Generate a new, unique feed name using a random UUID.
    # Uniqueness is important because feed names are used to identify
    # files associated with each feed; name collisions would
    # compromise the integrity of the service.
    u = uuid.uuid4()
    # base64 encode UUID to make it a little less unwieldy, and remove
    # padding (we won't ever need to decode it)
    return base64.urlsafe_b64encode(u.bytes).decode('utf-8')[:-2]
