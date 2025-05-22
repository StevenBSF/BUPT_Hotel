
from models.room import Room

class RoomRepository:
    def __init__(self):
        # 用一个 dict 简单模拟存储
        self._rooms: dict[str, Room] = {}

    def add(self, room: Room) -> None:
        """把房间对象注册到仓库里"""
        self._rooms[room.room_id] = room

    def get_by_id(self, room_id: str) -> Room | None:
        """根据 room_id 返回对应的 Room，找不到就返回 None"""
        return self._rooms.get(room_id)