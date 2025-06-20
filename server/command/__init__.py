from typing import Any, List, Optional

import loguru


class Command:  # Using a class instead of a decorator for simplicity
    def __init__(
        self,
        label: str,
        aliases: Optional[List[str]] = None,
        usage: Optional[List[str]] = None,
        description: str = "",  # Added description
        target_requirement: str = "NONE",
    ):
        self.label = label
        self.aliases = aliases or []
        self.usage = usage or []
        self.target_requirement = target_requirement
        self.description = description  # Store description


class CommandHandler:
    """
    Base class for command handlers.  This replaces the Java interface.
    """

    @staticmethod
    async def send_message(
        sender: Optional[Any],  # Player or None (for console)
        message: str,
    ) -> None:
        """
        Send a message to the target.  This is a static method.

        Args:
            sender: The player to send the message to, or None for the server console.
            message: The message to send.
        """
        #  In a real application, you'd have an event system.  For now, we'll
        #  just log or send directly.
        #  You might have something like:
        #  event = ReceiveCommandFeedbackEvent(sender, message)
        #  await event.call()
        #  if event.is_cancelled():
        #      return

        if sender is None:
            loguru.logger.info(message)  # Log to console
        else:
            #  Assuming 'sender' has a 'send_message' method
            await sender.send_message(
                message.replace("\n\t", "\n\n")
            )  #  Adjust as needed
            #  player.dropMessage(event.getMessage().replace("\n\t", "\n\n"));

    @staticmethod
    async def send_translated_message(
        sender: Optional[Any], message_key: str, *args: Any
    ) -> None:
        """
        Send a translated message.  This is a static method.

        Args:
            sender: The player or None.
            message_key: The message key.
            *args:  Arguments for translation.
        """
        #  In a real application, you'd have a translation system.
        #  For this example, we'll assume a simple dictionary lookup.
        # translated_message = translate(player, messageKey, args);
        translated_message = message_key.format(
            *args
        )  #  Very basic placeholder.
        await CommandHandler.send_message(sender, translated_message)

    def get_usage_string(self, sender: Optional[Any], *args: str) -> str:
        """
        Get the usage string for the command.

        Args:
            sender: The player or None.
            *args:  Additional arguments.
        """
        command_annotation = getattr(
            self.__class__, "command_annotation", None
        )  # Get annotation.
        if not command_annotation:
            return "Usage not defined."  # Or raise an exception

        usage_prefix = "Usage: "  # TODO Hardcoded,  you'd replace with a translation
        command = command_annotation.label
        for alias in command_annotation.aliases:
            if len(alias) < len(command):
                command = alias
        if sender is not None:
            command = "/" + command
        target = ""
        if command_annotation.target_requirement == "OFFLINE":
            target = "@<UID> "  # TODO: make translation keys
        elif command_annotation.target_requirement in ("ONLINE", "PLAYER"):
            target = "@<UID> " if sender is None else "[@<UID>] "
        joiner = "\n\t".join(
            usage_prefix + command + " " + target + usage
            for usage in command_annotation.usage
        )
        return joiner

    async def send_usage_message(self, sender: Optional[Any], *args: str) -> None:
        """
        Send the usage message.

        Args:
            sender: The player or None.
            *args:  Additional arguments.
        """
        await self.send_message(sender, self.get_usage_string(sender, *args))

    def get_label(self) -> str:
        """Get the command label."""
        command_annotation = getattr(
            self.__class__, "command_annotation", None
        )  # Get annotation.

        if command_annotation:
            return command_annotation.label
        return ""  # Or raise an exception

    def get_description_key(self) -> str:
        """Get the description key."""
        command_annotation = getattr(
            self.__class__, "command_annotation", None
        )  # Get annotation.
        if command_annotation:
            return "commands.{}.description".format(command_annotation.label)
        return ""  # Or raise exception

    def get_description_string(self, sender: Optional[Any]) -> str:
        """Get the description string."""
        # return translate(player, getDescriptionKey());
        return self.get_description_key()  # Placeholder

    async def execute(
        self, sender: Optional[Any], target_player: Optional[Any], args: List[str]
    ) -> None:
        """
        Execute the command.  This is the equivalent of the Java execute method.

        Args:
            sender:  The player or console that invoked the command.
            target_player: The target player, if applicable.
            args:    The command arguments.
        """
        raise NotImplementedError(
            "Subclasses must implement the execute method."
        )  # Make abstract