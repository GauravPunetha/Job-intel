
import urllib.robotparser as rp

def allowed_to_fetch(robots_url: str, agent: str, target_url: str) -> bool:
    parser = rp.RobotFileParser()
    parser.set_url(robots_url)
    try:
        parser.read()
        return parser.can_fetch(agent, target_url)
    except Exception:
        # Fail closed: if robots can't be read, do not fetch
        return False
