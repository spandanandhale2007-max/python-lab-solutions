"""
Experiment 3 - Question 5: Notification Factory

Scenario: A factory that returns different notification classes based on input:
Email, SMS or Push.

Rubrics covered:
  * factory returns the correct class
  * each notification type has a send() method
  * inheritance / a common interface used
  * easy to extend with new types
"""

from abc import ABC, abstractmethod


class Notification(ABC):
    """Common interface every channel must satisfy."""

    channel = "generic"

    def __init__(self, recipient):
        self.recipient = recipient
        self.sent = 0

    @abstractmethod
    def send(self, message):
        ...

    def _ok(self, detail):
        self.sent += 1
        print(f"  [{self.channel.upper():<5}] -> {self.recipient}: {detail}")
        return True


class EmailNotification(Notification):
    channel = "email"
    MAX_SUBJECT = 60

    def send(self, message, subject="Notification from MediVerse"):
        subject = subject[:self.MAX_SUBJECT]
        print(f"  Connecting to SMTP smtp.gmail.com:587 ...")
        return self._ok(f"subject={subject!r} body={message[:50]!r}")


class SMSNotification(Notification):
    channel = "sms"
    MAX_LEN = 160

    def send(self, message):
        parts = [message[i:i + self.MAX_LEN]
                 for i in range(0, len(message), self.MAX_LEN)] or [""]
        print(f"  Hitting SMS gateway for +91{self.recipient[-10:]} ...")
        return self._ok(f"{len(parts)} segment(s): {parts[0][:40]!r}")


class PushNotification(Notification):
    channel = "push"

    def send(self, message, title="MediVerse"):
        print("  Posting to FCM topic ...")
        return self._ok(f"title={title!r} payload={message[:40]!r}")


class WhatsAppNotification(Notification):
    """Added later: the factory needs one new line, nothing else changes."""
    channel = "wa"

    def send(self, message, template="appointment_reminder"):
        print("  Calling the WhatsApp Business API ...")
        return self._ok(f"template={template} text={message[:40]!r}")


class NotificationFactory:
    _registry = {
        "email": EmailNotification,
        "sms": SMSNotification,
        "push": PushNotification,
        "whatsapp": WhatsAppNotification,
    }

    @classmethod
    def create(cls, kind, recipient):
        try:
            klass = cls._registry[kind.strip().lower()]
        except KeyError:
            raise ValueError(
                f"unknown channel {kind!r}; available: "
                f"{', '.join(sorted(cls._registry))}") from None
        return klass(recipient)

    @classmethod
    def register(cls, kind, klass):
        """Extension point: plug in a new channel at runtime."""
        if not issubclass(klass, Notification):
            raise TypeError("channel must subclass Notification")
        cls._registry[kind] = klass
        print(f"[factory] registered new channel {kind!r} -> {klass.__name__}")

    @classmethod
    def channels(cls):
        return sorted(cls._registry)


if __name__ == "__main__":
    print("available channels:", NotificationFactory.channels())

    print("\n=== factory returns the matching class ===")
    for kind, who in (("email", "spandan@example.com"),
                      ("sms", "+919011223344"),
                      ("push", "device-token-ab12cd"),
                      ("whatsapp", "+919011223344")):
        obj = NotificationFactory.create(kind, who)
        print(f"  create({kind!r}) -> {type(obj).__name__}")

    print("\n=== same call, different behaviour ===")
    msg = "Your appointment with Dr. Kulkarni is confirmed for tomorrow 10:30 AM."
    for kind, who in (("email", "spandan@example.com"),
                      ("sms", "+919011223344"),
                      ("push", "device-token-ab12cd")):
        NotificationFactory.create(kind, who).send(msg)

    print("\n=== unknown channel ===")
    try:
        NotificationFactory.create("telegram", "@spandan")
    except ValueError as e:
        print("  ", e)

    print("\n=== extending the factory without touching existing code ===")
    class SlackNotification(Notification):
        channel = "slack"

        def send(self, message):
            return self._ok(f"posted to #{self.recipient}: {message[:30]!r}")

    NotificationFactory.register("slack", SlackNotification)
    NotificationFactory.create("slack", "ops-alerts").send(msg)
    print("  channels now:", NotificationFactory.channels())
