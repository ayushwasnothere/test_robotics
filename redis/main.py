import redis

r = redis.Redis(decode_responses=True)


def create_group(stream, group):
    try:
        r.xgroup_create(stream, group, id="0", mkstream=True)
    except redis.ResponseError as e:
        if "BUSYGROUP" not in str(e):
            raise


create_group("robot.tasks", "ros_bridge")
create_group("robot.events", "langgraph")

print("Streams ready")
