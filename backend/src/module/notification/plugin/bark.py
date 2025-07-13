import logging

from module.models import Notification
from module.network import RequestContent

logger = logging.getLogger(__name__)


class BarkNotification(RequestContent):
    def __init__(self, token, **kwargs):
        super().__init__()
        if kwargs.get("bark_base_url", None) is not None:
            self.base_url = kwargs.get("bark_base_url")
        self.base_url = f"https://api.day.app/{token}"

    @staticmethod
    def gen_message(notify: Notification) -> str:
        text = f"""
        番剧名称：{notify.official_title} 季度： 第{notify.season}季 更新集数： 第{notify.episode}集
        """
        return text.strip()

    def check_token(self) -> bool:
        if not self.check_connection(self.base_url):
            logger.error("Bark notification failed: Invalid token")
            return False
        logger.debug(f"Passing Bark notification check : {self.base_url}")
        return True

    def post_msg(self, notify: Notification) -> bool:
        logger.debug(f"Passing Bark notification check : {self.base_url}")
        text = self.gen_message(notify)
        total_msg = f"{self.base_url}/{notify.official_title}/{text}"
        logger.debug(f"Bark notification: {total_msg}")
        resp = self.post_url(total_msg, data={})
        if resp is None:
            logger.error("Bark notification failed: No response")
            return False
        logger.debug(f"Bark notification: {resp.status_code}")
        return resp.status_code == 200


if __name__ == "__main__":
    dummy_notify = Notification(
        official_title="test",
        season=1,
        episode=1,
    )
    with BarkNotification("") as obj:
        if obj.check_token():
            print("Bark notification check passed")
            print(obj.post_msg(dummy_notify))
        else:
            print("Bark notification check failed")
